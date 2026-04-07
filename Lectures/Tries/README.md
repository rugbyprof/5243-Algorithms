## Trie - Not A Tree (but it is...)

#### Due: N/A

Thanks Chat Gpt (with many fixes):

### First Explanation:

A `Trie` data structure, also known as a `prefix tree`, is a tree-like data structure used for efficient string matching and retrieval operations. The Trie structure represents a set of strings as a tree in which each node represents a prefix or complete string, with the root of the tree representing the empty string.

A `Trie` is typically used in situations where we need to store a large set of strings and perform operations such as searching for a string or finding all strings that share a common prefix. Tries can be used in various applications such as `spelling correction`, `autocomplete`, and `DNA sequence analysis`.

### Second Explanation:

A `Trie` is a tree-like data structure used for storing and searching strings efficiently. Each node in the Trie represents a prefix or complete string, with the root representing the empty string. Each edge leaving a node represents a character, and the path from the root to a leaf represents a complete string stored in the Trie.

A `Trie` can be used for a variety of applications, such as:

1. **Autocomplete**: A Trie can be used to efficiently search for all words in a dictionary that start with a given prefix. This is often used in search engines and text editors to provide autocomplete suggestions to users.
2. **Spell checking**: A Trie can be used to check if a given word is spelled correctly. This is often used in word processors and other applications that require spelling and grammar checking.
3. **IP routing**: A Trie can be used to efficiently route packets in a computer network. Each node in the Trie represents a portion of an IP address, and the path from the root to a leaf represents the route to a particular network.

---

### Why Is It Called a "Trie"?

The name comes from the word re**trie**val — making the full name a "retrieval tree." It's officially pronounced **"try"** (to distinguish it from "tree"), yet it absolutely is a tree. That's the joke in the title.

---

### Visualizing a Trie

Insert the words: `app`, `apt`, `apple`, `apply`

```
              [root]
                |
               (a)
                |
               (p)
              /   \
            (p)   (t)
           * |     *        <-- "app", "apt"
            (l)
           /   \
         (e)   (y)
          *     *           <-- "apple", "apply"
```

Every path from root to a `*` node spells a complete word. Nodes are **shared** — `app`, `apple`, and `apply` all travel the same `a→p→p` path before branching. That shared prefix storage is the whole point.

---

### Why Not Just Use a Hash Map?

A hash map is great for exact lookups, but falls apart for prefix queries:

| Operation | Hash Map | Balanced BST | Trie |
|-----------|----------|--------------|------|
| Insert | O(k) avg | O(k log n) | O(k) |
| Exact search | O(k) avg | O(k log n) | O(k) |
| **Prefix search** | **O(k · n)** | O(k log n + output) | **O(k + output)** |
| Delete | O(k) avg | O(k log n) | O(k) |

> `k` = length of the string, `n` = number of strings stored

To find all words starting with `"app"` in a hash map you'd have to scan every key. In a Trie you just walk three edges and collect everything below. That's why autocomplete uses Tries.

---

### Real-World Applications — In Depth

---

#### Autocomplete vs. Suggestions (they're not the same thing)

These two terms get conflated, but they're solving different problems:

- **Autocomplete** — there is one right answer. Your IDE completes `std::vec` → `std::vector`. A terminal completes a filename. The Trie finds the prefix, returns everything below it, and you pick the only (or first) match.
- **Suggestions** — there are many possible answers and they need to be *ranked*. This is what Google does.

Google's search bar is often called autocomplete but it's really a **suggestion engine**. When you type `"algo"`, a Trie (or similar index) finds millions of queries that start with `"algo"` — that's the easy part. The hard part is deciding which 8 to show you. Google ranks candidates using a black box that factors in global query frequency, your personal search history, location, trending topics, and ML models trained on billions of queries. The Trie handles "find the candidates"; everything after that is outside the Trie's job.

**The honest picture:**

```
User types "algo"
       |
       v
  [Trie lookup]  <-- O(4 edges)
       |
       v
  Subtree of all queries starting with "algo"
  (could be millions)
       |
       v
  [Ranking / scoring]  <-- NOT a Trie problem
       |
       v
  Top 8 suggestions shown
```

A simpler autocomplete (phone contacts, IDE symbols) skips the ranking step entirely and just returns the subtree.

---

#### IP Routing — Longest Prefix Match

This is one of the cleanest Trie applications because the structure maps perfectly.

Every IP address is 32 bits (IPv4). A routing table entry looks like `192.168.1.0/24` — the `/24` means "the first 24 bits must match; the last 8 can be anything." These are called **CIDR blocks**.

Build a **binary Trie** where each level represents one bit of the address:

```
Routing table:
  10.0.0.0/8       (match if first 8 bits = 00001010)
  10.20.0.0/16     (match if first 16 bits = 00001010 00010100)
  10.20.30.0/24    (match if first 24 bits = ...)

Binary Trie (first few levels):
          [root]
          /    \
        (0)    (1)
        ...   /   \
            (0)   (1)
            ...
           /
         (0)   <-- end of 8 bits: mark "10.0.0.0/8 route" here
         ...
```

