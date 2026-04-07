## Huffman Coding — Compression by Frequency

#### Due: N/A

---

## The Big Picture: Why Compress at All?

Every file on your computer is a sequence of bits. Most files have **redundancy** — patterns that repeat, values that are more common than others. Compression exploits that redundancy to represent the same information in fewer bits.

Two flavors:

| Type | Guarantees | Typical Use |
|------|-----------|-------------|
| **Lossless** | Perfect reconstruction — every bit recovered | Text, code, ZIP, PNG |
| **Lossy** | Approximate reconstruction — some data discarded | JPEG, MP3, H.264 |

Huffman coding is **lossless**. You get your original data back, bit for bit. The tradeoff is that it can't compress as aggressively as lossy methods — but for anything where correctness matters (source code, executables, documents), that's non-negotiable.

---

## The Core Idea in One Sentence

> Assign shorter binary codes to frequent symbols, longer codes to rare ones — then the average message length shrinks.

English text uses `e`, `t`, `a` constantly and `z`, `q`, `x` almost never. If `e` costs 3 bits and `z` costs 8 bits in standard ASCII they're both 8 bits. Huffman says: give `e` 2 bits, give `z` 12 bits. If you see `e` a thousand times and `z` twice, you've saved a lot.

This idea predates Huffman — the insight is ancient. What Huffman contributed in 1952 was a **provably optimal** algorithm for building these variable-length codes.

### Wait — What Does "3 Bits" Actually Mean?

This trips up almost everyone who hasn't done low-level binary I/O before. When we say a symbol is encoded in 3 bits, we mean **3 actual bits** — not 3 characters that happen to be `'0'` or `'1'`.

If you write the string `"111"` to a file, you've written **3 bytes** (24 bits) — the ASCII codes for the character `'1'` three times (0x31, 0x31, 0x31). That saves nothing. That's worse than the original.

Real compression packs bits into bytes like a cargo container:

```
Codes:    A=0   B=100   (encoding "ABBA")

Bits:     0 | 100 | 100 | 0
Packed:   0100 1000   (padded to a full byte)
= 0x48   (1 byte written to disk)
```

You accumulate bits in a buffer, and only write to disk when you have a full byte (or flush with padding at the end). This is why Huffman implementations use bitwise operations — `<<`, `>>`, `|`, `&` — and why the output file is not human-readable. The savings are real, but they only exist if you're packing bits, not printing characters.

---

## History — The Grad Student Who Beat His Professor

In 1951, David Huffman was a Ph.D. student at MIT taking a course from **Robert Fano** — one of the founders of information theory, and co-creator of **Shannon-Fano coding**, which was the best known method at the time.

Fano gave his class an unusual final exam: instead of a written test, students could either take the exam or write a term paper on an open problem — how to construct the most efficient binary code possible. Fano himself had worked on this problem and hadn't fully solved it. Shannon-Fano coding was good but not proven optimal.

Huffman spent months on it, got stuck, and was about to give up and take the exam instead. Then came the insight: **Shannon-Fano built the tree top-down** (splitting the symbol set in half repeatedly). Huffman tried **bottom-up** — start with the least frequent symbols, merge them first, work up to the root. This greedy inversion turned out to be the key.

The result — published in 1952 as *"A Method for the Construction of Minimum-Redundancy Codes"* — proved that his bottom-up tree produced the **optimal prefix code** for any set of symbol frequencies. Huffman had not only solved the problem, he had solved it better than his professor.

Fano was gracious about it. The algorithm is named for the student.

---

## Variable-Length Prefix Codes — One Rule That Makes Decoding Work

The trick with variable-length codes is: **how do you know where one code ends and the next begins?**

If `A = 0`, `B = 01`, `C = 1` — then the bitstring `001` could be `A A C` or `A B`. Ambiguous. Unusable.

Huffman codes avoid this with the **prefix property**: no code is a prefix of any other code. This is automatically guaranteed by putting all symbols at **leaf nodes** of the tree. A leaf has no children, so its path can never be a prefix of another path.

