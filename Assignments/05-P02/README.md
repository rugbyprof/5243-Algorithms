```yaml
id: 05-P02
course: 5243 Algorithms
category: program
title: "Experimental Comparison of Core Data Structures"
date_assigned: 2026-03-03 12:00
date_due: 2026-03-24 15:30
format:
  - code_submission
  - results_csv_files
  - written_report_pdf
primary_goal: "Design controlled experiments and analyze structural behavior"
secondary_goal: "Develop reproducible benchmarking discipline"
```

# 📦 Program 2
# Experimental Comparison of Core Data Structures

## Overview

- In this assignment, you will conduct controlled experiments comparing core data structures under standardized workloads.

- This is not a proof assignment.

- This is not a reimplementation assignment.

- This is an **experimental analysis assignment**. You will:

  - Instrument provided implementations
  - Run standardized workloads
  - Collect structural metrics
  - Analyze scaling behavior
  - Draw engineering conclusions

This assignment emphasizes experimental discipline that is used in graduate courses.

---

# 🎯 Learning Objectives

By completing this assignment, you will:

1. Empirically validate theoretical complexity.
2. Observe worst-case vs average-case behavior.
3. Understand how workload affects performance.
4. Develop reproducible benchmarking methodology.
5. Practice structured algorithmic reasoning.

---

# 🧱 Structures Included

You will be provided implementations of:

- Dynamic Array
- Linked List
- Unbalanced Binary Search Tree (BST)
- Binary Heap
- Hash Table (specify collision method)

You may modify these implementations **only to add instrumentation**.

You may not redesign them.

---

# 🧪 Experimental Architecture

You will use:

- A standardized **Python workload generator**
- A C++ `runner` executable that:
  - Reads operations from stdin
  - Executes one workload trial
  - Outputs exactly one JSON summary line
- The Python harness will:
  - Generate workloads
  - Execute 7 trials
  - Compute medians
  - Write CSV results

You may not modify workload definitions or random seed.


START

---
# 📊 Required Results & Reporting Format

All groups must use the same reporting structure to ensure comparability.

---

# 🔁 Standardized Workload Generator Specification

To ensure fairness across experiments, all students must use the following workload rules.

## Randomness

- Use a **fixed RNG seed = 42** (this means everyone seeds the RNG with 42)
- Use uniform distribution for random values
- Value range: integers in `[0, 10N]`

This avoids:
- accidental duplicates dominating behavior
- adversarial patterns unless explicitly required

---

## Workload Definitions (Formalized)

### Workload A — Random Insert + Random Lookup

1. Generate N random integers.
2. Values drawn uniformly from `[0, 10N]`
3. Insert all N random integers.
4. Perform N random lookups (values drawn from same range).

---

### Workload B — Sorted Insert

1. Generate N random integers.
2. Sort them ascending.
3. Insert in sorted order.
4. Perform N random lookups.

BST degradation must be observable here.

>Note: BST tests capped at N ≤ 20,000[^1].


---

### Workload C — Mixed Operations

Start with empty structure.

Perform 2*N total operations:

- 50% lookup
- 25% insert
- 25% delete

- Important: 
  - Operations must be `randomly interleaved`.
  - Delete only if structure not empty.

### Workload D — Lookup Heavy

1. Insert N random values (integers)
2. Perform 5N `random lookups` [^2]

---

# 📏 Required Input Sizes

You must test at least 4 sizes:

- N = 1,000  
- N = 5,000  
- N = 20,000  
- N = 80,000  

Exception:
- For Sorted Insert (Workload B), cap N at **20,000** for BST.

If a workload exceeds 10 seconds per run, stop increasing N and report the maximum feasible size.

# 🔢 Required Repetitions

For each (Structure, Workload, N):

- Run **7 trials**
- Report the **median**
- You may optionally include min/max

---

# 🧮 Instrumentation Contract

Each structure must track:

### Required Counters

All structures must report (counters):

- `comparisons`
- `structural_ops`
- `inserts`
- `deletes`
- `lookups`
- `resize_events`

Operation totals must match workload definitions.

### Structure-Specific Counters

`Hash table:`
- probe count (open addressing) OR
- chain traversal count (chaining)
- resize events

