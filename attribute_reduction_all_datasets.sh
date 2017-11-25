#!/bin/bash
#
for i in "decaf" "tensorflow";
do
    for j in 40 100 200 400;
    do
        for k in 100 200 400 600;
        do
            if [ $i == "decaf" ];
            then
                l=4096
            else
                l=2048
            fi
            ./attribute_reduction.py "data/breakhis_"$i"/"$j".txt" $l $k > "data/breakhis_"$i"_"$k"/"$j".txt"
        done
    done
done
