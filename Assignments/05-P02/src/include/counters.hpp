// ------------------------------
// Counters: what Python expects
// ------------------------------

#pragma once

struct Counters {
    long long comparisons = 0;
    long long structural_ops = 0;
    long long inserts = 0;
    long long deletes = 0;
    long long lookups = 0;
    long long resize_events = 0;
};