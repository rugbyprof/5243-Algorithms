from __future__ import annotations
from typing import List, Tuple
import random

Op = Tuple[str, int]  # ("insert"|"delete"|"contains", value)


class WorkloadGenerator:
    """
    Standardized workload generator for Program 1.
    All randomness controlled by seed.
    """

    def __init__(self, seed: int = 42, value_range_mult: int = 10):
        self.seed = seed
        self.value_range_mult = value_range_mult

    def _rng(self) -> random.Random:
        return random.Random(self.seed)

    def _gen_values(self, n: int, count: int) -> List[int]:
        r = self._rng()
        hi = self.value_range_mult * n
        return [r.randrange(0, hi + 1) for _ in range(count)]

    # -----------------------------------
    # Workload A: Random Insert + Lookup
    # -----------------------------------
    def workload_A(self, n: int) -> List[Op]:
        inserts = self._gen_values(n, n)
        lookups = self._gen_values(n, n)

        ops: List[Op] = []
        ops += [("insert", x) for x in inserts]
        ops += [("contains", x) for x in lookups]
        return ops

    # -----------------------------------
    # Workload B: Sorted Insert
    # -----------------------------------
    def workload_B(self, n: int) -> List[Op]:
        inserts = self._gen_values(n, n)
        inserts.sort()
        lookups = self._gen_values(n, n)

        ops: List[Op] = []
        ops += [("insert", x) for x in inserts]
        ops += [("contains", x) for x in lookups]
        return ops

    # -----------------------------------
    # Workload C: Mixed Operations
    # -----------------------------------
    def workload_C(self, n: int) -> List[Op]:
        r = self._rng()
        hi = self.value_range_mult * n

        total_ops = 2 * n
        num_contains = total_ops // 2
        num_insert = total_ops // 4
        num_delete = total_ops - num_contains - num_insert

        op_types = (
            ["contains"] * num_contains
            + ["insert"] * num_insert
            + ["delete"] * num_delete
        )

        r.shuffle(op_types)

        ops: List[Op] = []
        population: List[int] = []

        for op in op_types:
            x = r.randrange(0, hi + 1)

            if op == "insert":
                population.append(x)
                ops.append(("insert", x))

            elif op == "contains":
                ops.append(("contains", x))

            else:  # delete
                if population:
                    # delete something we likely inserted
                    y = population.pop()
                    ops.append(("delete", y))
                else:
                    # if empty, substitute lookup
                    ops.append(("contains", x))

        return ops

    # -----------------------------------
    # Workload D: Lookup Heavy
    # -----------------------------------
    def workload_D(self, n: int) -> List[Op]:
        inserts = self._gen_values(n, n)
        lookups = self._gen_values(n, 5 * n)

        ops: List[Op] = []
        ops += [("insert", x) for x in inserts]
        ops += [("contains", x) for x in lookups]
        return ops
