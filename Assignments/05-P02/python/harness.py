from __future__ import annotations
# ^ Lets you use type hints that refer to classes that appear later in the file
#   without doing weird quoting gymnastics. Mostly a “type checker friendliness”
#   feature; runtime behavior stays sane.

from dataclasses import dataclass, asdict
# ^ dataclass: quick way to create a simple "data holder" class
# ^ asdict: turns a dataclass into a plain Python dict (great for CSV/JSON)

from typing import Protocol, Dict, List, Tuple, Iterable, Optional
# ^ Protocol: defines an "interface" (a contract). Anything that has these methods
#   counts as a valid adapter.
# ^ Dict/List/Tuple: type hint helpers
# ^ Iterable: something you can loop over (list, generator, etc.)
# ^ Optional: value may be present or may be None (not used below, but imported)

import random
import time
import statistics
import csv
from pathlib import Path
# ^ random: generate repeatable pseudo-random numbers
# ^ time: measure performance
# ^ statistics: median (more stable than average when you get random slow runs)
# ^ csv: write results to CSV files
# ^ Path: clean file path handling (better than string paths)


# ----------------------------
# 1) Instrumentation contract
# ----------------------------
# "Instrumentation" here means: counting what happened inside the data structure.
# Not just *how long* it took, but how much *work* it did.


@dataclass
class Counters:
    """
    A simple bucket of counters.

    The idea: as your data structure runs operations, it increments these fields.
    Then the harness reads them out at the end.

    These counters are "measurement hooks" for students:
    - comparisons: how many key comparisons did we do? (e.g., x < y checks)
    - structural_ops: any “internal” re-arranging work (rotations, rehash probes, etc.)
    - inserts/deletes/lookups: how many high-level operations were requested
    - resize_events: how many times the structure resized (hash table growth, etc.)
    """
    comparisons: int = 0
    structural_ops: int = 0
    inserts: int = 0
    deletes: int = 0
    lookups: int = 0
    resize_events: int = 0  # hash tables, etc.

    def snapshot(self) -> Dict[str, int]:
        """
        Return a plain dictionary version of these counters.

        Why? Because dictionaries are easy to serialize (CSV/JSON) and inspect.
        """
        return asdict(self)
        # asdict(dataclass_instance) -> {"comparisons": 5, "inserts": 10, ...}


class StructureAdapter(Protocol):
    """
    This is the interface/contract that every student’s structure wrapper must follow.

    “Adapter” = a wrapper that makes different data structures look the same to the harness.

    Example: Your BST class might have insert/delete/contains methods.
    Your hash table might have put/remove/hasKey.
    The adapter hides those differences and presents the same names to the harness:
      insert(x), delete(x), contains(x)

    That way the harness can benchmark *anything* without knowing what it is.
    """

    # --- identity / lifecycle ---
    def name(self) -> str: ...
    # ^ Returns a display name like "BST", "HashTable", "TreapOfDoom"

    def reset(self) -> None: ...
    # ^ Clears the structure back to empty for a fresh trial.
    #   (No leftover data from previous trials.)

    def reset_counters(self) -> None: ...
    # ^ Sets all counters back to zero.

    def get_counters(self) -> Counters: ...
    # ^ Returns the Counters object so the harness can record results.

    # --- operations the harness will call ---
    def insert(self, x: int) -> None: ...
    def delete(self, x: int) -> None: ...
    def contains(self, x: int) -> bool: ...
    # ^ The harness uses only these three operations.
    #   Students map them to their implementation (BST, Hash, etc).


# ----------------------------
# 2) Workload spec (locked)
# ----------------------------
# Workloads are repeatable “scripts” of operations: what to insert/lookup/delete, and when.
# “locked” means: students shouldn't change these, so everyone's results are comparable.


