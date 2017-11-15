#!/usr/bin/python
#
nr_features = 162
zoom = 40
#
def load_dataset(filename):
    f = open(filename, "r")
    #
    X = list()
    Y = list()
    Z = list()
    for i in f:
        line = i[:-1].split(";")
        #
        label = int(line[0][0:2])
        x = np.array(line[2:-1])
        if(len(x) == nr_features):       
            X.append(x)
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
    #
    f.close()
    return X, Y, Z
#
#
#
def generate_fold(X, Y, Z, fold_file, zoom):
    imgs_train = list()
    imgs_test = list()
    f = open(fold_file, "r")
    for i in f:
        linha = i[:-1].split("|")
        if(int(linha[1]) == zoom):
            img = linha[0].split(".")[0]
            if(linha[3] == "train"):
                F_train.append(img)
            else:
                F_test.append(img)
       
    f.close()
