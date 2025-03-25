## Hashing - Introduction to Hash Tables

#### Due: N/A

# Major Topic Points for a Lecture on Hash Tables

## 1️⃣ **Introduction to Hash Tables**

- Definition: What is a hash table?
- Real-world applications (e.g., database indexing, caching, symbol tables in compilers).
- Comparison with other data structures (arrays, linked lists, trees).

---

## 2️⃣ **Hash Functions**

- What is a hash function?
- Properties of a good hash function:
  - **Deterministic**: Same input always gives the same output.
  - **Uniform Distribution**: Spreads keys evenly across the table.
  - **Efficient**: Fast to compute.
  - **Minimizes Collisions**.
- Example hash functions:
  - **Modulo-based hashing** (`key % table_size`).
  - **Multiplication method**.
  - **String hashing** (e.g., ASCII sum, polynomial rolling hash).
  - **Cryptographic hashing** (MD5, SHA-256, not commonly used for hash tables).

---

## 3️⃣ **Handling Collisions**

- Why do collisions happen?
- Collision resolution techniques:
  1. **Chaining (Separate Chaining)**
     - Uses linked lists or dynamic arrays at each index.
     - Advantages and disadvantages.
  2. **Open Addressing**
     - **Linear Probing** (`(hash + i) % size`)
     - **Quadratic Probing** (`(hash + i²) % size`)
     - **Double Hashing** (`(hash1 + i * hash2) % size`)
  3. **Perfect Hashing** (for static data sets).
  4. **Cuckoo Hashing** (multiple hash functions).
  5. **Robin Hood Hashing** (stealing from richer buckets).

---

## 4️⃣ **Load Factor and Resizing**

- Definition: `Load Factor = (number of elements) / (table size)`.
- How load factor affects performance.
- When to resize a hash table (e.g., load factor > 0.7).
- Resizing strategies (e.g., doubling size and rehashing).

---

## 5️⃣ **Performance Analysis**

- **Average case** complexity:
  - Insert: **O(1)**
  - Search: **O(1)**
  - Delete: **O(1)**
- **Worst case** (when collisions degrade performance):
  - Insert: **O(n)**
  - Search: **O(n)**
  - Delete: **O(n)**
- Impact of a poor hash function on performance.

---

## 6️⃣ **Hash Tables in Practice**

- Standard hash table implementations:
  - **C++**: `std::unordered_map`
  - **Python**: `dict`
  - **Java**: `HashMap`
- How different programming languages optimize their hash tables.
- Example use cases:
  - Fast lookups in databases.
  - Caching (e.g., LRU Cache).
  - Counting frequency of elements (word frequency in text processing).

---

## 7️⃣ **Advanced Topics (Optional)**

- **Dynamic Perfect Hashing** (minimal perfect hashing for large datasets).
- **Bloom Filters** (probabilistic data structures using hashing).
- **Consistent Hashing** (used in distributed systems, e.g., load balancing).
- **Hash Tables vs. Balanced Trees (e.g., AVL, Red-Black Trees)**.

---

## 🎯 **Summary and Key Takeaways**

- Hash tables are **fast** for lookup operations but require a **good hash function**.
- Collision resolution is **critical** for maintaining efficiency.
- Load factor determines when to **resize the table**.
- Used widely in **real-world applications** (databases, caches, symbol tables).

---

## 📝 **Potential Exercises**

1. Implement a basic hash table using **chaining** in C++ or Python.
2. Modify the implementation to use **linear probing**.
3. Analyze the **impact of different hash functions** on performance.
4. Implement a **simple cache system** using a hash table.
5. Compare **hash tables vs. balanced trees** in a lookup-heavy scenario.

---

# 🎯 **Example Hash Functions - A Lecture on Hashing in C++**

## 📝 **Introduction**

A **hash function** is a mathematical function that **converts input data (keys) into an index** in a **hash table**. The goal of a good hash function is to distribute keys **evenly** and **efficiently** while minimizing **collisions**.

This lecture will cover:

- What makes a **good hash function**.
- **Common hash function techniques**.
- **Example implementations** in C++.

---

## 🚀 **1. What Makes a Good Hash Function?**

A **good hash function** should:

