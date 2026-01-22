#include <iostream>

using namespace std;

// singly linked list (one pointer)
// two pointers implies (doubly linked list)
// N pointers implies ??
struct Node{
    // data stuff here
    int data;
    Node* next;
    Node(int data):data(data),next(nullptr){}
};

class LinkedList{
protected:
    Node* head;
    Node* tail;
    void endPush(int x){
        // handle
        Node* temp = new Node(x);
        
        if(!head){
            // list is empty
            head = tail = temp;
        }else{
            // list is not empty
            tail->next = temp;
            tail = temp;

        }
    }
    void frontPush(int x){
        // handle
        Node* temp = new Node(x);
        
        if(!head){
            // list is empty
            head = tail = temp;
        }else{
            // list is not empty
            temp->next = head;
            head = temp;

        }
    }
public:
    LinkedList():head(nullptr),tail(nullptr){}
    void print(){
        Node* travel = head;
        while(travel){
            cout<<"["<<travel->data<<"]";
            if(travel->next){
                cout<<"->";
            }
            travel = travel->next;
        }
    }
};

class OrderedList: public LinkedList{
    public:
    void push(int x){
        if(!head){
            frontPush(x);
        }else{
            if(x <= head->data){
                frontPush(x);
            }else if(x >= tail->data){
                endPush(x);
            }else{
                Node* temp = new Node(x);
                // ordered part
                Node* travel = head;
                while(temp->data > travel->next->data){
                    travel = travel->next;
                }
                // insert now
                temp->next = travel->next;
                travel->next = temp;
            }
        }
    }
};

int main(int argc, char** argv){
    OrderedList L;
    // L.endPush(1);
    for(int i=0;i<10;i++){
        L.push(rand()%1000);
    }
    // L.endPush(99);
    L.print();
    cout<<endl;

    return 0;
}