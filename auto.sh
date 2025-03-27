#!/bin/bash

for alpha in $(seq 0 0.2 1)
do
    for beta in $(seq 0 0.2 1)
    do
        python3 imfk_sifa.py $alpha $beta 0.05 0.06 inef > /dev/null &
    done
done