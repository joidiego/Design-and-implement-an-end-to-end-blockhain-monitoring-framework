#pragma once
#include <vector>
#include <string>

struct ECDSASignature
{
    std::string r;
    std::string s;
};

std::vector<ECDSASignature> parse_signatures(const std::vector<unsigned char> &tx);