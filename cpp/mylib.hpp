#pragma once
#include <string>
#include <vector>

namespace demo {

int add(int a, int b) noexcept;

double mean(const std::vector<double>& xs);

std::string greet(const std::string& name);

}