1. **Be deterministic** → The same input always produces the same output.
2. **Be fast** → The function should execute in **constant time O(1)**.
3. **Distribute keys uniformly** → Prevent clustering in a few spots.
4. **Minimize collisions** → Different inputs should hash to different values as much as possible.
5. **Use the entire range of the table** → Spread values evenly.

---

## 🔢 **2. Example Hash Functions in C++**

### ✨ **1. Simple Modulo Hashing**

A basic way to map integer keys to a hash table of size `N` is using **modulo division**.

#### **Formula:**

$\text{index} = (\text{key} \mod \text{table size})$

#### **C++ Implementation:**

```cpp
#include <iostream>
using namespace std;

int hashFunction(int key, int tableSize) {
    return key % tableSize;  // Modulo operation to get an index
}

int main() {
    int tableSize = 10;
    cout << "Hash of 25: " << hashFunction(25, tableSize) << endl;
    cout << "Hash of 37: " << hashFunction(37, tableSize) << endl;
    cout << "Hash of 49: " << hashFunction(49, tableSize) << endl;
    return 0;
}
```

#### 🛠️ Output Example:

```
Hash of 25: 5
Hash of 37: 7
Hash of 49: 9
```

- ✅ Pros: Simple, fast, and efficient for integer keys.
- ❌ Cons: Can cause collisions when numbers cluster around the same remainders.

### ✨ 2. Multiplication Method

This method is useful when the key space is large.

Formula:

$\text{index} = \lfloor N \times (K \times A \mod 1) \rfloor$

- Where:
  - $K$ is the key.
  - $A$ is a constant fractional number (commonly 0.6180339887).
  - $N$ is the table size.
  - $mod\ 1$ extracts the decimal portion.

#### C++ Implementation:

```cpp
#include <iostream>
using namespace std;

int hashFunction(int key, int tableSize) {
    const double A = 0.6180339887;  // A fractional constant (commonly used)
    double fractionalPart = key * A - int(key * A);
    return int(tableSize * fractionalPart);
}

int main() {
    int tableSize = 10;
    cout << "Hash of 25: " << hashFunction(25, tableSize) << endl;
    cout << "Hash of 37: " << hashFunction(37, tableSize) << endl;
    cout << "Hash of 49: " << hashFunction(49, tableSize) << endl;
    return 0;
}
```

- ✅ Pros: Works well for non-uniform data, spreads keys better than modulo.
- ❌ Cons: Slightly more computation than modulo.

### ✨ 3. String Hashing (Polynomial Rolling Hash)

When hashing strings, each character contributes to the final value.

#### Formula:

$\text{hash} = (c_1 \times p^0 + c_2 \times p^1 + c_3 \times p^2 + \dots) \mod M$

- Where:
  - $c_i$ = ASCII value of character at position i.
  - $p$ = Small prime number (e.g., 31).
  - $M$ = Large prime modulus to prevent overflow (e.g., 1e9 + 9).

**C++ Implementation:**

```cpp
#include <iostream>
using namespace std;

const int P = 31;
const int MOD = 1e9 + 9;

int stringHash(string s, int tableSize) {
    long long hashValue = 0;
    long long pPower = 1;

    for (char c : s) {
        hashValue = (hashValue + (c - 'a' + 1) * pPower) % MOD;
        pPower = (pPower * P) % MOD;
    }
    return hashValue % tableSize;
}

int main() {
    int tableSize = 10;
    cout << "Hash of 'sword': " << stringHash("sword", tableSize) << endl;
    cout << "Hash of 'shield': " << stringHash("shield", tableSize) << endl;
    cout << "Hash of 'staff': " << stringHash("staff", tableSize) << endl;
    return 0;
}
```

- ✅ Pros: Works well for variable-length strings, commonly used in text search & hashing algorithms.
- ❌ Cons: Computationally heavier than integer hashing.

### ✨ 4. Universal Hashing (Randomized)

Universal hashing chooses a random hash function at runtime from a set of hash functions.

**Formula:**

$\text{hash} = ((a \times key + b) \mod p) \mod N$

- Where:
  - $a, b$ are randomly chosen constants.
  - $p$ is a prime number greater than N.
  - $N$ is the table size.

**C++ Implementation:**

