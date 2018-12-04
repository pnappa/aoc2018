#!/usr/bin/python3

ordering = []
with open('input', 'r') as ifile:
    ordering = [int(x.strip()) for x in ifile.readlines()]

print(len(ordering))


cfreq = 0
reached_frequencies = set([0])
cIndex = 0
while True:
    cfreq += ordering[cIndex]
    if cfreq in reached_frequencies:
        break;
    reached_frequencies.add(cfreq)
    cIndex = (cIndex + 1) % len(ordering)
    

print(cfreq)
