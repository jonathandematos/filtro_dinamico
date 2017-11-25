#!/usr/bin/python
#
import numpy as np
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint as sp_randint
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
#
if(len(sys.argv) != 6):
    print("classify.py [nr_features] [zoom] [features_file] [fold_file] [inductor]")
    exit(0)
#
nr_features = 162
zoom = 40
features = "data/breakhis_pftas/40.txt"
fold_file = "folds/dsfold1.txt"
inductor = "svm"
#
nr_features = int(sys.argv[1])
zoom = int(sys.argv[2])
features = sys.argv[3]
fold_file = sys.argv[4]
inductor = sys.argv[5]
#
#
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
        else:
            print("Erro: {} {}".format(line[1], len(x)))
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
                imgs_train.append(img)
            if(linha[3] == "test"):
                imgs_test.append(img)
    f.close()
    X_train = list()
    Y_train = list()
    Z_train = list()
    X_test = list()
    Y_test = list()
    Z_test = list()
    print(len(imgs_train), len(imgs_test))
    for i in range(len(X)):
        tmp_img = Z[i].split("-")
        main_img = tmp_img[0]+"-"+tmp_img[1]+"-"+tmp_img[2]+"-"+tmp_img[3]+"-"+tmp_img[4]
        if(main_img in imgs_train):
            X_train.append(X[i])
            Y_train.append(Y[i])
            Z_train.append(Z[i])
        if(main_img in imgs_test):
            X_test.append(X[i])
            Y_test.append(Y[i])
            Z_test.append(Z[i])
    return X_train, Y_train, Z_train, X_test, Y_test, Z_test
#
#
#
def grid_report(clf, X_test, Y_test):
    print("Melhores parametros:")
    print(clf.best_params_)
    #
    print("\nScores:")
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    #
    print("Relatorio do teste:")
    Y_pred = clf.predict(X_test)
    print(classification_report(Y_test, Y_pred))
    print(confusion_matrix(Y_test, Y_pred))
#
#
#
X, Y, Z = load_dataset(features)
X_train, Y_train, Z_train, X_test, Y_test, Z_test = generate_fold(X, Y, Z, fold_file, zoom)
#
print(len(X_train), len(X_test)) 
#
#
#param_dist = {"n_estimators": [200,400,600,800]}
#              "max_depth": [3, None],
#              "max_features": sp_randint(1, 11),
#              "max_features": [1, 11],
#              "min_samples_split": sp_randint(1, 11),
#              "min_samples_split": [2, 11],
#              "min_samples_leaf": sp_randint(1, 11),
#              "min_samples_leaf": [1, 11],
#              "bootstrap": [True, False],
#              "criterion": ["gini", "entropy"]}
#
#scores = ['precision_macro', 'recall_macro', 'accuracy']
scores = ['accuracy']
#
for i in scores:i
    #
    if(inductor == "svm"):
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-1, 1e-2, 1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
        clf = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring=i, n_jobs=16)
    #
    if(inductor == "rf"):
        param_dist = {"n_estimators": [200,400,600,800]}
        clf = GridSearchCV(RandomForestClassifier(), param_dist, cv=5, scoring=i, n_jobs=12)
    #
    clf.fit(X_train, Y_train)
    grid_report(clf, X_test, Y_test)
#
