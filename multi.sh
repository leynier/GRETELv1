#!/bin/bash

search_dir=./config/steel/tc-500-28-7

for i in {1..10}
do
    for entry in "$search_dir"/*
    do
        qsub launch.sh main.py $entry $i
    done
done