```cpp
#include <iostream>
#include <cstdlib>
using namespace std;

int universalHash(int key, int tableSize) {
    const int p = 101;  // Large prime number
    int a = rand() % p + 1;  // Random number in range [1, p-1]
    int b = rand() % p;      // Random number in range [0, p-1]
    return ((a * key + b) % p) % tableSize;
}

int main() {
    int tableSize = 10;
    cout << "Hash of 25: " << universalHash(25, tableSize) << endl;
    cout << "Hash of 37: " << universalHash(37, tableSize) << endl;
    cout << "Hash of 49: " << universalHash(49, tableSize) << endl;
    return 0;
}
```

- ✅ Pros: Prevents worst-case attacks, great for cryptographic applications.
- ❌ Cons: Requires randomization, slightly slower due to modular arithmetic.

### 🎯 5. Comparing Hash Functions

| Hashing Method         | Pros                        | Cons                        | Best Used For              |
| :--------------------- | :-------------------------- | :-------------------------- | :------------------------- |
| Modulo Hashing         | Fast, simple                | Prone to clustering         | Small integers             |
| Multiplication Hashing | More uniform spread         | Requires floating-point ops | Large key spaces           |
| Polynomial Hashing     | Works well for strings      | Requires prime modulus      | Text search, dictionaries  |
| Universal Hashing      | Prevents worst-case attacks | Needs randomness            | Cryptographic applications |

### 🎯 6. Summary & Key Takeaways

- A good hash function should be fast, uniform, and minimize collisions.
- Modulo Hashing is simple but may cause clustering.
- Multiplication Hashing helps with uniform distribution.
- String Hashing (Polynomial Rolling) is great for text-based data.
- Universal Hashing is best for cryptographic and security applications.

## 📝 Homework & Exercises

1. Modify the modulo hashing function to work with floating-point numbers.
2. Implement a simple hash table using chaining with modulo hashing.
3. Test different string hashing techniques using real-world data.

# 🔢 The Division Method

## 🎯 **What Is the Division Method?**

The **division method** is one of the **simplest** and most commonly used **hash functions** for mapping keys into a hash table.

### **Formula:**

$h(k) = k \mod m$

**Where:**

- $( k )$ = Key to be hashed.
- $( m )$ = Hash table size.
- $( h(k) )$ = Index in the hash table.

This function **divides** the key by the table size and takes the remainder as the **index**.

---

## 🏗 **How It Works (Example in C++)**

```cpp
#include <iostream>
using namespace std;

// Division method hash function
int hashFunction(int key, int tableSize) {
    return key % tableSize;  // Remainder after division
}

int main() {
    int tableSize = 10;
    cout << "Hash of 25: " << hashFunction(25, tableSize) << endl;
    cout << "Hash of 37: " << hashFunction(37, tableSize) << endl;
    cout << "Hash of 49: " << hashFunction(49, tableSize) << endl;
    return 0;
}
```

**🛠️ Example Output**

```

Hash of 25: 5
Hash of 37: 7
Hash of 49: 9

```

Each key is divided by 10, and the remainder determines its position.

- ✅ Advantages of the Division Method

  1. Simple to implement → Just one modulo operation.
  2. Fast → Runs in constant time O(1).
  3. Efficient for small datasets.

- ❌ Disadvantages & Limitations
  1. Clustering Issues
     - If the table size is not a prime number, certain hash values are used more frequently, causing collisions.
  2. Poor Distribution for Some Keys
     - If keys have a common factor with m, they cluster into a few slots.

#### 🏆 Best Practices to Improve the Division Method

1. Use a Prime Number for Table Size (m)
   - If m is prime, the keys spread more evenly across the table.
   - Example: Instead of m = 10, use m = 11 or m = 17.
2. Avoid Powers of 2 (m = 2^p)
   - Using m = 16 (or any power of 2) results in collisions for binary keys.
   - Instead, choose a prime number that is not close to a power of 2.
3. Use a Load Factor & Rehashing
   - If the table gets too full, dynamically resize it and pick a new prime m.

#### 🔍 Is the Division Method Still Used Today?

- Yes, but with modifications!
  - Still used for basic hash tables in:
  - Compilers (symbol tables).
  - Small-scale hash tables (e.g., caching).
  - Simple key-value maps.
  - Not ideal for large-scale databases, cryptography, or distributed systems, where:
  - Multiplication Hashing (Knuth’s method) or Universal Hashing is preferred.
  - Cryptographic Hash Functions (e.g., SHA-256) are used for security.