Compare these two code tables for symbols A, B, C, D:

**Bad (prefix violation):**
```
A = 0
B = 01    <-- 0 is a prefix of 01 (A is a prefix of B)
C = 10
D = 11
```

**Good (prefix-free, Huffman-style):**
```
A = 00
B = 01
C = 10
D = 11
```

With a prefix-free code, you can decode a bitstring left to right, one bit at a time, walking the tree. When you hit a leaf, emit the symbol, return to root, repeat. No lookahead needed.

---

## Building a Huffman Tree — Full Walkthrough

Let's encode the string **`ABRACADABRA`** (11 characters).

### Step 1 — Count Frequencies

| Symbol | Frequency |
|--------|-----------|
| A | 5 |
| B | 2 |
| R | 2 |
| C | 1 |
| D | 1 |

### Step 2 — Build a Min-Heap (Priority Queue)

Insert all symbols as single-node trees, ordered by frequency (lowest priority = lowest frequency):

```
[ C:1, D:1, B:2, R:2, A:5 ]
```

### Step 3 — Greedily Merge

**Iteration 1:** Pull the two smallest → `C:1` and `D:1`. Merge into a parent node with frequency 1+1=2.

```
  [2]
  / \
C:1  D:1

Queue: [ B:2, R:2, [CD]:2, A:5 ]
```

**Iteration 2:** Pull `B:2` and `R:2`. Merge.

```
  [4]
  / \
B:2  R:2

Queue: [ [CD]:2, [BR]:4, A:5 ]
```

**Iteration 3:** Pull `[CD]:2` and `[BR]:4`. Merge.

```
      [6]
     /    \
   [4]   [CD]:2
   / \    /  \
 B:2 R:2 C:1  D:1

Queue: [ A:5, [BRCD]:6 ]
```

**Iteration 4:** Pull `A:5` and `[BRCD]:6`. Merge into root.

```
           [root: 11]
           /         \
         A:5         [6]
                    /    \
                  [4]   [2]
                  / \   / \
                B:2 R:2 C:1 D:1
```

### Step 4 — Read Off the Codes

Traverse root to each leaf. Left edge = `0`, right edge = `1`:

```
           [root]
           /     \
          0       1
         /         \
       A(5)        [6]
                  /    \
                 0      1
                /        \
              [4]        [2]
             /   \      /   \
            0     1    0     1
           /       \  /       \
         B(2)    R(2) C(1)   D(1)
```

| Symbol | Code | Length |
|--------|------|--------|
| A | `0` | 1 bit |
| B | `100` | 3 bits |
| R | `101` | 3 bits |
| C | `110` | 3 bits |
| D | `111` | 3 bits |

### Step 5 — Encode the String

```
A   B    R    A  C    A  D    A  B    R    A
0  100  101   0  110  0  111  0  100  101  0
```

Concatenated: `0 100 101 0 110 0 111 0 100 101 0`

That's **23 bits** total.

### Step 6 — Compare the Savings

| Encoding | Bits per symbol | Total bits | Savings |
|----------|----------------|------------|---------|
| ASCII (standard) | 8 bits each | 88 bits | — |
| Fixed 3-bit (5 symbols → ⌈log₂5⌉ = 3) | 3 bits each | 33 bits | 62% vs ASCII |
| **Huffman** | avg ≈ 2.09 bits | **23 bits** | **74% vs ASCII** |

### Step 7 — Decode (Verify It Works)

Take the bitstring `0100101011001110100101 0` and walk the tree:

```
Read 0      → leaf A. Emit A. Back to root.
Read 1      → go right
Read 0      → go left
Read 0      → leaf B. Emit B. Back to root.
Read 1      → go right
Read 0      → go left
Read 1      → leaf R. Emit R. Back to root.
... (continue)
```

Result: `ABRACADABRA`. Exactly what we started with.

---

## How Close to Optimal Is It?

Shannon's information theory defines a lower bound on how many bits per symbol any lossless code requires — the **entropy** of the source:

> H = −Σ p(x) · log₂ p(x)

For ABRACADABRA:

