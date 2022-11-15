#!/bin/bash
sd=$(pwd)
for f in $(ls games)
do
    mkdir -p $sd/html/$f
    cd games/$f
    python -m pygbag --build --html main.py
    cp -r build/web/* $sd/html/$f/
    cd $sd
done