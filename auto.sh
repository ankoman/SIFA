#!/bin/bash

for alpha in $(seq 0 0.2 1)
do
    for beta in $(seq 0 0.2 1)
    do
        python3 imfk_sifa.py $alpha $beta 1 0.5 inef_all_x > /dev/null &
    done
done