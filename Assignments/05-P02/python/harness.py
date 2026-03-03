from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Protocol, Dict, List, Tuple, Iterable, Optional
import random
import time
import statistics
import csv
from pathlib import Path


# ----------------------------
# 1) Instrumentation contract
# ----------------------------


@dataclass
class Counters:
    comparisons: int = 0
    structural_ops: int = 0
    inserts: int = 0
    deletes: int = 0
    lookups: int = 0
    resize_events: int = 0  # hash tables, etc.

    def snapshot(self) -> Dict[str, int]:
        return asdict(self)


class StructureAdapter(Protocol):
    """
    Students implement this adapter for each structure they test.
    The harness treats every structure uniformly.
    """

    def name(self) -> str: ...
    def reset(self) -> None: ...
    def reset_counters(self) -> None: ...
    def get_counters(self) -> Counters: ...

    def insert(self, x: int) -> None: ...
    def delete(self, x: int) -> None: ...
    def contains(self, x: int) -> bool: ...


# ----------------------------
# 2) Workload spec (locked)
# ----------------------------


@dataclass(frozen=True)
class WorkloadSpec:
    code: str  # "A", "B", "C", "D"
    n: int
    seed: int = 42
    value_range_mult: int = 10  # values in [0, value_range_mult * n]
    trials: int = 7


def _rng(spec: WorkloadSpec) -> random.Random:
    return random.Random(spec.seed)


def gen_values(spec: WorkloadSpec, count: int) -> List[int]:
    r = _rng(spec)
    hi = spec.value_range_mult * spec.n
    return [r.randrange(0, hi + 1) for _ in range(count)]


def workload_A(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    # Random insert N, then lookup N
    inserts = gen_values(spec, spec.n)
    lookups = gen_values(spec, spec.n)
    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts  # inserts returned as "population"


def workload_B(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    # Sorted insert N, then lookup N
    inserts = gen_values(spec, spec.n)
    inserts.sort()
    lookups = gen_values(spec, spec.n)
    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts


def workload_C(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    # 2N ops: 50% lookup, 25% insert, 25% delete; interleaved randomly.
    r = _rng(spec)
    hi = spec.value_range_mult * spec.n

    total_ops = 2 * spec.n
    counts = {
        "contains": total_ops // 2,
        "insert": total_ops // 4,
        "delete": total_ops - (total_ops // 2) - (total_ops // 4),  # remainder
    }

    # Generate operation types and shuffle
    op_types: List[str] = []
    for k, c in counts.items():
        op_types.extend([k] * c)
    r.shuffle(op_types)

    ops: List[Tuple[str, int]] = []
    population: List[int] = []

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
                y = population.pop()  # delete something known-in-structure-ish
                ops.append(("delete", y))
            else:
                # If empty, replace delete with lookup to keep op count constant
                ops.append(("contains", x))

    return ops, population


def workload_D(spec: WorkloadSpec) -> Tuple[List[Tuple[str, int]], List[int]]:
    # Insert N, then 5N lookups
    inserts = gen_values(spec, spec.n)
    lookups = gen_values(spec, 5 * spec.n)
    ops = [("insert", x) for x in inserts] + [("contains", x) for x in lookups]
    return ops, inserts


WORKLOADS = {
    "A": workload_A,
    "B": workload_B,
    "C": workload_C,
    "D": workload_D,
}


# ----------------------------
# 3) Runner + reporting
# ----------------------------


@dataclass
class TrialResult:
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
    adapter.reset()
    adapter.reset_counters()

    ops, _population = WORKLOADS[spec.code](spec)

    t0 = time.perf_counter()
    for op, x in ops:
        if op == "insert":
            adapter.insert(x)
        elif op == "delete":
            adapter.delete(x)
        else:
            adapter.contains(x)
    t1 = time.perf_counter()

    c = adapter.get_counters()
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
    Returns a 'median' row by taking median of each numeric field.
    The structure/workload/n fields are identical for all trials.
    """
    assert results, "No results"
    base = results[0]
    med = lambda xs: float(statistics.median(xs))

    return TrialResult(
        structure=base.structure,
        workload=base.workload,
        n=base.n,
        trial=-1,  # -1 indicates "median"
        seconds=med([r.seconds for r in results]),
        comparisons=int(med([r.comparisons for r in results])),
        structural_ops=int(med([r.structural_ops for r in results])),
        inserts=int(med([r.inserts for r in results])),
        deletes=int(med([r.deletes for r in results])),
        lookups=int(med([r.lookups for r in results])),
        resize_events=int(med([r.resize_events for r in results])),
    )


def write_csv(path: Path, rows: Iterable[TrialResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def run_suite(
    adapters: List[StructureAdapter], specs: List[WorkloadSpec], out_dir: Path
) -> None:
    raw_rows: List[TrialResult] = []
    med_rows: List[TrialResult] = []

    for adapter in adapters:
        for spec in specs:
            # Safety: optional cap for pathological BST sorted insert
            # You can enforce this in assignment text too.
            if (
                adapter.name().lower().startswith("bst")
                and spec.code == "B"
                and spec.n > 20000
            ):
                continue

            trial_rows = [run_one_trial(adapter, spec, i) for i in range(spec.trials)]
            raw_rows.extend(trial_rows)
            med_rows.append(median_of_trials(trial_rows))

    write_csv(out_dir / "raw_trials.csv", raw_rows)
    write_csv(out_dir / "median_summary.csv", med_rows)


# ----------------------------
# 4) Student extension points
# ----------------------------
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
# ----------------------------

