#!/usr/bin/python
#
from __future__ import print_function
import caffe
import leveldb
import numpy as np
from caffe.proto import caffe_pb2
import sys, os

#labels = open("breakhis_images.txt","r")

nr_dbs = 8

#for i in range(1,nr_dbs+1):
for i in range(0,119):

    db_dir = "breakhis_features/features_{:05d}".format(i)

    labels = open("breakhis_features/features_{:05d}.txt".format(i), "r")

    outfile = open("breakhis_features/features_{:05d}_output.txt".format(i), "w")

    db = leveldb.LevelDB(db_dir)
    datum = caffe_pb2.Datum()

    for key, value in db.RangeIter():
        linha = labels.readline()

        datum.ParseFromString(value)
    
        label = datum.label
        data = caffe.io.datum_to_array(datum)
        outfile.write("{};".format(linha[:-1]))
        for j in data.squeeze():
            outfile.write("{:.5f};".format(j))
        outfile.write("\n")
    labels.close()

    outfile.close()
#
#labels.close()
