// ------------------------------
// Structure interface
// Plug your DS behind this.
// ------------------------------

#pragma once

#include "counters.hpp"

class Structure {
public:
    virtual ~Structure() = default;
    virtual const char *name() const = 0;

    virtual void reset() = 0;
    virtual void reset_counters() = 0;
    virtual Counters counters() const = 0;

    virtual void insert(int x) = 0;
    virtual void erase(int x) = 0;
    virtual bool contains(int x) = 0;
};