from __future__ import annotations
# ^ Allows type hints to refer to classes/types defined later in the file
#   without quoting them. Mostly a “type-checker friendliness” thing.

from typing import List, Tuple
# ^ Type hints:
#   - List[T] = a list of T
#   - Tuple[A, B] = a pair (A, B)

import random
# ^ Used to generate reproducible random workloads (same seed => same ops)


# An "Op" is one benchmark step:
#   ("insert" | "delete" | "contains", value)
# Example:
#   ("insert", 17)   means: insert key 17
#   ("contains", 42) means: check if key 42 exists
#   ("delete", 9)    means: delete key 9
Op = Tuple[str, int]


class WorkloadGenerator:
    """
    This class generates standardized “workloads” for benchmarking data structures.

    A workload = a list of operations your structure must execute.
    These workloads are designed to stress different behaviors:

      A) Random build then query
      B) Sorted inserts (classic BST worst-case trap)
      C) Mixed inserts/deletes/lookups in random order (more “real life”)
      D) Read-heavy: many lookups after some inserts

    The big promise:
      All randomness is controlled by a seed, so results are repeatable.
      (Translation: your benchmark is not “vibes-based.”)
    """

    def __init__(self, seed: int = 42, value_range_mult: int = 10):
        """
        seed:
          Controls randomness. Same seed => same random numbers => same workload.
          This is crucial for fair comparisons between structures.

        value_range_mult:
          Controls how wide the key range is relative to n.

          Keys will be generated in:
            [0, value_range_mult * n]

          If value_range_mult is small, you get more repeated values
          (duplicates / collisions are more likely).
          If it's large, values spread out more.
        """
        self.seed = seed
        self.value_range_mult = value_range_mult

    def _rng(self) -> random.Random:
        """
        Create a fresh Random generator seeded with self.seed.

        Why “fresh” each time?
        - It makes generation deterministic based only on seed.
        - Downside: multiple calls produce the same sequence again.
          That’s not necessarily bad, but it means inserts and lookups can be identical
          sequences if you call _gen_values twice (more on that below).
        """
        return random.Random(self.seed)

    def _gen_values(self, n: int, count: int) -> List[int]:
        """
        Generate `count` random integers in a range scaled by n.

        hi = value_range_mult * n
        values are generated in [0, hi] inclusive.

        Example:
          n = 1000, value_range_mult = 10 -> values in [0..10000]
        """
        r = self._rng()
        hi = self.value_range_mult * n
        return [r.randrange(0, hi + 1) for _ in range(count)]
        # randrange(0, hi+1) -> includes hi (since upper bound is exclusive)

    # -----------------------------------
    # Workload A: Random Insert + Lookup
    # -----------------------------------
    def workload_A(self, n: int) -> List[Op]:
        """
        Workload A:
          1) Insert N random values
          2) Perform N contains() lookups of random values

        Purpose:
          Simulates a common pattern:
            “build the structure, then query it”

        Note:
          Because _gen_values uses a freshly seeded RNG each call,
          inserts and lookups will be the SAME sequence here (same seed, same count).
          That means lookups are heavily biased toward successful hits.
          This might be intentional (testing hit-heavy lookup performance) or accidental.
        """
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
        """
        Workload B:
          1) Insert N values, but SORTED (ascending)
          2) Perform N lookups

        Purpose:
          This is the “BST bully” workload:
            - A naive (unbalanced) BST inserting sorted keys degenerates into a linked list
              -> operations can become O(n) each (bad)
            - Balanced trees should handle this fine (AVL/Red-Black/Treap, etc.)

        Again, same caveat:
          inserts and lookups are generated using the same seed, so the lookup list
          will match the original random list (but inserts were sorted).
          Lookups still tend to hit often.
        """
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
        """
        Workload C:
          Total operations = 2N, randomly interleaved:
            - 50% contains
            - 25% insert
            - 25% delete (with guardrails)

        Purpose:
          Models a more realistic workload where reads and writes are mixed together.

        Important safety behavior:
          We avoid deleting from an empty structure:
            - If population (inserted items) is empty, a delete is replaced with a lookup
            - This keeps the total number of ops constant (still 2N)
        """
        r = self._rng()
        # ^ Here we keep one RNG instance and use it throughout, so the shuffle
        #   and the generated x values are part of one consistent random stream.

        hi = self.value_range_mult * n

        total_ops = 2 * n
        num_contains = total_ops // 2
        num_insert = total_ops // 4
        num_delete = total_ops - num_contains - num_insert
        # ^ Delete count uses the remainder so totals always add to 2N.

        # Build a list of operation names with the correct proportions.
        op_types = (
            ["contains"] * num_contains
            + ["insert"] * num_insert
            + ["delete"] * num_delete
        )

        # Shuffle them to randomize the order of operations.
        r.shuffle(op_types)

        ops: List[Op] = []
        population: List[int] = []
        # ^ population tracks inserted values that haven't been deleted yet.
        #   It's a simple way to choose delete targets that are likely to exist.

        for op in op_types:
            # Choose a random value for this step (used for insert or contains,
            # and sometimes used when we substitute a contains for a delete).
            x = r.randrange(0, hi + 1)

            if op == "insert":
                population.append(x)
                ops.append(("insert", x))

            elif op == "contains":
                ops.append(("contains", x))

            else:  # delete
                if population:
                    # Delete something we “probably inserted”
                    #
                    # Note: population.pop() removes the most recently inserted item.
                    # This creates a LIFO delete pattern (stack-ish), not uniformly random.
                    # For benchmarking, it's usually fine, but it's a bias worth knowing.
                    y = population.pop()
                    ops.append(("delete", y))
                else:
                    # If we can’t delete (empty), substitute a lookup so we don’t
                    # change the total number of operations.
                    ops.append(("contains", x))

        return ops

    # -----------------------------------
    # Workload D: Lookup Heavy
    # -----------------------------------
    def workload_D(self, n: int) -> List[Op]:
        """
        Workload D:
          1) Insert N
          2) Perform 5N lookups

        Purpose:
          Stress test lookup/contains performance in a read-heavy scenario,
          which is common in real systems (many reads, fewer writes).

        Same caveat as A/B:
          inserts and lookups come from the same seeded generator call pattern,
          so the first N lookups may match inserted values exactly (hit-heavy).
        """
        inserts = self._gen_values(n, n)
        lookups = self._gen_values(n, 5 * n)

        ops: List[Op] = []
        ops += [("insert", x) for x in inserts]
        ops += [("contains", x) for x in lookups]
        return ops