#!/bin/bash
#
diretorio="breakhis_features"
total=$(wc -l breakhis_images.txt | cut -f 1 -d " ")
passo=1000
inicio=1
let fim=$inicio+$passo-1
t=0
while [ $fim -lt $total ];
do
    iter=$(printf "%05d" $t)
    a=$inicio","$fim"p"
    sed -n $a breakhis_images.txt > tmp_breakhis.txt
    #echo $inicio" "$fim
    ../../build/tools/extract_features.bin ../../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel imagenet_val.prototxt fc7 "breakhis_features/features_"$iter 1 leveldb
    mv tmp_breakhis.txt "breakhis_features/features_"$iter".txt"
    let inicio=$inicio+$passo
    let fim=$fim+$passo
    let t=$t+1
done
#
fim=$total
iter=$(printf "%05d" $t)
a=$inicio","$fim"p"
sed -n $a breakhis_images.txt > tmp_breakhis.txt
#echo $inicio" "$fim
../../build/tools/extract_features.bin ../../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel imagenet_val.prototxt fc7 "breakhis_features/features_"$iter 1 leveldb
mv tmp_breakhis.txt "breakhis_features/features_"$iter".txt"
#
