#/bin/bash
#
rel=("1,2,3,4,5,6,7" "1,2,3,4,5,6" "1,2,3,4,5" "1,2,3,4" "1,2,3" "1,2" "1")
irrel=("8" "7,8" "6,7,8" "5,6,7,8" "4,5,6,7,8" "3,4,5,6,7,8" "2,3,4,5,6,7,8")
#
#features=("pftas" "tensorflow" "decaf")
#features=("pftas" "tensorflow" "decaf")
#features=("glcm")
features=("tensorflow_100" "decaf_100" "tensorflow_200" "decaf_200" "tensorflow_400" "decaf_400" "tensorflow_600" "decaf_600" )
#
j=0
#
for i in ${rel[*]};
do
    l=0
    for k in ${features[*]};
    do 
        echo $k
        echo ${irrel[$j]}
        #echo ${rel[$j]}
        a=$(head -n 1 "data/crc_"$k"/features.txt" | grep -o ";" | wc -l)
        let b=$a-2
        c=$(echo ${rel[$j]} | sed 's/\,//g')
        d=$(echo ${irrel[$j]} | sed 's/\,//g')
        ./generate_filter.py $b "data/crc_"$k"/features.txt" 0.15 "filters/"$k"/" ${rel[$j]} ${irrel[$j]} > "filters/"$k"/output-"$c"-"$d"-0.15-10.txt"
    done
    let j=$j+1
done
