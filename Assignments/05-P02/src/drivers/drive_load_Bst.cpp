#include "bst.hpp"
#include <iostream>
#include <string>

using namespace std;

int main(int argc,char**argv) {
    Bst tree;

    if(argc < 2){
        cout<<"Error: You need a filename!"<<endl;
        cout<<"Usage: ./dbst ../work_files/workload_A_1000.json"<<endl;
    }

    tree.runJobFile(argv[1]);
}