#!/bin/bash

if [[ $1 = '--version' ]]; then
    echo "lrg_fake_maxquant.sh v0"
    exit 256
elif [[ $1 == *.xml ]]; then
    mkdir combined
    mkdir combined/txt
    touch combined/txt/proteinGroups.txt
    touch combined/txt/peptides.txt
fi
