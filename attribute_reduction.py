#!/usr/bin/python
#
from __future__ import print_function
import numpy as np
from sklearn.decomposition import PCA
import sys
#
X = list()
Y = list()
Z = list()
W = list()
#
tissues = sys.argv[1]
nr_features = int(sys.argv[2])
nr_final_features = int(sys.argv[3])
#
#
#
def load_crc(filename):
    X = list()
    Z = list()
    W = list()
    f = open(tissues, "r")
    for i in f:
        line = i[:-1].split(";")
        label = int(line[0][0:2])
        x = np.array(line[2:-1])
        # discard bad images (with less attributes due to image format)
        if(len(x) == nr_features):
            # selection of relevant and irrelevant
            X.append(x.astype(np.float))
            Z.append(line[1])
            W.append(label)
        else:
    	    print("{} {} {}".format(line[0], line[1], len(x)))
    f.close()
    return X, Z, W
#
#
#
def load_breakhis(filename):
    f = open(filename, "r")
    #
    X = list()
    Y = list()
    Z = list()
    W = list()
    for i in f:
        line = i[:-1].split(";")
        #
        x = np.array(line[2:-1])
        if(len(x) == nr_features):       
            X.append(x)
            Z.append(line[1])
            W.append(line[0])
            if(line[0] == 'adenosis'):
            #if(line[0] == 'A'):
            	Y.append(int(0))
            if(line[0] == 'ductal_carcinoma'):
            #if(line[0] == 'DC'):
            	Y.append(int(4))
            if(line[0] == 'fibroadenoma'):
            #if(line[0] == 'F'):
            	Y.append(int(1))
            if(line[0] == 'lobular_carcinoma'):
            #if(line[0] == 'LC'):
            	Y.append(int(5))
            if(line[0] == 'mucinous_carcinoma'):
            #if(line[0] == 'MC'):
               	Y.append(int(6))
            if(line[0] == 'papillary_carcinoma'):
            #if(line[0] == 'PC'):
            	Y.append(int(7))
            if(line[0] == 'phyllodes_tumor'):
            #if(line[0] == 'PT'):
            	Y.append(int(2))
            if(line[0] == 'tubular_adenoma'):
            #if(line[0] == 'TA'):
            	Y.append(int(3))
        else:
            print("Erro: {} {}".format(line[1], len(x)))
    #
    f.close()
    return X, Z, W
#
#
#
X, Z, W = load_breakhis(tissues)
#
#
#
pca = PCA(n_components=nr_final_features)
pca.fit(X)
#
#print(pca.transform([X[1]]))
#
for i in range(len(X)):
    x_tmp = np.squeeze(pca.transform([X[i]]))
    print("{:02d};{};".format(W[i], Z[i]), end="")
    for j in x_tmp:
        print("{:.6f};".format(j), end="")
    print()
