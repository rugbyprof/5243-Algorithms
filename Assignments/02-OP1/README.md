## Program 1 - Vector Class
#### Due: Optional Program

## Overview

Getting help from [Lecture 04](../../Lectures/05-Vector_Starter/main.cpp)  create a linked list based `Vector` class that will include the functionality listed below. You will achieve this by writing additional methods to add values, remove values, and maintain sorted values if needed. This class also needs the ability to be initialized with different data sources (files, other vectors, and arrays).

I'll give some basic linked list code to help, 

## Requirements

- Your class will be a basic container type of integers that can grow or shrink easily without the need to copy values over to newly allocated memory when resizing (I will explain this more in class).
- Initializing your class instance:
  - From an array
    - `V1 = new (int *A, int size)` : *adds each item from an array type*
  - From a file 
    - `V1 = new Vector(string FileName)` : *read until eof loading each value into list* 
  - From another instance of same type 
    - `V2 = new Vector(Vector V1)` : *traverse* `other.list` *adding each value to* `this.list`
- Adding items to your class instance:
  - To the front
    - `V.pushFront(int val)` : *adds single value to front of* `this.list`
    - `V.pushFront(Vector V2)`: *adds entire* `other.list` *to front of* `this.list`
  - To the rear
    - `V.pushRear(int val)` : *adds single value to rear of* `this.list`
    - `V.pushRear(Vector V2)` : *adds entire* `other.list` *to rear of* `this.list`
  - At a specified location (if it exists)
    - `V.pushAt(int loc,int val)`
  - In ascending or descending order (order set by constructor or setter)
    - `V.inOrderPush(int val)` : *adds single value to proper location in order to maintain order (ascending or descending)*
    - This requires the list to be sorted from the beginning. We can discuss this more in class.
- Removing items from a class instance:
  - From the front
    - `val = V.popFront()` : *removes single value from front of list*
  - From the rear
    - `val = V.popRear()` : *removes single value from rear of list*
  - A specified location
    - `val = V.popAt(int loc)` : *removes single value from an indexed location if index between* `0 and size of list -1`
  - By a search than removal (if it exists)
    - `loc = V.find(int val)`  : *find location of item (index) if it exists*
    - `val = V.popAt(int loc)`) : *then use index to remove item*
- Printing
  - Output should look similar to: [v<sub>1</sub>, v<sub>2</sub>, v<sub>3</sub>, ... , v<sub>n</sub>]
 

## Tests

Run this code with your class and make sure you get same output. The example below is writing to stdout only. I want your test program to write to stdout AND a file called `test.out`. Your name, date and course (Fall 2143) should be written at top of output file (with your code):

**Example Output File (portion of)**
```
Name
Date
Fall 2143

[25, 20, 18, 18, 20, 25]
[11, 25, 33, 47, 51]
[9, 11, 25, 27, 33, 47, 51, 63]
[25, 20, 18, 18, 20, 25, 9, 11, 25, 27, 33, 47, 51, 63]
etc...
```

**Example Code Run**
```cpp

int x = 0;

Vector v1;
v1.pushFront(18);
v1.pushFront(20);
v1.pushFront(25);
v1.pushRear(18);
v1.pushRear(20);
v1.pushRear(25);
v1.print();
// [25, 20, 18, 18, 20, 25]

int A[] = {11,25,33,47,51};
Vector v2(A,5);
v2.print();
// [11, 25, 33, 47, 51]

v2.pushFront(9);
//v2.inOrderPush(27);
v2.pushRear(63);
v2.print();
// [9, 11, 25, 33, 47, 51, 63]

v1.pushRear(v2);
v1.print();
// [25, 20, 18, 18, 20, 25, 9, 11, 25, 33, 47, 51, 63]

x = v1.popFront();
x = v1.popFront();
x = v1.popFront();
v1.print();
// [18, 20, 25, 9, 11, 25, 27, 33, 47, 51, 63]
cout<<x<<endl;
// 18

x = v1.popRear();
x = v1.popRear();
x = v1.popRear();
v1.print();
// [18, 20, 25, 9, 11, 25, 27, 33]
cout<<x<<endl;
// 47

x = v2.popAt(3);
v2.print();
// [9, 11, 25, 33, 47, 51, 63]
cout<<x<<endl;
// 27

x = v2.find(51);
cout<<x<<endl;
// 5

x = v2.find(99);
cout<<x<<endl;
// -1

Vector v3(v1);
v3.print();
// [18, 20, 25, 9, 11, 25, 27, 33]

v3.pushFront(v2);
v3.print();
//[9, 11, 25, 33, 47, 51, 63, 18, 20, 25, 9, 11, 25, 27, 33]

Vector v4("input.dat");
v4.pushRear(v3);
v4.print();
// [56, 61, 97, 66, 83, 25, 26, 11, 53, 49, 62, 18, 10, 18, 14, 3, 4, 23, 18, 24, 26, 27, 54, 14, 12, 45, 65, 98, 56, 97, 15, 84, 98, 9, 11, 25, 33, 47, 51, 63, 18, 20, 25, 9, 11, 25, 27, 33]
```

### Deliverables

- Create a folder in your assignments folder called `P01`
- In that folder create a file called README.md
- Help with markdown: https://guides.github.com/features/mastering-markdown/
- Look at [this](../../Resources/02-Readmees/README.md) to help with your `README.md` file
- Create a banner for your program **(see [HERE](../../Resources/03-Banner/README.md))**.

```
2143 
P01
Name
```

- Print out your source code. Make sure it's **[commented](../../Resources/01-Comments/README.md)**.
- Print out your output file.
- Put your assignment on the lecture podium at the beginning of class.
- Staple everything in this order:
  - **1)** Banner (on top)
  - **2)** Source code (middle)
  - **3)** Output (bottom)
- Any hand writing on your assignment is reduction in 1 letter grade.
- Failure to follow instructions is a reduction in 1 letter grade.

