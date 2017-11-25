#!/bin/bash
#
textures=("decaf" "tensorflow" "pftas")
#
for i in ${textures[*]};
do
    for j in "40" "100" "200" "400";
    do
        for k in $(find "filters/"$i"/" -iname *.pkl);
        do
            #wc -l "data/breakhis_"$i"/"$j".txt"
            #file $k
            a=$(head -n 1 "data/breakhis_"$i"/"$j".txt" | grep -o ";" | wc -l)
            let b=$a-2
            t=$(basename  $k .pkl)
            #echo 1 > "data_filtered/"$i"/"$j"-"$t".txt"
            ./filter_images.py "data/breakhis_"$i"/"$j".txt" $k $b > "data_filtered/"$i"/"$j"-"$t".txt"
        done
    done
done
