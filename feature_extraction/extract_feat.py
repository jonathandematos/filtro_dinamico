#!/usr/bin/python
#
from __future__ import print_function
import os
import sys
import stat
import mahotas
import numpy as np
#import opencv
#
if( len(sys.argv) < 1):
	print("Diretorio nao informado")
	exit(0)

files = sys.argv[len(sys.argv)-1].split("/")[-1]
if(files == ''):
    print("Sem arquivos")
    exit(0)

p_file = open("pftas_file_"+files+".txt","w")
h_file = open("haralick_file_"+files+".txt","w")

mode = os.stat(sys.argv[1]).st_mode
if( stat.S_ISDIR(mode) ):
	total = os.listdir(sys.argv[1])
	cont = 0
	for img_files in total:
		print("{} de {}\r".format(cont, len(total)), end="")
		cont += 1
		files = sys.argv[len(sys.argv)-1].split("/")[-1]
		if(files == ''):
			exit(0)
		img_array = mahotas.imread(sys.argv[1]+"/"+img_files).astype(np.int32)
		img_array_colour = mahotas.imread(sys.argv[1]+"/"+img_files)
		h_feat = mahotas.features.haralick(img_array)
		h_feat_reshape = np.reshape(h_feat,(1,-1))
		p_feat = mahotas.features.pftas(img_array_colour)
		h_file.write("{};{};".format(files,img_files))
		for val in h_feat_reshape[0]:
			h_file.write("{:5.5f};".format(val))
		h_file.write("\n")
		p_file.write("{};{};".format(files,img_files))
		for val in p_feat:
			p_file.write("{:5.5f};".format(val))
		p_file.write("\n")
		#print(np.shape(h_feat_reshape))
		#print(h_feat_reshape)
		#exit(0)
h_file.close()
p_file.close()
					
