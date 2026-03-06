#include <algorithm>
#include <functional>
#include <iostream>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include "json.hpp"

using json = nlohmann::json;

// -------------------------------------------------------------
// Operation type
// -------------------------------------------------------------
struct Op {
    std::string op;
    int value;
};

// Convert Op -> JSON automatically
void to_json(json &j, const Op &o) {
    j = json{{"op", o.op}, {"value", o.value}};
}

// -------------------------------------------------------------
// WorkloadGenerator
// -------------------------------------------------------------
class WorkloadGenerator {
private:
    int seed;
    int valueRangeMult;

    // Same design as your Python version:
    // each helper call gets a fresh RNG with the same seed
    // so repeated calls are reproducible.
    std::mt19937 rng() const {
        return std::mt19937(seed);
    }

    std::vector<int> genValues(int n, int count) const {
        std::mt19937 r = rng();
        int hi = valueRangeMult * n;
        std::uniform_int_distribution<int> dist(0, hi);

        std::vector<int> values;
        values.reserve(count);

        for (int i = 0; i < count; i++) {
            values.push_back(dist(r));
        }

        return values;
    }

public:
    WorkloadGenerator(int seed_ = 42, int valueRangeMult_ = 10)
        : seed(seed_), valueRangeMult(valueRangeMult_) {}

    std::vector<Op> workloadA(int n) const {
        auto inserts = genValues(n, n);
        auto lookups = genValues(n, n);

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x});
        }
        for (int x : lookups) {
            ops.push_back({"contains", x});
        }

        return ops;
    }

    std::vector<Op> workloadB(int n) const {
        auto inserts = genValues(n, n);
        std::sort(inserts.begin(), inserts.end());

        auto lookups = genValues(n, n);

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x});
        }
        for (int x : lookups) {
            ops.push_back({"contains", x});
        }

        return ops;
    }

    std::vector<Op> workloadC(int n) const {
        std::mt19937 r = rng();
        int hi = valueRangeMult * n;
        std::uniform_int_distribution<int> dist(0, hi);

        int totalOps = 2 * n;
        int numContains = totalOps / 2;
        int numInsert = totalOps / 4;
        int numDelete = totalOps - numContains - numInsert;

        std::vector<std::string> opTypes;
        opTypes.reserve(totalOps);

        opTypes.insert(opTypes.end(), numContains, "contains");
        opTypes.insert(opTypes.end(), numInsert, "insert");
        opTypes.insert(opTypes.end(), numDelete, "delete");

        std::shuffle(opTypes.begin(), opTypes.end(), r);

        std::vector<Op> ops;
        ops.reserve(totalOps);

        std::vector<int> population;

        for (const auto &op : opTypes) {
            int x = dist(r);

            if (op == "insert") {
                population.push_back(x);
                ops.push_back({"insert", x});
            } else if (op == "contains") {
                ops.push_back({"contains", x});
            } else { // delete
                if (!population.empty()) {
                    int y = population.back();
                    population.pop_back();
                    ops.push_back({"delete", y});
                } else {
                    ops.push_back({"contains", x});
                }
            }
        }

        return ops;
    }

    std::vector<Op> workloadD(int n) const {
        auto inserts = genValues(n, n);
        auto lookups = genValues(n, 5 * n);

        std::vector<Op> ops;
        ops.reserve(6 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x});
        }
        for (int x : lookups) {
            ops.push_back({"contains", x});
        }

        return ops;
    }
};

// -------------------------------------------------------------
// Tiny command-line parser
// -------------------------------------------------------------
struct Args {
    std::string workload = "A";
    int size = 10;
    int preview = 20;
    bool emitJson = false;
};

Args parseArgs(int argc, char *argv[]) {
    Args args;

    for (int i = 1; i < argc; i++) {
        std::string s = argv[i];

        if ((s == "-w" || s == "--workload") && i + 1 < argc) {
            args.workload = argv[++i];
        } else if ((s == "-n" || s == "--size") && i + 1 < argc) {
            args.size = std::stoi(argv[++i]);
        } else if (s == "--preview" && i + 1 < argc) {
            args.preview = std::stoi(argv[++i]);
        } else if (s == "--json") {
            args.emitJson = true;
        } else if (s == "-h" || s == "--help") {
            std::cout
                << "Usage:\n"
                << "  ./workload_generator [-w A|B|C|D] [-n SIZE] [--preview K] [--json]\n\n"
                << "Options:\n"
                << "  -w, --workload   Workload type (A, B, C, D)\n"
                << "  -n, --size       Base problem size n\n"
                << "  --preview        Number of operations to preview\n"
                << "  --json           Print all operations as JSON\n";
            std::exit(0);
        }
    }

    return args;
}

// -------------------------------------------------------------
// main
// -------------------------------------------------------------
int main(int argc, char *argv[]) {
    Args args = parseArgs(argc, argv);

    WorkloadGenerator gen(42);

    std::unordered_map<std::string, std::function<std::vector<Op>(int)>> workloads = {
        {"A", [&](int n) { return gen.workloadA(n); }},
        {"B", [&](int n) { return gen.workloadB(n); }},
        {"C", [&](int n) { return gen.workloadC(n); }},
        {"D", [&](int n) { return gen.workloadD(n); }}};

    // The "contains" method isn't available until c++ 20
    if (!workloads.contains(args.workload)) {
        std::cerr << "Error: workload must be one of A, B, C, D\n";
        return 1;
    }

    auto ops = workloads[args.workload](args.size);

    if (args.emitJson) {
        json j = ops;
        std::cout << j.dump(2) << "\n";
        return 0;
    }

    std::cout << "\n----------------------------------\n";
    std::cout << "Workload: " << args.workload << "\n";
    std::cout << "n: " << args.size << "\n";
    std::cout << "Total operations: " << ops.size() << "\n";
    std::cout << "----------------------------------\n\n";

    int preview = std::min<int>(args.preview, static_cast<int>(ops.size()));

    for (int i = 0; i < preview; i++) {
        json j = ops[i];
        std::cout << j.dump() << "\n";
    }

    if (preview < static_cast<int>(ops.size())) {
        std::cout << "...\n";
    }

    return 0;
}