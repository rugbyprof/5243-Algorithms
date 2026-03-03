from __future__ import annotations
# ^ This lets Python treat type hints as "strings" until later, instead of needing
#   every type to already exist at runtime.
#   Example: if a function says it returns TrialRow, Python won't freak out if
#   TrialRow is defined further down in the file.
#   It's mostly a "type hint convenience" feature.

from dataclasses import dataclass
# ^ dataclass = a shortcut for making simple "data containers" (like a record/row).
#   It auto-creates __init__, __repr__, comparisons, etc., so you don't write boilerplate.

from typing import List, Tuple, Dict, Any
# ^ Type hints:
#   - List[T] means "a list of T"
#   - Tuple[A, B] means "a pair: (A, B)"
#   - Dict[K, V] means "mapping from K to V"
#   - Any means "anything goes" (like a wildcard)

import subprocess
# ^ Used to run external programs (your C++ executable) from Python.

import json
# ^ Used to parse JSON text into Python dictionaries (and vice versa).

import statistics
# ^ We use this for median() to summarize multiple trial runs robustly.

import time
# ^ Imported but not used in this snippet.
#   (Not wrong, just currently unused — could be used elsewhere for timing.)

# Same Op list format the harness produces:
# ops = [("insert", 123), ("contains", 456), ...]
# In plain English: ops is a "to-do list" of operations to perform on a data structure.
# Each item is (operation_name, value).
Op = Tuple[str, int]
# ^ A single operation is a 2-item tuple:
#   - first item: the action, like "insert", "delete", "contains"
#   - second item: the integer the action is applied to


@dataclass
class TrialRow:
    """
    Think of this as ONE row in your results table.

    A trial run produces a bunch of measurements (time, comparisons, etc.)
    and this class stores them in a neat bundle.
    """
    structure: str         # Name of the data structure tested (e.g., "BST", "HASH")
    workload: str          # Name/label of the workload pattern (e.g., "random", "zipf")
    n: int                 # Typically the size of the workload or number of operations
    trial: int             # Which repetition this is (trial 0, 1, 2, ...)
    seconds: float         # How long the trial took in wall-clock seconds
    comparisons: int       # How many key comparisons happened (algorithm "work")
    structural_ops: int    # "Internal" operations (rotations, probes, rebalances, etc.)
    inserts: int           # How many inserts were performed
    deletes: int           # How many deletes were performed
    lookups: int           # How many contains/find operations were performed
    resize_events: int     # How many resizes happened (mostly relevant for hash tables)


