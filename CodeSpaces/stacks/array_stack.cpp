#include <iostream>

using namespace std;

struct Node{
    // hello
};

// LIFO
struct Stack{
private:
    int *stack;
    int top;
    int size;
    bool full(){
        return top <= size-1;
    }
    bool empty(){
        return top >= 0;
    }
public:
    Stack():stack(new int[10]),top(-1),size(10){}
    Stack(int size):stack(new int[size]),top(-1),size(size){}
    void push(int x){

        if(!full()){
             top++;
            stack[top] = x;
        }
    }

    int pop(){
        if(!empty()){
            int x = stack[top];
            top--;
            return x;
        `}else{
            cout<<"empty"<<empty;
        }
        return -9999999;
    }

    void print(){
        for(int i=top;i>=0;i--){
            cout<<stack[i]<<" ";
        }
        cout<<endl;

    }

};

class ListStack{

};

int main(int argc, char** argv){
    Stack stack;
    stack.push(4);
    stack.push(11);
    stack.pop();
    stack.push(76);
    stack.pop();
    stack.pop();
    stack.pop();
    stack.print();
}

