#!/usr/bin/python
#
from __future__ import print_function
import sys
import numpy as np
from sklearn.externals import joblib
#
if(len(sys.argv) != 4):
    print("filter_images.py [dataset] [filter] [nr_features]")
    exit(0)
#
breakhis = sys.argv[1]
filter_file = sys.argv[2]
nr_features = int(sys.argv[3])
print_stats = False
print_excluded = True
#
if( print_stats ):
    print(sys.argv)
#
def load_dataset(filename):
    f = open(filename, "r")
    #
    X = list()
    Y = list()
    Z = list()
    Y_ext = list()
    for i in f:
        line = i[:-1].split(";")
        #
        x = np.array(line[2:-1])
        if(len(x) == nr_features):       
            X.append(x.astype(np.float))
            Y_ext.append(line[0])
            Z.append(line[1])
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
            if( print_stats ):
                print("Erro: {} {}".format(line[1], len(x)))
    #
    f.close()
    return X, Y, Z, Y_ext
#
#
#
def generate_patient_image(X, Y, Z, Y_ext):
    patient = dict()
    images = dict()
    for i in range(len(X)):
        a = Z[i].split("-")
        # SOB_M_PC-14-19440-40-021-137-155.png
        if(not patient.has_key(a[0]+"-"+a[1]+"-"+a[2])):
            patient[a[0]+"-"+a[1]+"-"+a[2]] = 0
        if(not images.has_key(a[0]+"-"+a[1]+"-"+a[2]+"-"+a[3]+"-"+a[4])):
            images[a[0]+"-"+a[1]+"-"+a[2]+"-"+a[3]+"-"+a[4]] = 0
    return patient, images
#
#
#
def generate_patient_list(X, Y, Z, Y_ext):
    patient = list()
    images = list()
    for i in range(len(X)):
        a = Z[i].split("-")
        # SOB_M_PC-14-19440-40-021-137-155.png
        if(a[0]+"-"+a[1]+"-"+a[2] not in patient):
            patient.append(a[0]+"-"+a[1]+"-"+a[2])
        if(a[0]+"-"+a[1]+"-"+a[2]+"-"+a[3]+"-"+a[4] not in images):
            images.append(a[0]+"-"+a[1]+"-"+a[2]+"-"+a[3]+"-"+a[4])
    return patient, images
#
#
#
X, Y, Z, Y_ext = load_dataset(breakhis)
#
clf = joblib.load(filter_file)
#
total = 0
keep = 0
W_pred = list()
for i in range(len(X)):
    a = clf.predict([X[i]])
    W_pred.append(a)
    if(a == 0):
        keep += 1
    total += 1
#
#print("{} mantidas de {}".format(keep, total))
#
patients, images =  generate_patient_list(X, Y, Z, Y_ext)
#
if( print_stats ):
    print("Original: {} pacientes, {} imagens, {} patches".format(len(patients), len(images), len(X)))
#
X_filtered = list()
Y_filtered = list()
Z_filtered = list()
Y_ext_filtered = list()
for i in range(len(X)):
   if(W_pred[i] == 0):
         X_filtered.append(X[i])
         Y_filtered.append(Y[i])
         Z_filtered.append(Z[i])
         Y_ext_filtered.append(Y_ext[i])
#
patients_f, images_f =  generate_patient_list(X_filtered, Y_filtered, Z_filtered, Y_ext_filtered)
#
if( print_stats ):
    print("Filtrado: {} pacientes, {} imagens, {} patches".format(len(patients_f), len(images_f), len(X_filtered)))
#
#
for i in patients:
    if(i not in patients_f):
        if( print_excluded ):
            for j in range(len(Z)):
                a = Z[j].split("-")
                # SOB_M_PC-14-19440-40-021-137-155.png
                if(a[0]+"-"+a[1]+"-"+a[2] == i):
                    print("{};{};".format(Y_ext[j], Z[j]), end="")
                    for k in X[j]:
                        print("{:.6f};".format(k),end="")
                    print()
        if( print_stats ):
            print("Paciente excluido: {}".format(i))
#
for i in range(len(X_filtered)):
    print("{};{};".format(Y_ext_filtered[i], Z_filtered[i]), end="")
    for j in X_filtered[i]:
        print("{:.6f};".format(j),end="")
    print()
#for i in images:
#    if(i not in images_f):
#        print(i)
#