@dataclass(frozen=True)
class WorkloadSpec:
    """
    Settings that define a workload run.

    frozen=True means "immutable": once created, you can't change fields.
    That’s good for experiments: prevents accidental changes mid-run.

    Fields:
      code: which workload pattern to run ("A", "B", "C", or "D")
      n: scale (often number of inserts or baseline size)
      seed: random seed for repeatability (same spec => same random numbers)
      value_range_mult: how “wide” the key range is compared to n
      trials: how many repeats to run for this workload/spec
    """
    code: str  # "A", "B", "C", "D"
    n: int
    seed: int = 42
    value_range_mult: int = 10  # values in [0, value_range_mult * n]
    trials: int = 7


def _rng(spec: WorkloadSpec) -> random.Random:
    """
    Create a Random object seeded from the spec.

    Why this helper?
    - It ensures deterministic workloads (same seed => same sequence)
    - Using your own Random instance avoids interference from other random usage
      elsewhere in the program.
    """
    return random.Random(spec.seed)


def gen_values(spec: WorkloadSpec, count: int) -> List[int]:
    """
    Generate a list of random integers.

    The values come from a controlled range:
      0 to (value_range_mult * n), inclusive

    So if n=1000 and mult=10, keys are in [0..10000].
    This makes collisions / duplicates more likely than using a huge range,
    which is good because real workloads often do repeat keys.
    """
    r = _rng(spec)
    hi = spec.value_range_mult * spec.n
    return [r.randrange(0, hi + 1) for _ in range(count)]
    # randrange(a, b) generates in [a, b-1], so hi+1 makes it inclusive


