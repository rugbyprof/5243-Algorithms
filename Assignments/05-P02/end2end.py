from pathlib import Path

from python.workloads import WorkloadGenerator
from python.cppAdapter import CppRunnerAdapter
from python.cppAdapter import median_row

generator = WorkloadGenerator(seed=42)
adapter = CppRunnerAdapter("./runner", "BST")

N_values = [1000, 5000, 20000, 80000]
workloads = {
    "A": generator.workload_A,
    "B": generator.workload_B,
    "C": generator.workload_C,
    "D": generator.workload_D,
}

for code, fn in workloads.items():
    for N in N_values:
        if code == "B" and N > 20000:
            continue  # BST safety cap

        ops = fn(N)

        trials = [adapter.run_trial(ops, workload=code, n=N, trial=i) for i in range(7)]

        median = median_row(trials)
        print(median)
