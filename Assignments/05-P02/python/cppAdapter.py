from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import subprocess
import json
import statistics
import time

# Same Op list format the harness produces:
# ops = [("insert", 123), ("contains", 456), ...]
Op = Tuple[str, int]


@dataclass
class TrialRow:
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


class CppRunnerAdapter:
    """
    A thin adapter that:
      - takes ops generated in Python
      - sends them to the C++ runner via stdin
      - parses exactly one JSON line from stdout
    """

    def __init__(self, exe_path: str, structure_flag: str):
        self.exe_path = exe_path
        self.structure_flag = structure_flag  # e.g. "BST", "HASH", etc.

    def run_trial(self, ops: List[Op], workload: str, n: int, trial: int) -> TrialRow:
        payload = "\n".join(f"{op} {val}" for op, val in ops) + "\n"

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

        proc = subprocess.run(
            cmd,
            input=payload.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if proc.returncode != 0:
            raise RuntimeError(
                f"C++ runner failed (code={proc.returncode}).\n"
                f"stderr:\n{proc.stderr.decode('utf-8', errors='replace')}"
            )

        out = proc.stdout.decode("utf-8", errors="replace").strip()
        # enforce ONE line JSON
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if len(lines) != 1:
            raise RuntimeError(f"Expected 1 JSON line, got {len(lines)} lines:\n{out}")

        data: Dict[str, Any] = json.loads(lines[0])

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
    assert rows
    base = rows[0]
    medf = lambda xs: statistics.median(xs)
    return TrialRow(
        structure=base.structure,
        workload=base.workload,
        n=base.n,
        trial=-1,
        seconds=float(medf([r.seconds for r in rows])),
        comparisons=int(medf([r.comparisons for r in rows])),
        structural_ops=int(medf([r.structural_ops for r in rows])),
        inserts=int(medf([r.inserts for r in rows])),
        deletes=int(medf([r.deletes for r in rows])),
        lookups=int(medf([r.lookups for r in rows])),
        resize_events=int(medf([r.resize_events for r in rows])),
    )
