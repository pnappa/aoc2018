#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <tuple>

#include <unordered_map>

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

    // we know by looking at the file, the range is between [0,0]->[400,400]
    // as there are ~50 points, consider the x pos:
    //  worst case leftmost pos is if all coords are on x = 0
    //  thus, a point @ -200, will lead to a manhattan distance of 10k
    // so, we have to look at [-200, -200] -> [600, 600]
    
    std::vector<std::pair<int, int>> valid_points;
    constexpr int min_bound = -200;
    constexpr int max_bound = 600;
    constexpr int max_cum_dist = 10000;
    for (int y = min_bound; y < max_bound; ++y) {
        for (int x = min_bound; x < max_bound; ++x) {
            size_t cSum = 0;
            for (const auto& point : coords) {
                size_t manhatdist = abs(point.first - x) + abs(point.second-y);
                cSum += manhatdist;
            } 
            if (cSum < max_cum_dist) {
                valid_points.push_back(std::make_pair(x,y));
            }
        }
    }

    std::cout << "answer: " << valid_points.size() << std::endl;
    



}