## 📝 Summary

| Feature     | Division Method                              |
| :---------- | :------------------------------------------- |
| Formula     | $h(k) = k % m$                               |
| Pros        | Simple, fast, easy to implement              |
| Cons        | Poor distribution if m is not prime          |
| Fix         | Use prime numbers for m to reduce clustering |
| Used today? | Yes, but mainly for basic hash tables        |

#### 🚀 Takeaway:

The division method is a classic, easy-to-implement hash function. While still used, it works best when combined with prime-number table sizes to avoid clustering.

# 🚨 **Poor Hash Table Size Choices & The Low-Order Bit Problem**

## 🎯 **Why Table Size Matters in Hashing**

When choosing a **hash table size (`m`)**, selecting a **poor value** can cause the hash function to rely only on the **low-order bits** of the key, leading to **more collisions**.

### Common Mistake: Using a Power of 2 for `m`

If $m = 2^p$ (e.g., 16, 32, 64), the modulo operation:

$h(k) = k \mod m$

only retains the **lowest `p` bits** of `k`, **ignoring the higher bits**.

### **Problem: Clustering of Hash Values**

- If keys follow a **pattern** (e.g., even increments, sequential numbers), they will hash to **repeating indices**.
- This **wastes space** and increases **collisions**.

---

## 🛑 **Example of a Bad Hash Table Size**

```cpp
#include <iostream>
using namespace std;

// Poor hash function: Uses a power of 2 for the table size
int badHash(int key, int tableSize) {
    return key % tableSize;
}

int main() {
    int tableSize = 16;  // Power of 2 (BAD CHOICE)
    int keys[] = {18, 34, 50, 66, 82};  // All keys differ by 16 (a multiple of 2)

    cout << "Hash Values (Modulo " << tableSize << "):\n";
    for (int key : keys) {
        cout << "Key " << key << " -> Index " << badHash(key, tableSize) << endl;
    }
    return 0;
}
```

**🛠️ Output:**

- Hash Values (Modulo 16):
  - Key 18 -> Index 2
  - Key 34 -> Index 2
  - Key 50 -> Index 2
  - Key 66 -> Index 2
  - Key 82 -> Index 2

**🚨 Problem:**

All keys collide at index 2 because tableSize = 16 causes low-order bit repetition.

✅ Fix: Use a Prime Number for m

Instead of $m = 16$, choose a prime number like $17$:

```cpp
int goodHash(int key, int tableSize) {
    return key % tableSize;
}

int main() {
    int tableSize = 17;  // Prime number (GOOD CHOICE)
    int keys[] = {18, 34, 50, 66, 82};

    cout << "Hash Values (Modulo " << tableSize << "):\n";
    for (int key : keys) {
        cout << "Key " << key << " -> Index " << goodHash(key, tableSize) << endl;
    }
    return 0;
}
```

**🛠️ Output (Using Prime Table Size m = 17):**

- Hash Values (Modulo 17):
  - Key 18 -> Index 1
  - Key 34 -> Index 0
  - Key 50 -> Index 16
  - Key 66 -> Index 15
  - Key 82 -> Index 14

✅ Keys are now spread out and collisions are reduced.

**🔥 Takeaways**

| Bad Table Size                          | Why It’s Bad                                                                           |
| :-------------------------------------- | :------------------------------------------------------------------------------------- |
| $m = 2^p$ (e.g., 16, 32, 64)            | Uses only low-order bits, causing clustering                                           |
| Small m (e.g., 10)                      | Leads to frequent collisions if keys are not well distributed                          |
| m that shares factors with key patterns | Creates periodic collisions (e.g., keys that are multiples of 4 in a table of size 16) |

- ✅ Best Practices
  - Choose m as a prime number → Prevents patterns from forming.
  - Avoid m that is a power of 2 → Forces use of low-order bits.
  - Rehash dynamically → When load factor > 0.7, resize m to the next prime number.

### 🚀 Final Thought

Choosing the right hash table size (m) is just as important as the hash function itself!
Bad choices (powers of 2) cause clustering, while prime numbers help distribute keys evenly.

**🔑 Rule of Thumb:**

Always use a prime number for the table size to avoid low-order bit collisions. 🔥