def workload_A(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    """
    Workload A:
      - Insert N random values
      - Then do N lookups (contains) of random values

    This simulates:
      “build the structure, then query it”
    """
    inserts = gen_values(spec, spec.n)
    lookups = gen_values(spec, spec.n)

    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts  # inserts returned as "population"
    # "population" here means: the set of items that were inserted.
    # Some workloads may use that later for deletes, etc.


def workload_B(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    """
    Workload B:
      - Insert N values, but SORTED
      - Then do N lookups

    This is the classic “BST worst-case bait” workload:
      - A plain BST inserting sorted keys becomes a linked list.
      - Balanced trees should handle it fine.

    So this workload is meant to expose whether a structure is robust
    against adversarial insertion order.
    """
    inserts = gen_values(spec, spec.n)
    inserts.sort()
    lookups = gen_values(spec, spec.n)

    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts


def workload_C(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    """
    Workload C:
      Total operations = 2N, mixed and randomly interleaved:
        - 50% lookups
        - 25% inserts
        - 25% deletes

    This simulates a “live” structure: queries and updates all mixed together,
    like a real service might do.

    Important detail:
      We avoid deleting from an empty structure.
      If we would delete while empty, we replace that delete with a lookup,
      so the total number of operations stays exactly 2N.
    """
    r = _rng(spec)
    hi = spec.value_range_mult * spec.n

    total_ops = 2 * spec.n
    counts = {
        "contains": total_ops // 2,
        "insert": total_ops // 4,
        "delete": total_ops - (total_ops // 2) - (total_ops // 4),  # remainder
    }
    # ^ We compute exact counts. The "delete" count uses the remainder to ensure
    #   the totals add up to 2N even when integer division truncates.

    # Generate operation types and shuffle (random order).
    op_types: List[str] = []
    for k, c in counts.items():
        op_types.extend([k] * c)
    r.shuffle(op_types)

    ops: List[Tuple[str, int]] = []
    population: List[int] = []
    # ^ population holds values that have been inserted and not yet deleted.
    #   We use it so deletes target something that “should exist” (more realistic).

    # We will delete only when population non-empty.
    for op in op_types:
        x = r.randrange(0, hi + 1)

        if op == "insert":
            population.append(x)
            ops.append(("insert", x))

        elif op == "contains":
            ops.append(("contains", x))

        else:  # delete
            if population:
                # Delete something we inserted previously.
                # Note: pop() deletes the most recently inserted (stack-like).
                # That is "good enough" for this harness, but it does bias deletes
                # toward recent inserts.
                y = population.pop()
                ops.append(("delete", y))
            else:
                # If empty, replace delete with lookup to keep op count constant.
                ops.append(("contains", x))

    return ops, population
    # population returned here is the leftovers still inserted at end of workload.
    # Not used in run_one_trial currently, but useful if you later add validation.


def workload_D(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    """
    Workload D:
      - Insert N
      - Then do 5N lookups

    This is a “read-heavy” workload:
      Many queries after a modest build phase.

    Good for showing:
      structures that have fast queries shine here,
      and expensive rebalancing (if any) is mostly paid only during insert phase.
    """
    inserts = gen_values(spec, spec.n)
    lookups = gen_values(spec, 5 * spec.n)

    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts


# Map workload code letters to functions.
WORKLOADS = {
    "A": workload_A,
    "B": workload_B,
    "C": workload_C,
    "D": workload_D,
}


# ----------------------------
# 3) Runner + reporting
# ----------------------------
# This section actually runs workloads against adapters, collects results,
# computes medians, and writes CSV reports.


@dataclass
class TrialResult:
    """
    The outcome of ONE trial run of ONE structure on ONE workload spec.

    Think of this as a row in a spreadsheet:
      structure, workload, n, trial#, seconds, comparisons, ...
    """
    structure: str
    workload: str
    n: int
    trial: int
    seconds: float
    comparisons: int
    structural_ops: int
    inserts: int
    deletes: int
    lookups: int
    resize_events: int


def run_one_trial(
    adapter: StructureAdapter, spec: WorkloadSpec, trial_idx: int
) -> TrialResult:
    """
    Run exactly one trial:
      - reset structure + counters
      - generate workload operations
      - execute them while timing
      - read counters
      - return a TrialResult

    This function is the core "benchmark loop".
    """

    adapter.reset()
    # ^ Start from empty data structure so results aren't polluted by previous trials.

    adapter.reset_counters()
    # ^ Start all counters at 0 for this trial.

    ops, _population = WORKLOADS[spec.code](spec)
    # ^ Build the operation script for this workload.
    # _population is not used here (underscore = "intentionally unused").

    t0 = time.perf_counter()
    # ^ perf_counter is a high-resolution timer appropriate for benchmarking.

    for op, x in ops:
        # The harness interprets operation strings and calls the adapter methods.
        if op == "insert":
            adapter.insert(x)
        elif op == "delete":
            adapter.delete(x)
        else:
            # Anything else is treated as lookup ("contains")
            # (This is safe because workloads only produce "contains" besides insert/delete.)
            adapter.contains(x)

    t1 = time.perf_counter()

    c = adapter.get_counters()
    # ^ Pull the counters after the trial. Students are responsible for incrementing them.

    return TrialResult(
        structure=adapter.name(),
        workload=spec.code,
        n=spec.n,
        trial=trial_idx,
        seconds=t1 - t0,
        comparisons=c.comparisons,
        structural_ops=c.structural_ops,
        inserts=c.inserts,
        deletes=c.deletes,
        lookups=c.lookups,
        resize_events=c.resize_events,
    )


def median_of_trials(results: List[TrialResult]) -> TrialResult:
    """
    Convert a list of TrialResult objects (same structure/workload/n, different trial#)
    into one “summary” TrialResult.

    We use MEDIAN for each numeric field rather than mean because benchmarks have outliers:
      - One run hits a background OS task
      - One run gets unlucky scheduling
      - One run warms caches differently

    Median is less sensitive to those random spikes.
    """
    assert results, "No results"
    base = results[0]

    med = lambda xs: float(statistics.median(xs))
    # ^ Helper: median returns a number; we force float to keep types consistent.

    return TrialResult(
        structure=base.structure,
        workload=base.workload,
        n=base.n,
        trial=-1,  # -1 indicates "median"
        # ^ Not a real trial index; this row is a statistical summary.

        seconds=med([r.seconds for r in results]),

        comparisons=int(med([r.comparisons for r in results])),
        structural_ops=int(med([r.structural_ops for r in results])),
        inserts=int(med([r.inserts for r in results])),
        deletes=int(med([r.deletes for r in results])),
        lookups=int(med([r.lookups for r in results])),
        resize_events=int(med([r.resize_events for r in results])),
    )


def write_csv(path: Path, rows: Iterable[TrialResult]) -> None:
    """
    Write a CSV file from a bunch of TrialResult rows.

    - Creates parent directories if needed.
    - Writes headers based on dataclass field names.
    - Writes each TrialResult as one CSV row.

    CSV is intentionally boring. Boring is reliable.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    # ^ Ensure output directory exists.

    rows = list(rows)
    # ^ If rows is an iterator/generator, converting to list lets us check if empty
    #   and also iterate multiple times.

    if not rows:
        return
        # ^ Nothing to write; silently exit.

    with path.open("w", newline="") as f:
        # newline="" is recommended for csv module so it doesn't insert extra blank lines.
        w = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        # ^ DictWriter wants a fixed list of columns.
        #   We take the keys from the first row's dataclass -> dict conversion.

        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))
            # ^ Convert each dataclass row to a dict and write it.


def run_suite(
    adapters: List[StructureAdapter], specs: List[WorkloadSpec], out_dir: Path
) -> None:
    """
    Run the full experiment suite:
      for each structure adapter
        for each workload spec
          run spec.trials trials
          store raw trial rows
          store median summary row

    Then write two CSV files:
      - raw_trials.csv: every trial
      - median_summary.csv: one median row per (structure, spec)
    """
    raw_rows: List[TrialResult] = []
    med_rows: List[TrialResult] = []

    for adapter in adapters:
        for spec in specs:
            # Safety: optional cap for pathological BST sorted insert
            #
            # Translation:
            # - A plain BST + sorted inserts can become O(n^2) and take forever.
            # - So for big n, skip workload B (sorted insert) for BST-like adapters.
            # - This prevents one structure from turning your benchmark into a hostage situation.
            if (
                adapter.name().lower().startswith("bst")
                and spec.code == "B"
                and spec.n > 20000
            ):
                continue

            trial_rows = [run_one_trial(adapter, spec, i) for i in range(spec.trials)]
            # ^ Run the same spec multiple times to smooth out timing noise.

            raw_rows.extend(trial_rows)
            # ^ Keep everything (good for graphs / deeper analysis).

            med_rows.append(median_of_trials(trial_rows))
            # ^ Add one summary row for this adapter+spec pair.

    write_csv(out_dir / "raw_trials.csv", raw_rows)
    write_csv(out_dir / "median_summary.csv", med_rows)


# ----------------------------
# 4) Student extension points
# ----------------------------
# This is basically assignment scaffolding / guidance:
# Students create a class that matches StructureAdapter's contract.
#
# The harness does NOT need to know anything about the real structure implementation.
# It only calls adapter.insert/delete/contains and reads adapter.get_counters().

# Students implement adapters like:
#
# class BSTAdapter:
#     def __init__(self): self.tree = BST(); self.counters = Counters()
#     def name(self): return "BST"
#     def reset(self): self.tree.clear()
#     def reset_counters(self): self.counters = Counters()
#     def get_counters(self): return self.counters
#     def insert(self, x): self.counters.inserts += 1; self.tree.insert(x, self.counters)
#     def delete(self, x): self.counters.deletes += 1; self.tree.delete(x, self.counters)
#     def contains(self, x): self.counters.lookups += 1; return self.tree.contains(x, self.counters)
#
# ...where your BST implementation increments comparisons/node_visits/etc.
#
# Translation:
# - adapter increments the "high level" counters (insert/delete/lookup count)
# - the underlying structure increments the "inner work" counters (comparisons, structural_ops)
#
# That separation is nice because:
# - the harness can verify student code is doing roughly the right number of operations
# - the structure reports its internal effort honestly (lol) via comparisons/structural_ops
# ----------------------------