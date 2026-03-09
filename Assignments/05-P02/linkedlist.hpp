#pragma once

#include "counters.hpp"
#include "statsInterface.hpp"

#include "json.hpp"
#include <fstream>
#include <iostream>
#include <string>

using namespace std;
using json = nlohmann::json;

// Node for our linked list
struct Node {
    unsigned long val; // val value (could be a lot more values)

    Node *next; // we always need a "link" in a linked list

    Node(unsigned long val) : val(val) {} // cunstructor to make adding values easy
    friend ostream &operator<<(ostream &os, const Node *item) {
        return os << "[" << item->val << "]";
    }
};

// virtual ~StatsInterface() = default;
// virtual const char *name() const = 0;

// virtual void reset() = 0;
// virtual void reset_counters() = 0;
// virtual Counters counters() const = 0;

// virtual bool insert(int x) = 0;
// virtual bool erase(int x) = 0;
// virtual bool contains(int x) = 0;

class LinkedList : public StatsInterface {
private:
    Node *head; // base pointer of list
    Node *tail;
    int size;

    void _print(Node *travel) {
        while (travel) {
            cout << travel << endl;
            travel = travel->next;
        }
    }

    void _print(Node *travel, string filename) {
        ofstream fout(filename);
        while (travel) {
            fout << travel << "->" << endl;
            travel = travel->next;
        }
    }

public:
    const char *name() {
        return "LL";
    }

    void reset() {
    }

    void reset_counters() {
    }

    bool insert() {
    }

    bool erase() {
    }

    bool contains() {
    }

    LinkedList() : head(nullptr), tail(nullptr), size(0) {}

    void print(string filename = "") {
        if (filename.size() > 0) {
            this->_print(head, filename);
        } else {
            this->_print(head);
        }
    }
    void pushFront(unsigned long val) {
        Node *tempPtr = new Node(val); // create a new Node and
                                       // add val to it

        if (!head) { // `!head` implies empty list
                     // So does `head == NULL`

            head = tail = tempPtr; // `head = tempPtr` places addrress of
                                   // tempPtr in head (points head to tempPtr)

        } else {                  // list not empty
            tempPtr->next = head; // point tempPtr's next to what head points to
            head = tempPtr;       // now point head to tempPtr
        }
        this->size++;
    }

    void pushRear(unsigned long val) {
        Node *tempPtr = new Node(val); // create a new Node and
                                       // add val to it
        if (!head) {                   // `!head` implies empty list
                                       // So does `head == NULL`

            head = tail = tempPtr; // `head = tempPtr` places addrress of
                                   // tempPtr in head (points head to tempPtr)

        } else {
            tail->next = tempPtr; // point tempPtr's next to what head points to
            tail = tempPtr;       // now point head to tempPtr
        }
        this->size++;
    }

    bool delete_node(unsigned long key) {

        if (key == head->val) {
            Node *killer = head;
            head = head->next;
            delete killer;
            return true;
        }

        Node *travel = head;
        Node *chaser = head;

        while (travel && travel->val != key) {
            chaser = travel;
            travel = travel->next;
        }
        if (travel) {
            Node *killer = travel;
            chaser->next = travel->next;
            delete killer;
            return true;
        }
        return false;
    }

    friend ostream &operator<<(ostream &os, const LinkedList &rhs) {
        Node *temp = rhs.head; // temp pointer copies head

        while (temp) { // this loops until temp is NULL
                       // same as `while(temp != NULL)`

            os << temp->val; // print val from Node
            if (temp->next) {
                os << "->";
            }
            temp = temp->next; // move to next Node
        }
        os << endl;
        return os;
    }

    bool find(unsigned long key) {
        Node *travel = head; // temp pointer copies head

        while (travel) { // this loops until temp is NULL

            if (travel->val == key) {
                return true;
            }

            travel = travel->next; // move to next Node
        }

        return false;
    }

    int getSize() {
        return this->size;
    }

    void loadLLViaStdin() {
        json j;
        while (cin >> j) {
            cout << j << endl;
            // cout << j['op'] << j['value'] << endl;
            // this->pushRear(long(j['value']));
        }
    }

    ~LinkedList() {
    }
};