`BST:`
- node visits

`Heap:`
- swaps
- heapify steps

`Linked List:`
- node traversals

You must clearly define what each counter represents.

---

# 📋 Required Results Tables

## Table 1 — Structural Metrics Summary

For each workload and N:

| Structure | N   | Comparisons | Structural Ops | Resize Events | Median Time (optional) |
| --------- | --- | ----------- | -------------- | ------------- | ---------------------- |

One table per workload.

---

## Table 2 — Scaling Trend Table

For each structure under Workload A:

| N   | Comparisons | Comparisons / N | Comparisons / (N log N) |
| --- | ----------- | --------------- | ----------------------- |

This forces you to examine growth trends, not just raw numbers.

---

# 📈 Required Plots

You must include:

### Plot 1 — Comparisons vs N (per workload)

- X-axis: N
- Y-axis: comparisons
- One line per structure

---

### Plot 2 — Structural Ops vs N

Same structure as above.

---

### Optional Plot — Time vs N

Only if timing is included.

Median values only.

---

# 📝 Required Analysis Structure

Your report must follow this order:

---

## 1. Experimental Design

- How workloads were implemented
- What counters mean
- Why N values were chosen

---

## 2. Scaling Observations

Discuss:

- Which structures scale linearly?
- Which appear logarithmic?
- Which degrade under sorted insert?
- Does the empirical data match theoretical expectations?

---

## 3. Structural Tradeoff Analysis

For each structure:

- Strengths
- Weaknesses
- Ideal use case

---

## 4. Engineering Decision Framework

Answer:

If building:
- A dictionary
- A scheduler
- A database index
- A logging system

Which structure and why?

You must justify using experimental evidence.

---

# 🚫 Common Mistakes (Preemptive Strike Section)

You will lose points if:

- You only report time.
- You do not define counters clearly.
- You do not control randomness.
- You do not repeat trials.
- Your analysis merely restates tables without interpretation.

---

# 🎯 Why This Matters

This assignment is not about proving asymptotics.

It is about:

- validating theory experimentally
- understanding structure behavior
- thinking like an engineer
---

END

---



# 📊 Required Counters



---

# 📐 Counter Definitions Standard

## Comparisons

Count one comparison whenever you evaluate a key relation:

- `<`, `>`, `<=`, `>=`, `==`, `!=` between keys

Do not count loop bounds or null checks.

---

## Structural Operations

Count meaningful structural work beyond comparisons.

### Dynamic Array
- Element shift: +1 per element moved
- Resize copy: +1 per element copied
- Resize event: increment `resize_events`

### Linked List
- Node traversal: +1 per node visited

### BST
- Node visit: +1 structural_op
- Key comparison at node: +1 comparison
- Pointer reassignment during delete: +1 structural_op

### Binary Heap
- Key comparison during percolation: +1 comparison
- Swap: +1 structural_op

### Hash Table

Chaining:
- Node visited in chain: +1 structural_op
- Key equality check: +1 comparison

Open Addressing:
- Slot probe: +1 structural_op
- Key equality check: +1 comparison
- Resize/rehash: increment `resize_events`

You must clearly document your counting policy in your report.

---

# 📋 Required Tables

## Table 1 — Structural Metrics Summary (per workload)

| Structure | N   | Comparisons | Structural Ops | Resize Events | Median Time |
| --------- | --- | ----------- | -------------- | ------------- | ----------- |

One table per workload.

---

## Table 2 — Scaling Trend (Workload A)

| N   | Comparisons | Comparisons / N | Comparisons / (N log N) |
| --- | ----------- | --------------- | ----------------------- |

Interpret trends.

---

# 📈 Required Plots

1. Comparisons vs N (per workload)
2. Structural Ops vs N
3. Optional: Time vs N (median only)

All plots must be labeled clearly.

---

# 📝 Required Written Report (3–5 pages)

## 1. Experimental Design
- Workload explanation
- Counter definitions
- Rationale for chosen N values

## 2. Results
- Tables and graphs
- Brief summary per workload

## 3. Scaling Analysis
Discuss:

- Which structures scale linearly?
- Which scale logarithmically?
- Which degrade under sorted input?
- Does empirical behavior match theory?

