## The Answer to Everything (42)

<sup>Well, in regards to Program 02</sup>

### Provided to You

There are c++ implementations for:
- Binary Heap
- Binary Search Tree
- Hash Table
- Linked List
- Ordered Dynamic Array

with all necessary basic functionality and small tests to show how to use each of them. 
There is no additional code added to count any of the stats we want to collect for comparing different data structures and how they handle certain types of behaviors (insert, find, delete). Below is the new folder structure: 

### Folder Structure

Here is the new organization for `Program 02`'s 

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

Where the `src` folder holds all the `hpp's` in the `include` folder and the `tests` folder containing `cpp's` that should compile and run showing each data structure's hpp works. 

### Compiling 

There is no executable code uploaded. You must compile it to run it. To compile a **`test`** or the **`workload_generator`** you can do it a couple of different ways depending on where you want the object file to end up and where you compile from.

A typical compile command looks like: 

- `g++ source_file.cpp -o objectfile`

**Where:**
- `g++` : is the compiler invocation
- `source_file.cpp` : is the file you want to compile
- `-o` is a flag indicating the name of the object file. 

**Additional Flags:**

- `-std=c++20` : this flag tells g++ which version of c++ to use when compiling
- `-I` : This flag tells g++ where to look for additional header files (usually ones written by you and not 'installed')

**Compile Command Examples**

- If I want to compile a test from inside the `src` directory and have the object file end up in the same directory (`src`), I would do this: 
  - `g++ -std=c++20 -Iinclude tests/test_Bst.cpp -o bst`
- If I want to compile from the `05-P02` folder and have the object file end up in that same folder, I would do this: 
  - `g++ -std=c++20 -Isrc/include src/tests/test_Bst.cpp -o bst`
- If I want to compile from `src` folder  and I want my object file to end up in the parent folder (`05-P02`):
  - `g++ -std=c++20 -Iinclude tests/test_Bst.cpp -o ../bst`
  

## Programs Goal

The goal is to track stats for each of the data structures we have been discussing as they process the same data sets. The "big picture" as I see it is for you to learn and understand certain choices we make when determining what structures would work best in specific conditions. But before we compare structures, we need to determine what data points are important enough to track. The following is a list (with descriptions) of the stats (data points) we will analyze. 

### Comparisons

- A **comparison** occurs whenever two values are evaluated relative to one another (e.g., `<`, `>`, or `==`).  Comparisons are the fundamental operations that drive decision-making in most data structures. For example, a binary search tree uses comparisons to determine whether to traverse left or right, and a sorted array uses comparisons during binary search. Tracking comparisons helps reveal how efficiently a structure locates elements as the data size grows.

---

### Structural Operations
- A **structural operation** is any action that modifies the internal organization of the data structure rather than simply reading data. Examples include pointer rewiring in linked structures, node rotations or swaps in trees or heaps, or element shifts in arrays. These operations typically represent the “maintenance work” required to preserve the structure’s invariants (ordering, heap property, collision chains, etc.).

---

### Inserts
- An **insert** records each attempt to add a value to the data structure. If the structure enforces uniqueness (like a set), an insert may fail if the value already exists. Insert metrics help measure how efficiently the structure accommodates growth and how costly it is to maintain ordering or structural constraints while adding new elements.

---

### Deletes
 - A **delete** records each attempt to remove a value from the data structure. Depending on the implementation, deletion may involve locating the element first and then restructuring the surrounding elements or pointers. Tracking delete operations highlights how expensive removal is for different structures, particularly those that require shifting elements or reorganizing nodes.

---

### Lookups
- A **lookup** represents a membership query such as `contains(value)` or `find(value)`. Lookups measure how quickly a structure can determine whether an element is present. Because many real-world systems perform far more reads than writes, lookup performance is often one of the most important metrics in evaluating a data structure.

---

### Resize Events
- A **resize event** occurs when a data structure must allocate a larger block of memory to accommodate additional elements. This commonly happens in dynamic arrays or hash tables when the current capacity is exhausted or a load factor threshold is exceeded. Although resizing is infrequent, it can be costly because existing elements often must be copied or rehashed into the new storage.

---

### Shifts or Relinks
- Shifts or relinks count the number of internal element movements required to maintain the structure after an insertion or deletion.
	•	In array-based structures, this usually means shifting elements left or right to preserve ordering.
	•	In linked structures, it represents pointer updates when nodes are inserted, removed, or rearranged.
	•	In heaps, it may correspond to swaps during sift-up or sift-down operations.

- Tracking these movements helps distinguish between structures that rely on pointer manipulation versus those that require large memory moves, which can have very different performance characteristics on real hardware.

---
To track the above list of items, you will need to add a bit of code to each structure. Below you see a list of "counters" that simply count events as they happen. 

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

Basic example:

```cpp
#include "Counters.hpp"

class DS{
private:
    Counters c;
    void _insert(Node* root, x){
        // this method keeps comparing values to find correct location
        // so we increment comparisons.
        c.comparisons++
    })
public:
    void insert(int x){
        c.inserts++;
        _insert(Node* root, x);
    }
}

So you can create an instance of the Counters in each class, and then add the necessary lines of code in each particular function to track all the stats. 

- You can placer and instance of the Counters struct in each class as a data member. No inheritance necessary, composition only.
- By incrementing the right values in the right methods, you can track what the structure is doing. 
- Notice all the reset and return counters? After every run, you will return that instance of the counts and save them appropriately.

```cpp
class BST  {
    Node* root; 
    Counters counters;
    string name;
    // private find, delete, insert methods up here counting comparisons
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
        counters.structural_ops += 1;

        // This next one would be done in the private _insertKey method
        // while it is traversing (comparing) looking for the key
        counters.comparisons += 1;
    }

    void deleteKey(int k)  {
        counters.deletes++;
        counters.structural_ops += 1;

        // This next one would be done in the private _deleteKey method
        // while it is traversing (comparing) looking for the key
        counters.comparisons += 1;
    }

    bool findKey(int k)  {
        counters.lookups++;

        // This next one would be done in the private _findKey method
        // while it is traversing (comparing) looking for the key
        counters.comparisons += 1;
        return _findKey(root,k);
    }
};
```
---

## Workload Types

Above we discuss (well list) the data structures we will compare, we discuss how to compile some code, and we discuss a bit about counting events for each structure. Now we need to discuss the different workload types, which very much impact which data structure we would normally choose. But for our experiment, we will expose each structure to all workload types. Just for a simple overview, the major workload types are:

- Build once, tons of searches with few inserts and deletes (stable structure)
- Highly fluctuating: lots of inserts and deletes with few searches. 
- Mix : a little bit of everything 

A little more to think about that doesn't have a lot to do with our experiment (except "is it ordered") because ordered data destroys a binary search tree that doesn't do rotations. 

- Type of data (string, integer)
- **Is it ordered**
- Is it mixed
- Is it random
- is it missing values

So based on some pretty common workload experiences, here are 4 that we will use to test our structures:

### Workload A

- Random inserts followed by random lookups (not a ton of fluctuation)

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

- Insert n items then perform heavy lookup activity (stable structure).

- Pattern:
   - n inserts
   - 5n lookups
- Useful for read-heavy workloads.

---


## Track and Save Counts

Now we discuss comparing all the runs for each structure. If you're not going to use a runner file to control all the runs (which is ok), then I would recommend creating all of the input files first. 

### Workloads and Saving Stats

Assuming your structures have the counting code added and now you just need to count everything for each run, lets look at how we might do the big experiment. As I stated, the simple path is to create all the workload files with each holding a different workload type (A-D) and a different number of operations (1000,5000,10000,20000). How do we do this?

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

## Workload Generator

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

Using the workload generator you can create the files that you need for all your runs. You can do it in a file that will run all different runs of the generator. Lets call it `batch.sh`:

```sh
./workload_generator  -workload A  --size 1000 --save workload_A_1000.json
./workload_generator  -workload A  --size 5000 --save workload_A_5000.json
./workload_generator  -workload A --size 10000 --save workload_A_10000.json
./workload_generator  -workload A --size 20000 --save workload_A_20000.json
./workload_generator  -workload B  --size 1000 --save workload_B_1000.json
./workload_generator  -workload B - -size 5000 --save workload_B_5000.json
./workload_generator  -workload B --size 10000 --save workload_B_10000.json
./workload_generator  -workload B --size 20000 --save workload_B_20000.json
# you can add the rest ...
```

Next make `batch.sh` executable: 

```sh
chmod +x batch.sh
```

Now run it: 

```sh
./batch.sh
```

All files created. 

Or maybe write a script:

```python
#!/usr/bin/env python3

import subprocess

workloads = ["A", "B", "C", "D"]
sizes = [1000, 5000, 10000, 20000]

for w in workloads:
    for n in sizes:
        outfile = f"workload_{w}_{n}.json"

        cmd = [
            "./workload_generator",
            "--workload", w,
            "--size", str(n),
            "--save", outfile
        ]

        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)
```

- This will create the files automatically. If you want to test it first, comment out the `subprocess.run` command and just look at the output. 
- If you want to write to a folder, then edit this line: `outfile = f"workload_{w}_{n}.json"` and add your folder name: `outfile = f"newFolder/workload_{w}_{n}.json"`

## File Contents

Each workload file will hold a json list with a command and a value where the commands are ['contains','insert','delete'] and the values are some valid integer . This difference between the files depends on its size [1000.5000,10000,20000] and its workload [A,B,C,D] as defined above. 

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

## Running Your Experiment

This will be up to you. The big picture again is: 

1. Add Counter code to each data structure so that you can save the counts for a single run. 
2. Generate your workloads.
3. Run each data structure with each workload saving your results either in a file, or append it to a csv or json structure.


## Deliverables

TBD