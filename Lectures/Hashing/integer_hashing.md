```yaml
id: integer_hash_functions_overview
topic: hash_functions_for_integers
audience: cs_students_algorithms
goal: recommend_practical_hash_functions
sections:
  - simple_modulo
  - multiplicative_hashing
  - bit_mixing_hash
  - modern_fast_hash
```

For **Integers specifically**, hashing is actually easier than general hashing because the input is already numeric. The goal is just to **mix the bits well** so patterns in the keys don’t cause clustering.

There are a few tiers depending on how serious you want to be.

---

# 1️⃣ The classic textbook hash (good for teaching)

If you’re doing a **hash table with a fixed capacity**, the traditional approach is:

```cpp
size_t hash(int key, size_t capacity) {
    return key % capacity;
}
```

### Works well when

- capacity is **prime**
- keys are **random-ish**

### Bad when

Keys share patterns:

```
10, 20, 30, 40
```

with capacity 10 → all collide.

So it's good pedagogically but not robust.

---

# 2️⃣ Multiplicative hashing (better distribution)

Knuth’s multiplicative method:

```
h(k) = floor(m * frac(k * A))
```

Where

```
A ≈ 0.6180339887
```

Example:

```cpp
size_t hash(int key, size_t capacity) {
    const double A = 0.6180339887;
    double frac = key * A - floor(key * A);
    return capacity * frac;
}
```

### Pros

- avoids simple modulo clustering
- good for sequential keys

### Cons

- uses floating point
- slower

---

# 3️⃣ Bit mixing hash (excellent for integers)

A very good **simple integer mixer**:

```cpp
uint32_t hash(uint32_t x) {
    x ^= x >> 16;
    x *= 0x7feb352d;
    x ^= x >> 15;
    x *= 0x846ca68b;
    x ^= x >> 16;
    return x;
}
```

Then map to the table:

```cpp
index = hash(key) % capacity;
```

### Why this is good

It:

- destroys patterns
- spreads nearby integers apart
- avoids clustering

This style is used in many modern hash implementations.

---

# 4️⃣ The “golden ratio” bit hash (super common)

Another excellent integer hash:

```cpp
size_t hash(uint32_t key) {
    return key * 2654435761u;
}
```

Then

```cpp
index = hash(key) % capacity;
```

Where

```
2654435761 = 2^32 / φ
```

This constant comes from **Knuth's multiplicative hashing**.

### Why it's good

Sequential numbers like

```
1,2,3,4,5
```

become:

```
2654435761
1013904226
3668339987
2027808452
387276917
```

which are well mixed.

This is extremely common.

---

# 5️⃣ What `std::hash<int>` does

Most standard libraries effectively do something close to:

```cpp
size_t hash(int x) {
    return x;
}
```

Because the table implementation itself mixes bits internally.

---

# 6️⃣ Simple In Class Hash Function

For a class assignment:

```cpp
size_t hash(int key) {
    return key * 2654435761u;
}
```

Then

```cpp
index = hash(key) % capacity;
```

This gives:

✔ simple code  
✔ good distribution  
✔ easy explanation  
✔ no floating point  

---

# 7️⃣ Learning Takeaway

- Hashing is not  **complicated math**.
- Its send a value to a hash function and get a big number back.
- Use modulo to fit big number into your array (and hope for little or no collisions)

- For integers, the best idea is to just:
  - mix the bits
  - then compress to table size (modulo)

---

# 8️⃣ Cool Demo

Plain modulo can be not good.

Example:

```cpp
for(int i=0;i<20;i++)
    cout << (i * 10) % 10 << endl;
```

Output:

```
0
0
0
0
0
```

But with the right constant:

```cpp
(i * 2654435761u) % 10
```

Now it distributes.