For each incoming packet the router walks the Trie **bit by bit** and tracks the last node that had a valid route entry. When the walk ends, the deepest match wins — this is the **longest prefix match** rule. More specific routes (longer prefix = narrower CIDR) always beat broader ones.

- Cost: O(32) for IPv4, O(128) for IPv6 — completely independent of how many routes are in the table
- Without a Trie: O(n) scan of the routing table for every packet — unacceptable at line rate

This is why every production router uses a hardware Trie (called a **TCAM** — Ternary Content Addressable Memory) to do longest prefix match in a single clock cycle.

---

#### Spell Check — Detection is Easy, Suggestions are Hard

Spell checking has two distinct phases and a Trie only directly solves the first one.

**Phase 1 — Detection:** Is this word in the dictionary?
- Trie exact-match lookup: O(k) where k = word length. Done.

**Phase 2 — Suggestion:** The word isn't there. What did they mean?
- This is an **edit distance** problem. The standard metric is **Levenshtein distance** — the minimum number of single-character insertions, deletions, or substitutions to transform one string into another.
- `"recieve"` → `"receive"`: distance 1 (swap i and e)
- `"teh"` → `"the"`: distance 1 (transpose t and h... actually Levenshtein counts this as 2; Damerau-Levenshtein adds transpositions as distance 1)

One practical approach that combines Tries with edit distance:

```
For a misspelled word W:
  1. Generate all strings within edit distance 1 of W
     (deletions, insertions, substitutions — this is a finite set)
  2. Look each candidate up in the Trie
  3. Return the ones that exist in the dictionary
```

Edit distance 1 from a length-k word generates O(54k) candidates (26 substitutions × k positions + deletions + insertions). Each Trie lookup is O(k). Total: O(k²) — fast enough to run on every keystroke.

More sophisticated checkers use **BK-trees** (a metric tree built on Levenshtein distance) which let you query "all dictionary words within distance d of W" directly without enumerating candidates. Modern production spell checkers (phones, browsers) layer ML models on top for context-aware correction ("duck" → probably meant something else).

---

Both coding examples below serve nearly the same purpose, load some words then search using a partial string match. I have plenty of data for you to do much more even in this directory! Look [HERE](dictionary.txt)

The Chat GPT code looks skimpy so if you want a full born implementation, go [HERE](https://replit.com/@rugbyprof/3013TrieSpring2021-1) and look at this code!!

```cpp

#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

using namespace std;

class Trie {
private:
    unordered_map<char, Trie*> children;
    bool is_end;

public:
    Trie() {
        is_end = false;
    }

    void insert(string word) {
        Trie* node = this;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new Trie();
            }
            node = node->children[c];
        }
        node->is_end = true;
    }

    vector<string> search(string prefix) {
        Trie* node = this;
        for (char c : prefix) {
            if (node->children.find(c) == node->children.end()) {
                return vector<string>();
            }
            node = node->children[c];
        }
        return find_words(node, prefix);
    }

    vector<string> find_words(Trie* node, string prefix) {
        vector<string> res;
        if (node->is_end) {
            res.push_back(prefix);
        }
        for (auto it : node->children) {
            char c = it.first;
            Trie* child = it.second;
            vector<string> words = find_words(child, prefix + c);
            res.insert(res.end(), words.begin(), words.end());
        }
        return res;
    }
};

int main() {
    vector<string> words = {"apple", "banana", "orange", "pear", "peach"};
    Trie* trie = new Trie();
    for (string word : words) {
        trie->insert(word);
    }
    string prefix = "p";
    vector<string> results = trie->search(prefix);
    cout << "Words with prefix '" << prefix << "': ";
    for (string word : results) {
        cout << word << " ";
    }
    cout << endl;
    return 0;
}
```

```cpp
#include <iostream>
#include <unordered_map>

using namespace std;

class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool is_word;

    TrieNode() {
        is_word = false;
    }
};

class Trie {
private:
    TrieNode* root;

public:
    Trie() {
        root = new TrieNode();
    }

    void insert(string word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (curr->children.find(c) == curr->children.end()) {
                curr->children[c] = new TrieNode();
            }
            curr = curr->children[c];
        }
        curr->is_word = true;
    }

    bool search(string word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (curr->children.find(c) == curr->children.end()) {
                return false;
            }
            curr = curr->children[c];
        }
        return curr->is_word;
    }
};

int main() {
    Trie trie;
    trie.insert("apple");
    trie.insert("banana");
    trie.insert("orange");
    trie.insert("pear");

    if (trie.search("apple")) {
        cout << "Found apple in the Trie!" << endl;
    }

    return 0;
}
```

In this example, we created a `Trie` data structure that used a `TrieNode class` to represent the nodes of the Trie. We use an unordered_map to store the child nodes for each node in the Trie. We also define two methods, `insert` and `search`, to insert words into the Trie and search for words in the Trie, respectively.

As a real-world example, we could use this Trie to implement `autocomplete functionality` in a `search engine` or `text editor`. When a user types a prefix, we can use the search method to find all words in the Trie that start with that prefix and suggest them as autocomplete options to the user.
