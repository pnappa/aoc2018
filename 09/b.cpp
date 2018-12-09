#include <list>

#include <cstdlib>
#include <unordered_map>
#include <iostream>

std::list<ssize_t>::iterator two_forward(std::list<ssize_t>&  marb_ring, std::list<ssize_t>::iterator c_it) {
    size_t remaining = 2;
    ++c_it;
    --remaining;
    if (c_it == marb_ring.end()) c_it = marb_ring.begin();
    ++c_it;
    --remaining;
    return c_it;
}

std::list<ssize_t>::iterator seven_behind(std::list<ssize_t> & marb_ring, std::list<ssize_t>::iterator c_it) {
    ssize_t num_remaining = 7;
    while (num_remaining > 0) {
        if (c_it == marb_ring.begin()) {
            c_it = marb_ring.end();
        }

        --c_it;
        --num_remaining;
    }

    return c_it;
}

int main() {
    constexpr ssize_t num_players = 452;
    constexpr ssize_t max_marble  = 70784*100;

    // players are 0-indexed
    std::unordered_map<ssize_t, size_t> scores;
    std::list<ssize_t> marble_ring{0,1};

    ssize_t c_player = 1;
    // iterator pointing to the current marble
    auto c_marble_it = marble_ring.begin();
    c_marble_it++;

    for (ssize_t marble_num = 2; marble_num <= max_marble; ++marble_num) {
        if (marble_num % 23 == 0) {
            scores[c_player] += marble_num;

            // remove 7th marble behind c iterator
            auto pop_it = seven_behind(marble_ring, c_marble_it);
            auto index_val = *pop_it;

            c_marble_it = pop_it;
            c_marble_it++;
            if (c_marble_it == marble_ring.end()) c_marble_it = marble_ring.begin();

            marble_ring.erase(pop_it);

            scores[c_player] += index_val;
        } else {
            auto insert_index = two_forward(marble_ring, c_marble_it);
            c_marble_it = marble_ring.insert(insert_index, marble_num);
        }

        c_player += 1;
        c_player %= num_players;
    }

    
    ssize_t max = 0;
    for (auto& k : scores) {
        if (k.second > max) max = k.second;
    }

    std::cout << max << std::endl;
}
