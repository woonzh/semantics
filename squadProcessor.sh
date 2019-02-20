#!/bin/sh

for counter in 1 2 3 4 5 6 7 8 9 10
do
    echo "Starting no $counter script"
    python squadProcessor.py dev false
done