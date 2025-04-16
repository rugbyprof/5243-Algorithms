- A balanced tree is a binary tree where the height difference between left and right subtrees differs by no more than?

Ans: 1 level

- What advantages do simple BST's have over balanced trees?

Ans: Lower overhead

- Worse case performance for a BST that does not incorporate rotations to maintain balance?

Ans: $O(n)$

- The **\*\***\_\_**\*\*** tree has slightly faster inserts/deletes on average, but **\*\*\*\***\_\_\_**\*\*\*\*** trees are more strictly balanced and better for read-heavy workloads.

Ans: Red Black Trees , Avl Trees

- At worst case, while each rotation is O(1), total overhead for an insertion or deletion can reach **\*\***\_\_\_\_**\*\***?

Ans: $O(lg n)$

- Every AVL tree is a binary search tree.

Ans: True because ...

- What is the maximum allowed balance factor of a node in an AVL tree?

Ans: abs(1)

- After inserting into an AVL tree, the balance factor of a node is –2. What type of rotation is needed?

Ans: It depends on the left or right subtree.

- Why might AVL trees perform better than Red-Black trees for search-heavy applications?

Ans: They are more strictly balanced than red black trees.

- What is the worst-case height of an AVL tree with n nodes?

Ans: $O(lg N)$

- $O(V^2)$, where V is the number of vertices, as it stores potential edges even if they don't exist.

Ans: Matrix implementation of a Graph

- Efficient for checking the existence of edges.

Ans: Matrix implementation of a Graph

- Suitable for dense graphs (graphs with many edges).

Ans: Matrix implementation of a Graph

- $O(V + E)$, where $V$ is the number of vertices and $E$ is the number of edges, making it more space-efficient for sparse graphs.

Ans: List Implementation

- When you need to iterate over the neighbors of a vertex frequently.

Ans: List Implementation

- When the graph is sparse.

Ans: List Implementation

- A graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex from one set to the other.

Ans: Bipartite Graph

- How can we detect if graphs have certain features? Fully connected, cycles, bipartite?

Ans: BFS or DFS with a coloring method can check bipartiteness

- This data structure seems to be rarely implemented, but is referenced in many other algorithms (like Dijkstra's) when discussing best performance:

Ans: Fibonacci Heap

- Limitations of dijkstras

Ans: Negative edge weights
