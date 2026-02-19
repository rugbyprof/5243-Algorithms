#!/usr/bin/env python3
"""
bench_containers.py

Grad-level benchmarking harness to compare runtimes + container choices for:
- stacks/queues (array/list, deque, linked list)
- binary search (array vs linked list reality)
- BST (balanced-ish vs degenerate)
- priority queues (sorted linked list vs heap)
- heapify (O(n) build vs n inserts)
- graphs (adjacency list vs adjacency matrix BFS/DFS)

Notes:
- This is a microbenchmark. We try to reduce noise, but Python isn't a lab-grade timer.
- Still excellent for relative comparisons + design tradeoffs discussions.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics as stats
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple


# ---------------------------
# Timing utilities
# ---------------------------


@dataclass
class TrialResult:
    name: str
    n: int
    seconds: float
    meta: str = ""


def time_it(fn: Callable[[], None], repeats: int = 7) -> Tuple[float, float, float]:
    """
    Run fn multiple times and return (min, median, stdev) seconds.
    We use perf_counter (high resolution) and repeat to smooth noise.
    """
    samples: List[float] = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        samples.append(t1 - t0)
    return (
        min(samples),
        stats.median(samples),
        (stats.pstdev(samples) if len(samples) > 1 else 0.0),
    )


def fmt_sec(x: float) -> str:
    if x < 1e-6:
        return f"{x*1e9:.2f} ns"
    if x < 1e-3:
        return f"{x*1e6:.2f} µs"
    if x < 1:
        return f"{x*1e3:.2f} ms"
    return f"{x:.3f} s"


def print_table(rows: List[Dict[str, str]], headers: List[str]) -> None:
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            widths[h] = max(widths[h], len(r.get(h, "")))

    sep = " | "
    line = "-+-".join("-" * widths[h] for h in headers)

    print(sep.join(h.ljust(widths[h]) for h in headers))
    print(line)
    for r in rows:
        print(sep.join(r.get(h, "").ljust(widths[h]) for h in headers))


# ---------------------------
# Linked list implementations
# ---------------------------


class LLNode:
    __slots__ = ("value", "next")

    def __init__(self, value: int, nxt: Optional["LLNode"] = None):
        self.value = value
        self.next = nxt


class LinkedListStack:
    """Stack with O(1) push/pop using head pointer."""

    __slots__ = ("head", "size")

    def __init__(self):
        self.head: Optional[LLNode] = None
        self.size = 0

    def push(self, x: int) -> None:
        self.head = LLNode(x, self.head)
        self.size += 1

    def pop(self) -> int:
        if not self.head:
            raise IndexError("pop from empty stack")
        v = self.head.value
        self.head = self.head.next
        self.size -= 1
        return v


class LinkedListQueue:
    """Queue with O(1) enqueue/dequeue using head+tail pointers."""

    __slots__ = ("head", "tail", "size")

    def __init__(self):
        self.head: Optional[LLNode] = None
        self.tail: Optional[LLNode] = None
        self.size = 0

    def enqueue(self, x: int) -> None:
        node = LLNode(x)
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def dequeue(self) -> int:
        if not self.head:
            raise IndexError("dequeue from empty queue")
        v = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return v


class SortedLinkedListPQ:
    """
    Priority queue via sorted linked list.
    We'll treat smaller value as higher priority (min-PQ) for comparison.
    - insert: O(n) scan
    - pop_min: O(1) remove head
    """

    __slots__ = ("head", "size")

    def __init__(self):
        self.head: Optional[LLNode] = None
        self.size = 0

    def push(self, x: int) -> None:
        if not self.head or x <= self.head.value:
            self.head = LLNode(x, self.head)
            self.size += 1
            return

        prev = self.head
        cur = self.head.next
        while cur and cur.value < x:
            prev = cur
            cur = cur.next
        prev.next = LLNode(x, cur)
        self.size += 1

    def pop_min(self) -> int:
        if not self.head:
            raise IndexError("pop from empty PQ")
        v = self.head.value
        self.head = self.head.next
        self.size -= 1
        return v


# ---------------------------
# Binary heap (min-heap) implementation
# ---------------------------


class BinaryHeap:
    """Min-heap implemented in an array (Python list)."""

    __slots__ = ("a",)

    def __init__(self, data: Optional[List[int]] = None):
        self.a: List[int] = []
        if data:
            self.a = data[:]  # copy
            self.heapify()

    def push(self, x: int) -> None:
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) // 2
            if a[p] <= a[i]:
                break
            a[p], a[i] = a[i], a[p]
            i = p

    def pop_min(self) -> int:
        a = self.a
        if not a:
            raise IndexError("pop from empty heap")
        v = a[0]
        last = a.pop()
        if a:
            a[0] = last
            self._sift_down(0)
        return v

    def _sift_down(self, i: int) -> None:
        a = self.a
        n = len(a)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i
            if l < n and a[l] < a[smallest]:
                smallest = l
            if r < n and a[r] < a[smallest]:
                smallest = r
            if smallest == i:
                return
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest

    def heapify(self) -> None:
        a = self.a
        # bottom-up heapify: O(n)
        for i in range((len(a) // 2) - 1, -1, -1):
            self._sift_down(i)


# ---------------------------
# BST (simple) + build modes
# ---------------------------


class BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: int):
        self.key = key
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class BST:
    """
    Unbalanced BST. Great for showing best vs worst-case.
    We'll build it in either random order (usually OK-ish) or sorted order (degenerate).
    """

    __slots__ = ("root",)

    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = BSTNode(key)
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key)
                    return
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = BSTNode(key)
                    return
                cur = cur.right
            else:
                return  # ignore duplicates for simplicity

    def search(self, key: int) -> bool:
        cur = self.root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return True
        return False


# ---------------------------
# Graph representations + BFS/DFS
# ---------------------------


def make_sparse_graph_adj_list(
    n: int, avg_deg: int, rng: random.Random
) -> List[List[int]]:
    """
    Undirected sparse graph adjacency list.
    We'll connect each node to avg_deg random neighbors (approx), avoiding self-loops.
    """
    g = [[] for _ in range(n)]
    # We'll add edges in a controlled count:
    edges_target = (n * avg_deg) // 2  # undirected
    seen = set()
    while len(seen) < edges_target:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        g[u].append(v)
        g[v].append(u)
    return g


def adj_list_to_matrix(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = [[0] * n for _ in range(n)]
    for u, nbrs in enumerate(g):
        for v in nbrs:
            m[u][v] = 1
    return m


def bfs_adj_list(g: List[List[int]], start: int = 0) -> int:
    n = len(g)
    vis = [False] * n
    q = deque([start])
    vis[start] = True
    count = 0
    while q:
        u = q.popleft()
        count += 1
        for v in g[u]:
            if not vis[v]:
                vis[v] = True
                q.append(v)
    return count


def dfs_adj_list_iter(g: List[List[int]], start: int = 0) -> int:
    n = len(g)
    vis = [False] * n
    st = [start]
    count = 0
    while st:
        u = st.pop()
        if vis[u]:
            continue
        vis[u] = True
        count += 1
        # push neighbors
        for v in g[u]:
            if not vis[v]:
                st.append(v)
    return count


def bfs_adj_matrix(m: List[List[int]], start: int = 0) -> int:
    n = len(m)
    vis = [False] * n
    q = deque([start])
    vis[start] = True
    count = 0
    while q:
        u = q.popleft()
        count += 1
        row = m[u]
        for v in range(n):
            if row[v] and not vis[v]:
                vis[v] = True
                q.append(v)
    return count


def dfs_adj_matrix_iter(m: List[List[int]], start: int = 0) -> int:
    n = len(m)
    vis = [False] * n
    st = [start]
    count = 0
    while st:
        u = st.pop()
        if vis[u]:
            continue
        vis[u] = True
        count += 1
        row = m[u]
        for v in range(n - 1, -1, -1):
            if row[v] and not vis[v]:
                st.append(v)
    return count


# ---------------------------
# Benchmark suites
# ---------------------------


def bench_stack_queue(n: int, repeats: int, rng: random.Random) -> List[Dict[str, str]]:
    data = [rng.randrange(10**9) for _ in range(n)]

    rows: List[Dict[str, str]] = []

    # Stack: Python list
    def stack_list():
        s = []
        for x in data:
            s.append(x)
        while s:
            s.pop()

    # Stack: linked list
    def stack_ll():
        s = LinkedListStack()
        for x in data:
            s.push(x)
        while s.size:
            s.pop()

    # Queue: deque
    def queue_deque():
        q = deque()
        for x in data:
            q.append(x)
        while q:
            q.popleft()

    # Queue: linked list
    def queue_ll():
        q = LinkedListQueue()
        for x in data:
            q.enqueue(x)
        while q.size:
            q.dequeue()

    # Queue: list (intentionally bad: pop(0))
    def queue_list_bad():
        q = []
        for x in data:
            q.append(x)
        while q:
            q.pop(0)

    for name, fn in [
        ("Stack (list)", stack_list),
        ("Stack (linked list)", stack_ll),
        ("Queue (deque)", queue_deque),
        ("Queue (linked list)", queue_ll),
        ("Queue (list) BAD pop(0)", queue_list_bad),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "Stacks/Queues",
                "n": str(n),
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )

    return rows


def bench_binary_search(
    n: int, probes: int, repeats: int, rng: random.Random
) -> List[Dict[str, str]]:
    # sorted array
    arr = sorted({rng.randrange(10**9) for _ in range(n)})
    # ensure size n (set might shrink)
    while len(arr) < n:
        arr.append(rng.randrange(10**9))
        arr = sorted(set(arr))
    arr = arr[:n]

    # linked list version of same data
    head = None
    for x in reversed(arr):
        head = LLNode(x, head)

    probe_vals = [arr[rng.randrange(n)] for _ in range(probes)]  # guaranteed hits

    def bin_search_array():
        # classic iterative binary search
        for target in probe_vals:
            lo, hi = 0, n - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                v = arr[mid]
                if v < target:
                    lo = mid + 1
                elif v > target:
                    hi = mid - 1
                else:
                    break

    def search_linked_list_linear():
        # "binary search on a linked list" is a trap: without random access, you end up doing linear work.
        for target in probe_vals:
            cur = head
            while cur and cur.value != target:
                cur = cur.next

    rows: List[Dict[str, str]] = []
    for name, fn in [
        ("Binary search (array)", bin_search_array),
        ("Search (linked list) linear reality", search_linked_list_linear),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "Binary Search",
                "n": f"{n} (probes={probes})",
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )
    return rows


def bench_bst(
    n: int, probes: int, repeats: int, rng: random.Random
) -> List[Dict[str, str]]:
    keys = list(range(n))
    # random insert order (typically OK-ish)
    rng.shuffle(keys)
    bst_rand = BST()
    for k in keys:
        bst_rand.insert(k)

    # sorted insert order (worst-case degenerate)
    bst_bad = BST()
    for k in range(n):
        bst_bad.insert(k)

    probe_vals = [rng.randrange(n) for _ in range(probes)]

    def search_rand_bst():
        for x in probe_vals:
            bst_rand.search(x)

    def search_bad_bst():
        for x in probe_vals:
            bst_bad.search(x)

    rows: List[Dict[str, str]] = []
    for name, fn in [
        ("BST search (random build)", search_rand_bst),
        ("BST search (degenerate build)", search_bad_bst),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "BST",
                "n": f"{n} (probes={probes})",
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )
    return rows


def bench_priority_queue(
    n: int, repeats: int, rng: random.Random
) -> List[Dict[str, str]]:
    data = [rng.randrange(10**9) for _ in range(n)]

    def pq_sorted_ll():
        pq = SortedLinkedListPQ()
        for x in data:
            pq.push(x)
        while pq.size:
            pq.pop_min()

    def pq_heap_push_pop():
        h = BinaryHeap()
        for x in data:
            h.push(x)
        while h.a:
            h.pop_min()

    def pq_heapify_then_pop():
        h = BinaryHeap(data)  # heapify inside
        while h.a:
            h.pop_min()

    rows: List[Dict[str, str]] = []
    for name, fn in [
        ("PQ (sorted linked list)", pq_sorted_ll),
        ("PQ (heap via push)", pq_heap_push_pop),
        ("PQ (heap via heapify)", pq_heapify_then_pop),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "Priority Queue",
                "n": str(n),
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )
    return rows


def bench_heapify_vs_inserts(
    n: int, repeats: int, rng: random.Random
) -> List[Dict[str, str]]:
    data = [rng.randrange(10**9) for _ in range(n)]

    def build_by_inserts():
        h = BinaryHeap()
        for x in data:
            h.push(x)

    def build_by_heapify():
        BinaryHeap(data)  # heapify inside

    rows: List[Dict[str, str]] = []
    for name, fn in [
        ("Build heap by n inserts (O(n log n))", build_by_inserts),
        ("Build heap by heapify (O(n))", build_by_heapify),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "Heap Build",
                "n": str(n),
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )
    return rows


def bench_graphs(
    n: int, avg_deg: int, repeats: int, rng: random.Random
) -> List[Dict[str, str]]:
    g = make_sparse_graph_adj_list(n, avg_deg=avg_deg, rng=rng)

    def bfs_list():
        bfs_adj_list(g, 0)

    def dfs_list():
        dfs_adj_list_iter(g, 0)

    # matrix is expensive; keep n moderate in CLI when testing matrix
    m = adj_list_to_matrix(g)

    def bfs_mat():
        bfs_adj_matrix(m, 0)

    def dfs_mat():
        dfs_adj_matrix_iter(m, 0)

    rows: List[Dict[str, str]] = []
    for name, fn in [
        ("BFS (adj list)", bfs_list),
        ("DFS (adj list)", dfs_list),
        ("BFS (adj matrix)", bfs_mat),
        ("DFS (adj matrix)", dfs_mat),
    ]:
        tmin, tmed, tsd = time_it(fn, repeats=repeats)
        rows.append(
            {
                "suite": "Graphs",
                "n": f"{n} (avg_deg={avg_deg})",
                "case": name,
                "min": fmt_sec(tmin),
                "med": fmt_sec(tmed),
                "stdev": fmt_sec(tsd),
            }
        )
    return rows


# ---------------------------
# Main runner
# ---------------------------


def run_all(args: argparse.Namespace) -> List[Dict[str, str]]:
    rng = random.Random(args.seed)

    all_rows: List[Dict[str, str]] = []

    # Stacks/Queues (can go larger)
    for n in args.n_values:
        all_rows.extend(bench_stack_queue(n, repeats=args.repeats, rng=rng))

    # Binary search
    for n in args.n_values:
        all_rows.extend(
            bench_binary_search(n, probes=args.probes, repeats=args.repeats, rng=rng)
        )

    # BST
    for n in args.n_values:
        all_rows.extend(bench_bst(n, probes=args.probes, repeats=args.repeats, rng=rng))

    # Priority queue
    for n in args.n_values:
        all_rows.extend(bench_priority_queue(n, repeats=args.repeats, rng=rng))

    # Heapify build
    for n in args.n_values:
        all_rows.extend(bench_heapify_vs_inserts(n, repeats=args.repeats, rng=rng))

    # Graphs: matrix is O(n^2) space, so clamp
    for n in args.graph_n_values:
        all_rows.extend(
            bench_graphs(n, avg_deg=args.avg_deg, repeats=args.repeats, rng=rng)
        )

    return all_rows


def write_csv(path: str, rows: List[Dict[str, str]], headers: List[str]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Benchmark container choices + algorithm runtimes for core DS/A topics."
    )
    p.add_argument(
        "--seed", type=int, default=1337, help="RNG seed for reproducibility"
    )
    p.add_argument("--repeats", type=int, default=7, help="Timing repeats per case")
    p.add_argument(
        "--probes",
        type=int,
        default=2000,
        help="Number of search probes for search suites",
    )
    p.add_argument(
        "--n-values",
        type=int,
        nargs="+",
        default=[2_000, 10_000, 50_000],
        help="List sizes for most suites",
    )
    p.add_argument(
        "--graph-n-values",
        type=int,
        nargs="+",
        default=[200, 400, 700],
        help="Graph sizes (keep moderate because adjacency matrix is O(n^2) memory)",
    )
    p.add_argument(
        "--avg-deg",
        type=int,
        default=6,
        help="Average degree for sparse graph generation",
    )
    p.add_argument("--csv", type=str, default="", help="Optional CSV output path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rows = run_all(args)

    headers = ["suite", "n", "case", "min", "med", "stdev"]
    # grouped pretty print
    suites = sorted(set(r["suite"] for r in rows))

    for s in suites:
        print("\n" + "=" * 80)
        print(f"{s}")
        print("=" * 80)
        sub = [r for r in rows if r["suite"] == s]
        print_table(sub, headers=headers)

    if args.csv:
        write_csv(args.csv, rows, headers=headers)
        print(f"\nWrote CSV: {args.csv}")


if __name__ == "__main__":
    main()