class CppRunnerAdapter:
    """
    This is a "translator" between Python and your C++ benchmark runner.

    Big picture:
      1) Python generates a list of operations (ops)
      2) This adapter formats those ops as text and sends them to the C++ program via stdin
      3) The C++ program prints ONE line of JSON to stdout
      4) This adapter reads that JSON line and converts it into a TrialRow object

    Why do this?
    - Python is great for orchestrating experiments.
    - C++ is great for fast data structure implementations.
    - This glues them together with minimal drama.
    """

    def __init__(self, exe_path: str, structure_flag: str):
        """
        Store:
          - where the C++ executable lives (exe_path)
          - which data structure the C++ runner should test (structure_flag)

        Example:
          exe_path = "./runner"
          structure_flag = "BST"
        """
        self.exe_path = exe_path
        self.structure_flag = structure_flag  # e.g. "BST", "HASH", etc.

    def run_trial(self, ops: List[Op], workload: str, n: int, trial: int) -> TrialRow:
        """
        Run ONE benchmark trial in the C++ program and return results as a TrialRow.

        Parameters:
          ops:     list of operations like [("insert", 5), ("contains", 9), ...]
          workload: a label describing this workload pattern
          n:       size/scale label (often number of operations or problem size)
          trial:   which run number this is (helps you repeat and average/median later)
        """

        # Convert our list of ("op", value) into the plain-text format the C++ runner expects.
        #
        # Example ops:
        #   [("insert", 10), ("contains", 3)]
        #
        # payload becomes:
        #   "insert 10\ncontains 3\n"
        #
        # That trailing newline is intentional — many parsers like lines ending cleanly.
        payload = "\n".join(f"{op} {val}" for op, val in ops) + "\n"

        # Build the command-line arguments for the C++ executable.
        #
        # This ends up executing something like:
        #   ./runner --structure BST --workload random --n 1000 --trial 2
        #
        # So the C++ program knows which structure/workload/run it's doing,
        # even though the operations themselves come through stdin.
        cmd = [
            self.exe_path,
            "--structure",
            self.structure_flag,
            "--workload",
            workload,
            "--n",
            str(n),
            "--trial",
            str(trial),
        ]

        # Actually run the C++ program.
        #
        # subprocess.run launches the program and waits for it to finish.
        #
        # Key points:
        # - input=payload.encode("utf-8") sends our operations into the program's stdin
        # - stdout/stderr are captured so we can read them
        # - check=False means "don't auto-throw an exception on nonzero exit code"
        #   (we do our own error message below so it's nicer)
        proc = subprocess.run(
            cmd,
            input=payload.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        # If the C++ program returned an error code, treat that as a failed trial.
        # We raise an exception and include stderr so we can see what went wrong.
        if proc.returncode != 0:
            raise RuntimeError(
                f"C++ runner failed (code={proc.returncode}).\n"
                f"stderr:\n{proc.stderr.decode('utf-8', errors='replace')}"
            )

        # Read stdout (what the C++ program printed).
        # We expect it to be exactly ONE line of JSON.
        out = proc.stdout.decode("utf-8", errors="replace").strip()

        # Enforce "ONE JSON line" rule.
        #
        # We split stdout into non-empty lines, then demand exactly 1.
        # Why be strict?
        # - It prevents accidental debug prints from breaking parsing.
        # - It forces the C++ runner to behave like a clean “API”.
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if len(lines) != 1:
            raise RuntimeError(f"Expected 1 JSON line, got {len(lines)} lines:\n{out}")

        # Parse JSON text into a Python dictionary.
        # Example JSON might look like:
        # {"structure":"BST","workload":"random","n":1000,"trial":2,"seconds":0.014,...}
        data: Dict[str, Any] = json.loads(lines[0])

        # Convert the dictionary into a TrialRow.
        # We cast types explicitly so we don't silently accept nonsense.
        # (Example: n should be int even if JSON gave it as "1000".)
        return TrialRow(
            structure=data["structure"],
            workload=data["workload"],
            n=int(data["n"]),
            trial=int(data["trial"]),
            seconds=float(data["seconds"]),
            comparisons=int(data["comparisons"]),
            structural_ops=int(data["structural_ops"]),
            inserts=int(data["inserts"]),
            deletes=int(data["deletes"]),
            lookups=int(data["lookups"]),
            resize_events=int(data["resize_events"]),
        )


def median_row(rows: List[TrialRow]) -> TrialRow:
    """
    Given multiple TrialRow results that all represent the "same experiment"
    (same structure/workload/n), return a single TrialRow whose numeric fields
    are the MEDIAN of the group.

    Why median instead of average?
    - Benchmarks are noisy. One random OS hiccup / background process can
      make a trial unusually slow.
    - Median ignores that kind of outlier better than mean does.

    Important assumption:
    - All rows in `rows` are comparable (same structure/workload/n).
      We take those labels from the first row and treat them as “the group identity.”
    """
    assert rows
    # ^ If rows is empty, median doesn't make sense.
    #   This assert will crash loudly rather than quietly returning garbage.

    base = rows[0]
    # ^ We use the first row as the "template" for non-median fields.
    #   (structure/workload/n should match across all rows.)

    medf = lambda xs: statistics.median(xs)
    # ^ Small helper function: given a list of numbers, return median.
    #   Using a lambda keeps the code compact.

    return TrialRow(
        structure=base.structure,
        workload=base.workload,
        n=base.n,

        trial=-1,
        # ^ This row isn't a real trial run; it's a summary of several.
        #   Using -1 is a common "sentinel" value meaning "not an actual trial id".

        seconds=float(medf([r.seconds for r in rows])),
        # ^ Median runtime across trials.

        comparisons=int(medf([r.comparisons for r in rows])),
        # ^ Median comparisons across trials.

        structural_ops=int(medf([r.structural_ops for r in rows])),
        # ^ Median internal structural operations.

        inserts=int(medf([r.inserts for r in rows])),
        deletes=int(medf([r.deletes for r in rows])),
        lookups=int(medf([r.lookups for r in rows])),
        resize_events=int(medf([r.resize_events for r in rows])),
        # ^ For these counts: median is usually the same as any trial if the workload
        #   is deterministic. But if your harness can vary counts, median still works.
    )