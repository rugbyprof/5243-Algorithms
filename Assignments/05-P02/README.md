## The Answer to Everything (42)

There are implementations for:
- Binary Heap
- Binary Search Tree
- Hash Table
- Linked List
- Ordered Dynamic Array

with all necessary basic funcionality and small tests to show how to use them. There is no additional code added to count any of the stats we want to collect for comparing different data structures and how they handle certain types of behaviors. 


---------------------------------------------------------
### Workload A

- Random inserts followed by random lookups

- Pattern:
```
     insert
     insert
     insert
     ...
     contains
     contains
```


---------------------------------------------------------
### Workload B


- Same as workload A except **inserts are sorted first**
- This often stresses ordered data structures differently 
- Example:  BSTs without balancing


---------------------------------------------------------
### Workload C

- Mixed workload with random ordering of operations.

- Operation mix:
  - 50% contains
  - 25% insert
  - 25% delete

- Deletes only occur if something exists in the population.


---------------------------------------------------------
### Workload D

- Insert n items then perform heavy lookup activity.

- Pattern:
   - n inserts
   - 5n lookups
- Useful for read-heavy workloads.

---

## Tracked Items

The following is a list with descriptions for all the stats we are tracking (aka counting)

### Comparisons
A **comparison** occurs whenever two values are evaluated relative to one another (e.g., `<`, `>`, or `==`).  
Comparisons are the fundamental operations that drive decision-making in most data structures. For example, a binary search tree uses comparisons to determine whether to traverse left or right, and a sorted array uses comparisons during binary search. Tracking comparisons helps reveal how efficiently a structure locates elements as the data size grows.

---

### Structural Operations
A **structural operation** is any action that modifies the internal organization of the data structure rather than simply reading data. Examples include pointer rewiring in linked structures, node rotations or swaps in trees or heaps, or element shifts in arrays. These operations typically represent the “maintenance work” required to preserve the structure’s invariants (ordering, heap property, collision chains, etc.).

---

### Inserts
An **insert** records each attempt to add a value to the data structure. If the structure enforces uniqueness (like a set), an insert may fail if the value already exists. Insert metrics help measure how efficiently the structure accommodates growth and how costly it is to maintain ordering or structural constraints while adding new elements.

---

### Deletes
A **delete** records each attempt to remove a value from the data structure. Depending on the implementation, deletion may involve locating the element first and then restructuring the surrounding elements or pointers. Tracking delete operations highlights how expensive removal is for different structures, particularly those that require shifting elements or reorganizing nodes.

---

### Lookups
A **lookup** represents a membership query such as `contains(value)` or `find(value)`. Lookups measure how quickly a structure can determine whether an element is present. Because many real-world systems perform far more reads than writes, lookup performance is often one of the most important metrics in evaluating a data structure.

---

### Resize Events
A **resize event** occurs when a data structure must allocate a larger block of memory to accommodate additional elements. This commonly happens in dynamic arrays or hash tables when the current capacity is exhausted or a load factor threshold is exceeded. Although resizing is infrequent, it can be costly because existing elements often must be copied or rehashed into the new storage.

---

### Shifts or Relinks
Shifts or relinks count the number of internal element movements required to maintain the structure after an insertion or deletion.
	•	In array-based structures, this usually means shifting elements left or right to preserve ordering.
	•	In linked structures, it represents pointer updates when nodes are inserted, removed, or rearranged.
	•	In heaps, it may correspond to swaps during sift-up or sift-down operations.

Tracking these movements helps distinguish between structures that rely on pointer manipulation versus those that require large memory moves, which can have very different performance characteristics on real hardware.

---

## Track and Save Counts

By creating an instance of the following in each class, you can add lines of code in the necessary functions that increment these values. 

```cpp
struct Counters {
    long long comparisons = 0;
    long long structural_ops = 0;
    long long inserts = 0;
    long long deletes = 0;
    long long lookups = 0;
    long long resize_events = 0;
    long long shifts_relinks = 0;
};
```

- You can placer and instance of the Counters struct in each class as a data member. No inheritance necessary, composition only.
- By incrementing the right values in the right methods, you can track what the structure is doing. 
- Notice all the reset and return counters? After every run, you will return that instance of the counts and save them appropriately.

```cpp
class BST  {
    Node* root; 
    Counters counters;
    string name;
public:
    BST(){
        name = "BST";
    }
    string name(){
        return name; 
    }

    void reset()  { 
        /* clear your DS */ 
    }

    void reset_counters()  { 
        // create a new instance 
        counters = Counters{}; 
    }

    Counters counters() { 
        return counters; 
    }

    void insertKey(int k)  {
        counters.inserts++;
        // increment these meaningfully in your real implementation:
        counters.comparisons += 1;
        counters.structural_ops += 1;
    }

    void deleteKey(int k)  {
        counters.deletes++;
        counters.comparisons += 1;
        counters.structural_ops += 1;
    }

    bool findKey(int k)  {
        counters.lookups++;
        counters.comparisons += 1;
        counters.structural_ops += 1;
        return false;
    }
};
```
### Workloads and Saving Stats

Assuming you added all the Counters code to each data structure, you can then iterated over each data structure and the workloads (If you pre-generated them which I recommend). It would go something like this:

