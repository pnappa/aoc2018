
from collections import Counter
from time import time

# fill county words with (word, sumchars)
county_words = []
offset = ord('a')
with open('input', 'r') as ifile:
    for line in ifile:
        line = line.strip()
        county_words.append((line, sum(map(lambda x: ord(x) - offset, line))))

county_words.sort(key=lambda x: x[1])
print(county_words)


def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))

start = time()

# partition to separate impossible differences (i.e. > 52)
for word, count in county_words:
    for word2, count2 in county_words:
        if hamming_distance(word, word2) == 1:
            print("found")
            print(word, word2)
            
end = time()
print(end-start)
