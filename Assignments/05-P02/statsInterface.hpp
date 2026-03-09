// ------------------------------
// Structure interface
// Plug your DS behind this.
// ------------------------------

#pragma once

#include "counters.hpp"

class StatsInterface {
public:
    virtual ~StatsInterface() = default;
    virtual const char *name() const = 0;

    virtual void reset() = 0;
    virtual void reset_counters() = 0;
    virtual Counters counters() const = 0;

    virtual bool insert(int x) = 0;
    virtual bool erase(int x) = 0;
    virtual bool contains(int x) = 0;
};