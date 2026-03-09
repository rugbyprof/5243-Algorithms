#include "termcolor.hpp"
#include <algorithm>
#include <iomanip> // where setw is declared
#include <iostream>
#include <string>
#include <vector>

struct Option {
    std::string flag;
    std::string arg;
    std::string desc;
};

class UsagePrinter {
private:
    std::vector<Option> options;

public:
    void add(std::string flag, std::string arg, std::string desc) {
        options.push_back({flag, arg, desc});
    }

    void print(const std::string &programName) {

        using namespace termcolor;

        std::cout << bold << "Usage:\n"
                  << reset;
        std::cout << "  " << bold << programName << reset
                  << " " << cyan << "[OPTIONS]\n\n"
                  << reset;

        std::cout << bold << "Options:\n"
                  << reset;

        size_t flagWidth = 0;
        size_t argWidth = 0;

        for (auto &o : options) {
            flagWidth = std::max(flagWidth, o.flag.size());
            argWidth = std::max(argWidth, o.arg.size());
        }

        for (auto &o : options) {

            std::cout << "  "
                      << cyan << std::left
                      << std::setw(flagWidth) << o.flag
                      << reset << " ";

            if (!o.arg.empty()) {
                std::cout << yellow
                          << std::setw(argWidth) << o.arg
                          << reset;
            } else {
                std::cout << std::setw(argWidth) << " ";
            }

            std::cout << "   " << o.desc << "\n";
        }

        std::cout << "\n";
    }
};