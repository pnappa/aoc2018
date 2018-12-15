#!/bin/bash

set -e

for i in {10..16};
do
    python3 b.py $i || echo "fuck";
done