## 4. Structural Tradeoffs

For each structure:
- Strengths
- Weaknesses
- Ideal use cases

## 5. Engineering Decisions

If building:
- A dictionary
- A priority scheduler
- A database index
- A logging system

Which structure would you choose and why?

Justify with experimental evidence.

---

# 🚫 Common Mistakes (Avoid These)

You will lose points if:

- You only report time.
- You modify workload definitions.
- You change the seed.
- You do not repeat trials.
- Your analysis merely restates tables.
- Counters are inconsistent or undefined.

---

# 📦 Submission Requirements

Submit:

1. C++ runner executable (or source + build instructions)
2. Python harness
3. CSV results files
4. Written PDF report

---

# 📏 Grading Rubric

| Category                | Weight |
| ----------------------- | ------ |
| Correct instrumentation | 25%    |
| Experimental rigor      | 25%    |
| Analysis quality        | 30%    |
| Clarity & organization  | 20%    |

---


## Directory Structure

```txt
Program_2/
│
├── README.md                    ← Assignment spec (the final polished one)
│
├── python/
│   ├── harness.py               ← Main experimental driver
│   ├── workloads.py             ← WorkloadGenerator (A–D)
│   └── cpp_adapter.py           ← Subprocess wrapper for C++ runner
│
├── cpp/
│   ├── runner.cpp               ← C++ runner (stdin → JSON line)
│   ├── counters.hpp             ← Counters struct
│   ├── structure.hpp            ← Base Structure interface
│   │
│   ├── bst.hpp                  ← BST implementation (instrumented)
│   ├── heap.hpp                 ← Heap implementation (instrumented)
│   ├── hash.hpp                 ← Hash table implementation (instrumented)
│   ├── array.hpp                ← Dynamic array
│   └── list.hpp                 ← Linked list
│
├── build.sh                     ← Simple compile script
│
└── results/
    └── (generated CSVs go here)
```



# ✅ What Should Exist in the `Program_1/` Folder

Nothing more than this:

```
Program_1/
│
├── README.md                    ← Assignment spec (this file)
│
├── python/
│   ├── harness.py               ← Main experimental driver
│   ├── workloads.py             ← WorkloadGenerator (A–D)
│   └── cpp_adapter.py           ← Subprocess wrapper for C++ runner
│
├── cpp/
│   ├── runner.cpp               ← C++ runner (stdin → JSON line)
│   ├── counters.hpp             ← Counters struct
│   ├── structure.hpp            ← Base Structure interface
│   │
│   ├── bst.hpp                  ← BST implementation (instrumented)
│   ├── heap.hpp                 ← Heap implementation (instrumented)
│   ├── hash.hpp                 ← Hash table implementation (instrumented)
│   ├── array.hpp                ← Dynamic array
│   └── list.hpp                 ← Linked list
│
├── build.sh                     ← Simple compile script
│
└── results/
    └── (generated CSVs go here)
```
---

# 🎯 What Each File Does

## `python/harness.py`

- Loops over:
  - workloads
  - N values
  - structures
- Runs 7 trials
- Computes median
- Writes CSV

This is your orchestration brain.

## `python/workloads.py`

Contains:
- `WorkloadGenerator`
- A/B/C/D definitions
- Seed fixed at 42

This guarantees identical experiments.

## `python/cpp_adapter.py`

- Calls `./runner`
- Sends workload via stdin
- Parses single JSON line
- Returns structured result

No logic beyond subprocess + JSON parsing.

## `cpp/runner.cpp`

- Parses CLI args
- Reads operations from stdin
- Executes them
- Prints exactly one JSON line
- Exits

No workload generation inside C++.

## `cpp/counters.hpp`

Just:

```cpp
struct Counters {
    long long comparisons = 0;
    long long structural_ops = 0;
    long long inserts = 0;
    long long deletes = 0;
    long long lookups = 0;
    long long resize_events = 0;
};
```

## `cpp/structure.hpp`

Defines:

