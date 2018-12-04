#!/bin/bash

cat input | awk 'BEGIN { x = 0 } { x += $1 } END { print x }'
