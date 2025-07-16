#include "stats_engine.h"
#include <cmath>
#include <deque>
#include <string>

const int WINDOW_SIZE = 1000;
std::deque<double> r_values;
std::deque<double> s_values;

double rolling_entropy(std::deque<double> &values)
{
    // Placeholder: Hitung entropi Shannon sederhana
    double entropy = 0.0;
    return entropy;
}

void update_stats(const std::string &r, const std::string &s)
{
    try
    {
        double r_val = std::stod(r);
        double s_val = std::stod(s);

        r_values.push_back(r_val);
        s_values.push_back(s_val);

        if (r_values.size() > WINDOW_SIZE)
        {
            r_values.pop_front();
            s_values.pop_front();
        }
    }
    catch (...)
    {
    }
}

bool is_anomaly(const std::string &r, const std::string &s)
{
    try
    {
        double r_val = std::stod(r);
        double s_val = std::stod(s);

        update_stats(r, s);

        double r_entropy = rolling_entropy(r_values);
        double s_entropy = rolling_entropy(s_values);

        return (r_entropy < 0.94 || s_entropy < 0.94);
    }
    catch (...)
    {
        return false;
    }
}