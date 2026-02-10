## Refresher

- Stacks
- Queues
- List Based Structures
- Array Based Structures

## Recursion V Iteration
- Trees
- Graphs

## Graphs

- G=(V,E)
- InDegree
- OutDegree
- Vertex 
- Edge
- Weighted Edge
- Cycle
- Undirected
- Directed
- List Based v Array Based
- Source
- Sink 
- Destination
- Bread First Search (Queue)
- Depth First Search  (Stack)
- Sparse Graph
- Dense Graph
- Fully Connected
- Bipartite
- Forest
- Graph Complexity and Max Nodes and Edges


## Trees

- Recursive Traversal v Iterative Traversal
- List Based V Array Based
- Tree Definition 
- As Relates To Graph
- Spanning Tree
- Minimum Spanning Tree
- Height
- Balanced Definition
- Path
- Tree Complexity and Max Nodes and Edges
- Tree Traversals
  - Pre
  - Post
  - In
  - Benefits or reasons for each traversal
  - Which traversal lets you rebuild a binary tree when written to a file?
- Deleting a Value
- InOrder Successor
- InOrder Predecessor

## Array Based Trees

- Problems With Sparse Trees
- When are Array Based Trees Good
- Formulas: 
  - Parent
  - Left Child
  - Right Child

## Binary Search

- Complexity
- Non Sorted Values
- Algorithm
  - Generic V Speedups

## Big Picture

Up to now, the big picture for me is to:
1. Have reviewed list based and array based stacks and queues because I feel that they are a good litmus test and represent a type of backbone for many other more complex algorithms.

2. I try and differentiate data structures v algorithms and their relationship. I also like to use the word algorithm as applied to a specific container type to reinforce the fact that one needs the other since it's the container that has it's pros and cons while the algorithm has the rules to be followed when performing generic container operations (insert, delete, search , update).

3. My progression is to discuss:
   - Stack and Queues
   - Trees
   - Binary Trees (structure only rules)
   - Binary Search Trees (structure + algorithm to have ordered values)
   - Graphs (mostly to introduce Tree's as a type of graph at this point)
   - Array Based v List Based pros and cons
   - Introduced binary search as it pairs nicely with Binary Search Tree's and Array Based Binary Trees
   - This relationship lets me then lets me get into Binary Heap because we now have all the building blocks to put that type of priority queue together.
   - I show how a singly linked list with push pop operations can also implement a priority queue, but not as efficient as a binary heap
   - Heap Properties
     - Not a total ordering
     - Rules are parent must be larger (max) or smaller (min) than the children. 
     - No total ordering
     - Complexity of:
       - Insert
       - Removal
       - Heapify
     - Array Based Binary heap maintains:
       - A Complete tree which fits well into an array based implementation
     - Heapify is the power house behind heap sort or turning an array of items into a heap. 