```cpp
class Structure {
public:
    virtual ~Structure() = default;
    virtual const char* name() const = 0;

    virtual void reset() = 0;
    virtual void reset_counters() = 0;
    virtual Counters counters() const = 0;

    virtual void insert(int x) = 0;
    virtual void erase(int x) = 0;
    virtual bool contains(int x) = 0;
};
```

That keeps everything consistent.

---

## The actual structures (`bst.hpp`, etc.)

Each:
- Includes counters
- Increments properly
- Does not print anything
- Does not know about workloads
- Does not know about trials

They are pure structures.

---

## `build.sh`

Minimal:

```bash
#!/bin/bash
g++ -O2 -std=c++20 -Wall -Wextra -pedantic \
    cpp/runner.cpp -o runner
```

(You can expand later.)

---

# 🧠 What You Do NOT Need

You do NOT need:

- Multiple harness versions
- Multiple runner versions
- Profilers
- Per-structure Python code
- Multiple JSON formats
- Separate workload generators in C++

If you keep workload generation strictly in Python, you eliminate half the confusion.

---

# 🧩 Who Owns What?

| Component            | Owned By |
| -------------------- | -------- |
| Workload definitions | Python   |
| Trial repetition     | Python   |
| Median calculation   | Python   |
| Execution timing     | C++      |
| Structural counters  | C++      |
| CSV writing          | Python   |

That division is clean and stable.

---

# 🔥 Simplification Rule

If a file:

- prints debugging info to stdout  
- generates random numbers inside C++  
- knows about N values internally  
- runs multiple trials internally  

…it’s wrong.

The runner does one job:
> Read ops. Execute. Print metrics.

---

# 🎯 Final Sanity Check

If you can answer “yes” to these, your folder is correct:

- Does C++ generate random numbers? → **No**
- Does Python know about comparisons? → **No**
- Does C++ know about trials? → **No**
- Can I swap BST with Treap without touching Python? → **Yes**

If yes to all → you are clean.

---

When you get back later this week, we’ll do the exact same clarity pass for the Final Project.

For now: breathe. You’re organized again.

---


# 🎯 Final Note

This assignment is about understanding structure behavior.

Theory predicts trends.

Your job is to verify and interpret them.

Treat this as a controlled lab, not a timing contest.

[^1]: Limit on the number of values to be placed in the BST.
[^2]: A random lookup doesn't mean your searching with an existing number in the structure, random = might not be there

```yaml
id: algos-program1-counter-definitions-2026-03-03
course: 5243 Algorithms
assignment: Program_1
deliverable: counter_definition_standard
goal: consistent_metrics_across_groups_and_languages
counters:
  - comparisons
  - structural_ops
  - inserts
  - deletes
  - lookups
  - resize_events
includes:
  - global_rules
  - per_structure_rules
  - examples
  - audit_checks
```

Love it. This is exactly how you prevent “my comparisons are smaller because I counted less stuff” — aka *academic performance optimization*.

Below is a **drop-in “Counter Definitions Standard”** you can paste straight into Program 1. It defines what to count, how to count it, and includes sanity checks.

---

# Program 1 Counter Definitions Standard

## Counters you must report

All structures must report:

- `comparisons`
- `structural_ops`
- `inserts`
- `deletes`
- `lookups`
- `resize_events` (0 for structures that don’t resize)

**Rule:** `inserts + deletes + lookups` must match the workload’s operation totals (except when Workload C substitutes a delete with a lookup due to emptiness).

---

# Global counting rules

## What counts as a `comparison`
A **comparison** is counted when your code evaluates an **ordering/equality decision involving a key** that affects control flow.

Count **exactly one** comparison whenever you do one of these checks:

- `x < y`
- `x <= y`
- `x > y`
- `x >= y`
- `x == y`
- `x != y`

### Important clarifications
- **Do not** count loop conditions like `i < n` or pointer null checks as key comparisons.
- **Do** count comparisons against stored keys during search/insert/delete.
- If you do a combined check like:
  - `if (x < key) ... else if (x > key) ... else ...`
  then that can be **2 comparisons** in the “not equal” case.
  - (Because you actually evaluated two relational checks.)

## What counts as a `structural_op`
A structural operation is a **data-structure-specific “step”** that meaningfully reflects work beyond comparisons.