```
📁 workLoads
├── 📕workLoad_A_1000.json
├── 📕workLoad_A_5000.json
├── 📕workLoad_A_10000.json
├── 📕workLoad_A_20000.json
├── 📕workLoad_B_1000.json
├── 📕workLoad_B_5000.json
├── 📕workLoad_B_10000.json
├── 📕workLoad_B_20000.json
├── 📕workLoad_C_1000.json
├── 📕workLoad_C_5000.json
├── 📕workLoad_C_10000.json
├── 📕workLoad_C_20000.json
├── 📕workLoad_D_1000.json
├── 📕workLoad_D_5000.json
├── 📕workLoad_D_10000.json
└── 📕workLoad_D_20000.json
```

Where workload files contain stuff like: 

```json
    [ 
        "insert",12
        "insert",44
        "insert",12
        "contains",12
        "contains",51
        ...
    ]
```

```python
for ds in ['bst','heap','linkedlist','array','hash']:
    for file in workloads:
        # run all the files for bst first then save the output in its own folder
```

And after runs for a specific data structure our file list below:

```
📁 bst_runs
├── 📕workLoad_A_1000.json
├── 📕workLoad_A_5000.json
├── 📕workLoad_A_10000.json
├── 📕workLoad_A_20000.json
├── 📕workLoad_B_1000.json
├── 📕workLoad_B_5000.json
├── 📕workLoad_B_10000.json
├── 📕workLoad_B_20000.json
├── 📕workLoad_C_1000.json
├── 📕workLoad_C_5000.json
├── 📕workLoad_C_10000.json
├── 📕workLoad_C_20000.json
├── 📕workLoad_D_1000.json
├── 📕workLoad_D_5000.json
├── 📕workLoad_D_10000.json
└── 📕workLoad_D_20000.json
```

Would all contain something like (do not read into my random numbers in the example below)

```json
{
    "comparisons":25252,
    "structural_ops":5642,
    "inserts":500,
    "deletes":200,
    "resize_events":34,
    "shifts_relinks":170
};
```


## Folder Structure

Here is the new organization to `Program 02`'s 

```txt
📁 05-P02
├── ✳️ README.md        // This file
└── 📁 src              // Code files  
    ├── 📁 include      // Include hpps can't run directly
    │   ├── 📕 binaryHeap.hpp
    │   ├── 📕 bst.hpp
    │   ├── 📕 counters.hpp
    │   ├── 📕 hashTable.hpp
    │   ├── 📕 json.hpp
    │   ├── 📕 linkedList.hpp
    │   ├── 📕 sortedArraySet.hpp
    │   ├── 📕 termcolor.hpp
    │   └── 📕 usagePrinter.hpp
    ├── 📁 tests        // Tests for each of the hpp data structures
    │   ├── 📕 test_BinaryHeap.cpp  
    │   ├── 📕 test_Bst.cpp
    │   ├── 📕 test_HashTable.cpp
    │   ├── 📕 test_LinkedList.cpp
    │   └── 📕 test_SortedArraySet.cpp
    └── 📕workload_generator.cpp
```

There is no executable code uploaded. You must compile it to run it. To compile a **`test`** or the **`workload_generator`** you can do it a couple of different ways depending on where you want the object file to end up and where you compilefrom.

- The `-I` flag tells g++ where to look for additional header files.
- So if I want to compile a test from inside the src directory and have the object file end up in the src directory, I would do this: 
  - `g++ -std=c++20 -Iinclude tests/test_Bst.cpp -o bst`
- If I want to compile from the `05-P02` folder and have the object file end up in that same folder, I would do this: 
  - `g++ -std=c++20 -Isrc/include src/tests/test_Bst.cpp -o bst`
  
- Basically the `-I` flag says where to look for header files based on where you are.
- The next portion like `src/tests/...` is a path to a source file to compile.
- The last portion `-o` is your output object file. So if I write `-o ../../bst` it will create the object file `bst` two folders up. 
- Understanding paths is a big part of this.

### Workload Generator

The workload generator needs to be compiled as well. I would compile it from where it is in the `src` folder like this: 

- `g++ -std=c++20 -Iinclude workload_generator.cpp -o workload_generator`
  
Once you get it compiled, run it like so: 

- `./workload_generator -h` 

and you should see something like: 

```
Usage:
  workload_generator [OPTIONS]

Options:
  -w, --workload <TYPE>       Workload type (A,B,C,D)
  -n, --size     <N>          Base problem size N=int
  --preview      <K>          Preview operations K=int
  --json                      Emit JSON output
  -s, ---save    <FILENAME>   Save output to a file
  -h, --help                  Show help message

Examples:
./workload_generator --json -w C -n 1000 > workload.json
./workload_generator --json -workload B -size 5000 --save workload_B_5000.json
```

This shows you a couple of examples on how to run the workload_generator. 
- This example: `./workload_generator --json -w C -n 1000 > workload.json` 
  - **`--json`** says output a json object (list)
  - **`-w C`** uses workload_C for the job type
  - **`-n 1000`** generates 1000 events
  - `>` redirects output into a file called `workload.json`
  
- This example: `./workload_generator --json -workload B --size 5000 --save workload_B_5000.json`
  - Also will output json
  - **`--workload`** is equivalent to `-w` and this time the job types will be from `B`
  - **`--size`** is equivalent to `-n` and will generate 5000 events
  - **`--save`** is almost like redirect > but it actually opens the filename that comes after the --save flag, in this case: `workload_B_5000.json`