```
p(A) = 5/11 ≈ 0.454    contribution: 0.454 × 1.14 ≈ 0.517
p(B) = 2/11 ≈ 0.182    contribution: 0.182 × 2.46 ≈ 0.447
p(R) = 2/11 ≈ 0.182    contribution: 0.182 × 2.46 ≈ 0.447
p(C) = 1/11 ≈ 0.091    contribution: 0.091 × 3.46 ≈ 0.315
p(D) = 1/11 ≈ 0.091    contribution: 0.091 × 3.46 ≈ 0.315
```

**Shannon entropy ≈ 2.04 bits/symbol**
**Huffman average = 23/11 ≈ 2.09 bits/symbol**

Huffman is within 2.5% of the theoretical optimum. For this example. In general, Huffman is provably optimal among all **symbol-by-symbol** prefix codes.

---

## Complexity

| Operation | Complexity |
|-----------|-----------|
| Count frequencies | O(n) — one pass through input |
| Build Huffman tree | O(k log k) — k heap operations on k unique symbols |
| Generate codes | O(k) — one DFS of the tree |
| Encode input | O(n) — one pass, table lookup per symbol |
| Decode output | O(n) — one pass, one tree traversal per symbol |

`n` = length of input, `k` = number of unique symbols (≤ 256 for byte-level compression).

In practice k is small and constant, so the dominant cost is the O(n) encode/decode passes.

---

## Where Huffman Actually Lives Today

Huffman coding is rarely the only compression happening — it's almost always the **last stage** of a pipeline:

**DEFLATE** (used in ZIP, gzip, PNG):
```
Input → LZ77 (find repeated substrings) → Huffman → Compressed output
```
LZ77 finds repetitions at the byte-sequence level and replaces them with back-references. Huffman then compresses the resulting symbol stream. PNG uses this directly. ZIP/gzip use a variant.

**JPEG:**
```
Image → DCT (frequency transform) → Quantization (lossy) → Huffman → JPEG file
```
The DCT converts 8×8 pixel blocks into frequency coefficients. Quantization throws away high-frequency detail (the lossy step). Huffman compresses the remaining coefficients. The Huffman part is lossless — the loss happened earlier.

**MP3:**
```
Audio → MDCT → Psychoacoustic masking (lossy) → Huffman → MP3 file
```
Same idea: perceptual model discards what human ears can't hear, Huffman compresses the rest.

In all three: Huffman is the final entropy-coding stage. It contributes meaningfully but is not where the heavy lifting happens.

---

## Why Modern Systems Sometimes Replace It

Huffman has one structural limitation: **codes must be integer bit lengths**. A symbol with probability 0.4 has theoretical cost −log₂(0.4) ≈ 1.32 bits. Huffman must assign it 1 or 2 bits — never 1.32.

**Arithmetic coding** sidesteps this by encoding the entire message as a single number in [0, 1), achieving arbitrarily close to Shannon entropy. It's used in JPEG 2000, H.265, and modern ML compression.

**ANS (Asymmetric Numeral Systems)** — invented by Jarek Duda around 2014 — achieves arithmetic-coding efficiency with near-Huffman speed. It's now used in zstd (Facebook), LZFSE (Apple), and modern GPU compression.

Huffman remains in widespread use because:
- It's simple to implement correctly
- It's fast (table lookup, no arithmetic)
- For many real-world distributions, the integer-length penalty is small
- Decades of optimized implementations exist everywhere

---

## The Algorithm's Place in the Bigger Picture

Huffman sits at the intersection of several ideas worth understanding:

- **Greedy algorithms** — the merging strategy is greedy and provably optimal (exchange argument proof)
- **Priority queues / heaps** — the min-heap is what makes the construction O(k log k)
- **Binary trees** — the tree IS the code; its structure determines every code length
- **Information theory** — Shannon entropy is the target; Huffman is one of the cleanest algorithms that provably approaches it

It's not the state of the art. But it's one of those rare algorithms where the core idea, the implementation, the proof of optimality, and the practical impact are all accessible at the same time. That's why it's still taught.