This is your catch-all for:
- pointer traversals
- swaps
- rotations
- probes
- node splits
- etc.

If you’re unsure whether something should be “comparison” or “structural_op”:
- if it’s a key relation test → `comparisons`
- if it’s a movement/rearrangement/traversal → `structural_ops`

---

# Per-structure definitions

## 1) Dynamic Array (vector-style)

### comparisons
- Only count key comparisons you explicitly do (many array ops won’t compare keys).
- If you implement a linear search, each `arr[i] == x` is **1 comparison**.

### structural_ops
Count:
- each element shift due to insert/delete in the middle: **+1 structural_op per element moved**
- each append is **+1 structural_op**
- each resize copy move is **+1 structural_op per element copied**
- optionally: treat resize as `resize_events += 1`

### resize_events
- Increment when capacity increases (and you reallocate/copy).

---

## 2) Linked List

### comparisons
Count:
- each `node.value == x` check during search/remove: **+1 comparison**

### structural_ops
Count:
- each node visited/advanced pointer step: **+1 structural_op**
  - i.e., when you move from one node to `next`

(Yes, comparisons and traversals will often rise together. That’s fine—this is reality.)

---

## 3) Unbalanced BST

### comparisons
Count:
- each comparison between `x` and `node.key` used to decide direction or equality:
  - `x < node.key` → +1
  - `x > node.key` → +1
  - `x == node.key` → +1 (if you explicitly check it)

**Standard pattern:**
```cpp
if (x < k) ...
else if (x > k) ...
else found
```
Counts:
- Found case (equal): 2 comparisons (x<k false, x>k false) *unless you explicitly do x==k*
- Left/right case: 1 comparison in the branch taken + possibly 1 more if using else-if logic

To avoid ambiguity, you may implement a helper `cmp(x, k)` that returns -1/0/1 and increments `comparisons` exactly once per node visited. That’s *ideal*.

### structural_ops
Count:
- each node visit during traversal: **+1 structural_op**
- pointer re-links when deleting (each pointer reassignment): **+1 structural_op**
- (No rotations in unbalanced BST.)

---

## 4) Binary Heap (array-based min-heap or max-heap)

### comparisons
Count:
- each comparison between heap keys during percolate up/down:
  - parent vs child comparisons

### structural_ops
Count:
- each swap of two heap elements: **+1 structural_op**
- each percolate step can also be counted as +1 structural_op if you prefer, but then be consistent.

**Recommendation (consistent & simple):**
- structural_ops = swaps
- comparisons = key comparisons
That’s very clean.

---

## 5) Hash Table

You must clearly state which collision strategy you use:
- **chaining**
- **open addressing**

### comparisons
Count:
- each key equality check `stored_key == x` during lookup/insert/delete: **+1 comparison**

### structural_ops (chaining)
Count:
- each node visited in a chain: **+1 structural_op**
  - (Yes, this will correlate strongly with comparisons; that’s expected.)

### structural_ops (open addressing)
Count:
- each probe attempt (each slot examined): **+1 structural_op**
- comparisons counts only when the slot is occupied and you compare keys.

### resize_events
Count:
- each rehash / resize operation: **+1 resize_events**
Optionally also add:
- structural_ops += number of elements reinserted during resize

(If you do that, document it. It’s actually a good reflection of cost.)

---

# Required documentation in your report (short)

You must include a short section:

## “Counter Definitions”
- One paragraph describing exactly what increments comparisons and structural_ops for each structure.

They can copy from this standard—encouraged, even.

---

# Sanity checks (you can add as “self-audit”)

You must verify:

1. **Workload totals match**
   - inserts + deletes + lookups equals number of operations executed.

2. **Counters grow with N**
   - comparisons and structural_ops should generally increase as N increases.

3. **BST sorted insert blows up**
   - Workload B should show BST scaling much worse than random insert.

4. **Heap lookup is painful (if they attempt it)**
   - if they implement contains on heap by scan, comparisons scale ~N.

---

# Lastly

I need you to write a validation function

- `validate_counters()` that prints:
  - operations executed
  - counters summary
  - and asserts totals are consistent

That prevents oops I forgot to increment something” disasters.


## Deliverables

coming soon.

