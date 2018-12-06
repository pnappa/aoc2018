#include <iostream>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <cassert>
#include <vector>
#include <tuple>
#include <thread>

#include <unordered_map>

/**
 * c++17 solution for week 6 part a.
 * this is multithreaded, and you'll need to run twice, modifying min_bound & max_bound to be larger
 * You then should compare the output to see which area *didn't* change.
 * Yes, this could be solved easily using continuous voronoi, then aliasing bounded blocks to discrete chunks
 * ... but i'm lazy
 *
 * This solution isn't necessarily correct either, it *is* possible to break it, but it's incredibly unlikely,
 * especially given the fixed input.
 */

// Only for pairs of std::hash-able types for simplicity.
// You can of course template this struct to allow other hash functions
struct pair_hash {
    template <class T1, class T2>
    std::size_t operator () (const std::pair<T1,T2> &p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);

        // Mainly for demonstration purposes, i.e. works but is overly simple
        // In the real world, use sth. like boost.hash_combine
        return h1 ^ h2;  
    }
};


void get_counters(int begX, int endX, int begY, int endY, const std::vector<std::pair<int, int>>& coords, std::unordered_map<std::pair<int, int>, int, pair_hash>& counts) {
    for (int y = begY; y < endY; ++y) {
        for (int x = begX; x < endX; ++x) {
            int c_min_dist = 9999999;
            std::pair<int, int> closest = coords.front();
            bool doubled = false;
            for (const auto& point : coords) {
                int p_dist = abs(point.first - x) + abs(point.second - y);
                if (p_dist < c_min_dist) {
                    doubled = false;
                    c_min_dist = p_dist;
                    closest = point;
                } else if (p_dist == c_min_dist) {
                    doubled = true;
                }
            }
            if (!doubled) {
                counts[closest] += 1;
            }
        }
    }
}

int main() {
    std::ifstream ifile("input");
    if (ifile.is_open()) {
        std::cout << "file opened..." << std::endl;
    }
    std::vector<std::pair<int, int>> coords;
    std::string line = "";
    while (std::getline(ifile, line)) {
        int x = std::stoi(line.substr(0, line.find(',')));
        int y = std::stoi(line.substr(line.find(' ')+1));
        coords.push_back(std::make_pair(x,y));
    }

    // other attempts have failed... i tried using several solutions, but looks like the "guesstimation" way will suffice
    constexpr int num_threads = 4;
    
    // over this range fill our dict  [min_bound, max_bound]
    constexpr int min_bound = -4000;
    constexpr int max_bound = 4000;
    static_assert((max_bound - min_bound) % num_threads == 0, "area not evenly distributable");
    constexpr int vrange = (max_bound-min_bound)/num_threads;

    std::array<std::unordered_map<std::pair<int,int>, int, pair_hash>, num_threads> counters{};
    std::vector<std::thread> threads;
    for (int tnum = 0; tnum < num_threads; ++tnum) {
        threads.push_back(std::thread([&](int intranum) {
                    // split vertically
                    get_counters(min_bound, max_bound, min_bound + vrange*(intranum), min_bound + vrange*(intranum+1), coords, counters.at(intranum));
                    }, tnum));
    }

    for (auto& t : threads) t.join();

    std::unordered_map<std::string, int> totals;
    // merge the dictionaries together
    for (auto& map : counters) {
        for (auto& [coord, count] : map) {
            std::string vargo = std::to_string(coord.first) + ":" + std::to_string(coord.second);
            totals[vargo] += count;
        }         
    }
    
    std::vector<std::pair<int, std::string>> finals;
    for (auto& [coord, count] : totals) {
        finals.push_back(std::make_pair(count, coord));
    }

    std::sort(finals.begin(), finals.end());

    for (auto& [count, label] : finals) {
        std::cout << count << '\t' << label << std::endl;
    }

    return 0;
}
