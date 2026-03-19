// ------------------------------
// Counters: what Python expects
// ------------------------------

#pragma once
#include <iostream>

using namespace std;

struct Counters {
    long long comparisons = 0;
    long long structural_ops = 0;
    long long inserts = 0;
    long long deletes = 0;
    long long lookups = 0;
    long long resize_events = 0;
    friend ostream& operator <<(ostream& os, const Counters &o){
        return os <<"Comp:"<<o.comparisons<<" Ops:"<<o.structural_ops<<" Inserts: "<<o.inserts<<std::endl;
    }
};