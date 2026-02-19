# 📘 Algorithms Exam — Design the Container + Choose the Algorithm
```latex
\documentclass[11pt]{exam}
\usepackage{amsmath, amssymb}
\usepackage{enumitem}
\usepackage{geometry}
\geometry{margin=1in}

\title{Algorithms — Container Design \& Algorithm Selection}
\author{}
\date{}

\begin{document}
\maketitle

\instructions{
Answer all questions.
You must justify your design choices.
Big-O without explanation earns limited credit.
Diagrams are encouraged if they clarify reasoning.
}
```

---

## Question 1 — Priority Matters (25 points)

```latex
\section*{Question 1 — Priority Matters (25 points)}
```

You are designing a system that processes jobs with the following properties:

- Each job has:
  - an ID
  - a priority (integer)
  - a timestamp
- The system must:
  - Insert new jobs frequently
  - Always process the **highest priority job next**
  - Occasionally change the priority of an existing job

### Tasks

```latex
\begin{parts}
\part (5 pts) What abstract data structure best models this problem?
\part (5 pts) Choose a concrete container implementation.
\part (5 pts) Choose the primary algorithm(s) used for insertion and removal.
\part (5 pts) State the time complexity for:
\begin{itemize}
  \item insertion
  \item removal
\end{itemize}
\part (5 pts) Explain why a singly linked list with sorted insertion is inferior.
\end{parts}
```

**Instructor intent:**  
This question is fishing for **binary heap + array-based implementation**  
and punishes students who confuse *correctness* with *efficiency*.

---

## Question 2 — Undo, But Make It Efficient (20 points)

```latex
\section*{Question 2 — Undo, But Make It Efficient (20 points)}
```

You are implementing an **undo system** for a text editor.

Requirements:
- Undo operations must occur in **reverse order**
- Undo must be fast
- Redo support is not required (for now)

### Tasks

```latex
\begin{parts}
\part (5 pts) What data structure is most appropriate?
\part (5 pts) Describe the invariant of this structure.
\part (5 pts) State the time complexity of undo.
\part (5 pts) Explain why a queue would be a poor choice.
\end{parts}
```

**Instructor intent:**  
This should be a slam-dunk **stack**, but the explanation reveals who actually understands LIFO.

---

## Question 3 — Fast Search, Rare Updates (25 points)

```latex
\section*{Question 3 — Fast Search, Rare Updates (25 points)}
```

You are given a dataset of **1 million integers**.

Constraints:
- The data is loaded once at startup
- Searches are extremely frequent
- Insertions and deletions are rare
- Memory locality matters

### Tasks

```latex
\begin{parts}
\part (5 pts) Choose a container.
\part (5 pts) Choose a search algorithm.
\part (5 pts) State the time complexity of search.
\part (5 pts) Explain why this design favors cache performance.
\part (5 pts) Explain why a linked list is unacceptable.
\end{parts}
```

**Instructor intent:**  
Array + **binary search**.  
Any mention of “linked list search” should cause visible concern.

---

## Question 4 — Traversal With Intent (15 points)

```latex
\section*{Question 4 — Traversal With Intent (15 points)}
```

You are working with a **binary search tree**.

Tasks:
- Output all values in sorted order
- Delete the entire tree safely from memory

### Tasks

```latex
\begin{parts}
\part (5 pts) Which traversal produces sorted output?
\part (5 pts) Which traversal should be used to delete the tree?
\part (5 pts) Explain why using the wrong traversal is dangerous.
\end{parts}
```

**Instructor intent:**  
This is where inorder vs postorder becomes **life and death**, not trivia.

---

## Question 5 — Graph Reality Check (15 points)

```latex
\section*{Question 5 — Graph Reality Check (15 points)}
```

You are given a **sparse graph** with:
- Millions of vertices
- Very few edges per vertex

Tasks:
- Traverse the entire graph
- Detect cycles

### Tasks

```latex
\begin{parts}
\part (5 pts) Choose a graph representation.
\part (5 pts) Choose a traversal algorithm.
\part (5 pts) State the time complexity in terms of $V$ and $E$.
\end{parts}
```

**Instructor intent:**  
Adjacency list + DFS + \(O(V + E)\).  
Matrices should be publicly shamed.

---

## Question 6 — Design Judgment (Bonus 10 points)

```latex
\section*{Question 6 — Design Judgment (Bonus 10 points)}
```

You may answer **one** of the following:

- Describe a situation where:
  - A worse asymptotic complexity is acceptable
- OR
- Explain why Big-O alone is insufficient to choose a data structure

Clarity > length.

---

```latex
\end{document}
```
