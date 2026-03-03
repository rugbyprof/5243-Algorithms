#include <chrono>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "bst.hpp"
#include "counters.hpp"
#include "json.hpp"
#include "structure.hpp"

using json = nlohmann::json;

// struct Counters {
//     long long comparisons = 0;
//     long long structural_ops = 0;
//     long long inserts = 0;
//     long long deletes = 0;
//     long long lookups = 0;
//     long long resize_events = 0;
// };

// ------------------------------
// A tiny op representation
// ------------------------------ll

enum class OpType { Insert,
                    Delete,
                    Contains };

struct Op {
    OpType type;
    int value;
};

// class Structure {
// public:
//     virtual ~Structure() = default;
//     virtual const char *name() const = 0;

//     virtual void reset() = 0; // clear contents
//     virtual void reset_counters() = 0;
//     virtual Counters counters() const = 0;

//     virtual void insert(int x) = 0;
//     virtual void erase(int x) = 0;
//     virtual bool contains(int x) = 0;
// };

// ------------------------------
// Example stub: replace with real BST/Hash/etc.
// This just pretends to work.
// ------------------------------
// class StubBST final : public Structure {
//     Counters c_;

// public:
//     const char *name() const override { return "BST"; }
//     void reset() override { /* clear your DS */ }
//     void reset_counters() override { c_ = Counters{}; }
//     Counters counters() const override { return c_; }

//     void insert(int /*x*/) override {
//         c_.inserts++;
//         // increment these meaningfully in your real implementation:
//         c_.comparisons += 1;
//         c_.structural_ops += 1;
//     }

//     void erase(int /*x*/) override {
//         c_.deletes++;
//         c_.comparisons += 1;
//         c_.structural_ops += 1;
//     }

//     bool contains(int /*x*/) override {
//         c_.lookups++;
//         c_.comparisons += 1;
//         c_.structural_ops += 1;
//         return false;
//     }
// };

// ------------------------------
// Minimal CLI parsing
// ------------------------------
struct Args {
    std::string structure = "BST"; // choose which DS to run
    std::string workload = "A";
    int n = 0;
    int trial = 0;
};

Args parse_args(int argc, char **argv) {
    Args a;
    for (int i = 1; i < argc; i++) {
        std::string key = argv[i];
        auto get = [&](const std::string &def = "") -> std::string {
            if (i + 1 >= argc)
                return def;
            return argv[++i];
        };

        if (key == "--structure")
            a.structure = get(a.structure);
        else if (key == "--workload")
            a.workload = get(a.workload);
        else if (key == "--n")
            a.n = std::stoi(get("0"));
        else if (key == "--trial")
            a.trial = std::stoi(get("0"));
        // ignore unknown flags on purpose (keeps it flexible)
    }
    return a;
}

// ------------------------------
// Read stdin ops
// ------------------------------
std::vector<Op> read_ops_from_stdin() {
    std::vector<Op> ops;
    std::string line;
    ops.reserve(10000);

    while (std::getline(std::cin, line)) {
        if (line.empty())
            continue;

        std::istringstream iss(line);
        std::string op;
        int x;
        if (!(iss >> op >> x))
            continue;

        if (op == "insert")
            ops.push_back({OpType::Insert, x});
        else if (op == "delete")
            ops.push_back({OpType::Delete, x});
        else if (op == "contains")
            ops.push_back({OpType::Contains, x});
        // else ignore
    }
    return ops;
}

// ------------------------------
// Build the chosen structure
// Swap this factory to return your real implementations.
// ------------------------------
std::unique_ptr<Structure> make_structure(const std::string &which) {
    // TODO: return different implementations based on `which`
    // e.g. if (which=="HASH") return std::make_unique<HashTable>();
    // For now, only BST stub:
    (void)which;
    return std::make_unique<BST>();
}

// ------------------------------
// Emit ONE JSON line (machine-readable)
// ------------------------------
static void print_json_line_old(const Structure &s, const Args &a, double seconds) {
    Counters c = s.counters();

    // One line. No extra prints. No pretty formatting.
    std::cout
        << "{"
        << "\"structure\":\"" << s.name() << "\","
        << "\"workload\":\"" << a.workload << "\","
        << "\"n\":" << a.n << ","
        << "\"trial\":" << a.trial << ","
        << "\"seconds\":" << seconds << ","
        << "\"comparisons\":" << c.comparisons << ","
        << "\"structural_ops\":" << c.structural_ops << ","
        << "\"inserts\":" << c.inserts << ","
        << "\"deletes\":" << c.deletes << ","
        << "\"lookups\":" << c.lookups << ","
        << "\"resize_events\":" << c.resize_events
        << "}\n";
}

static void print_json_line(const Structure &s, const Args &a, double seconds) {
    Counters c = s.counters();

    json j = {
        {"structure", s.name()},
        {"workload", a.workload},
        {"n", a.n},
        {"trial", a.trial},
        {"seconds", seconds},
        {"comparisons", c.comparisons},
        {"structural_ops", c.structural_ops},
        {"inserts", c.inserts},
        {"deletes", c.deletes},
        {"lookups", c.lookups},
        {"resize_events", c.resize_events}};

    std::cout << j.dump() << "\n";
}

int main(int argc, char **argv) {
    Args args = parse_args(argc, argv);

    auto structure = make_structure(args.structure);

    // Read workload from stdin
    std::vector<Op> ops = read_ops_from_stdin();

    structure->reset();
    structure->reset_counters();

    auto t0 = std::chrono::steady_clock::now();

    for (const auto &op : ops) {
        switch (op.type) {
        case OpType::Insert:
            structure->insert(op.value);
            break;
        case OpType::Delete:
            structure->erase(op.value);
            break;
        case OpType::Contains:
            (void)structure->contains(op.value);
            break;
        }
    }

    auto t1 = std::chrono::steady_clock::now();
    std::chrono::duration<double> dt = t1 - t0;

    print_json_line(*structure, args, dt.count());
    return 0;
}