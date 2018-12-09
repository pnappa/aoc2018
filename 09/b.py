import string

# XXX: ignore this one, takes yonks to complete, refer to b.cpp for the real solution

num_players = 452
max_marble = 70784*100

scores = dict.fromkeys(range(num_players), 0)


marble_ring = [0,1]
c_player = 1
c_marble_index = 1

# ignore the first move, because we put 0 in anyway
for marble_num in range(2, max_marble+1):
    if marble_num % 70784 == 0:
        print("percent done")
    # SPECIAL CASE!!!
    if marble_num % 23 == 0:
        scores[c_player] += marble_num
        # then pop off the 7th marble anti-clockwise
        pop_index = (c_marble_index - 7)
        if pop_index < 0:
            pop_index += 1
        index_val = marble_ring[pop_index]
        scores[c_player] += index_val
        del marble_ring[pop_index]
        c_marble_index = (pop_index)%len(marble_ring)
    else:
        insert_index = c_marble_index + 2
        if insert_index == len(marble_ring):
            marble_ring.append(marble_num)
            c_marble_index = len(marble_ring)-1
        else:
            insert_index %= len(marble_ring)
            marble_ring.insert(insert_index, marble_num)
            c_marble_index = insert_index


    c_player += 1
    c_player %= num_players


print(scores)

print(max(scores.items(), key=lambda x: x[1]))
