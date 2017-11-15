#!/usr/bin/python
#
from __future__ import print_function
#
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.externals import joblib
#
nr_features = 162
tissues = "data/crc_pftas/features.txt"
percentage = 0.15
random_state = 10
dest_dir = "filters/pftas/"
#
relevant = [1, 2, 3, 4]
irrelevant = [5, 6, 7, 8]
#
files_ref_name = ""
for i in relevant:
    files_ref_name += str(i)
files_ref_name += "-"
for i in irrelevant:
    files_ref_name += str(i)
files_ref_name += "{:.2f}-{}".format(percentage, random_state)
#
#
#
def grid_report(clf, X_test, Y_test):
    print("Melhores paametros:")
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
#
#
#
def dump_image_names(Y, Z, filename):
    f = open(filename, "w")
    for i in range(len(Z)):
        f.write("{}-{}\n".format(Y[i],Z[i]))
    f.close()
#
#
#
def load_data(X, Y, Z, filename):
    f = open(filename, "r")
    for i in f:
        Z_file = i[:-1]
    f.close()
    X_tmp = list()
    Y_tmp = list()
    Z_tmp = list()
    for i in range(len(Z)):
        if(Z[i] in Z_file):
            X_tmp.append(X[i])
            Y_tmp.append(Y[i])
            Z_tmp.append(Z[i])
    return X_tmp, Y_tmp, Z_tmp
#
#
#
X = list()
Y = list()
Z = list()
#
f = open(tissues, "r")
for i in f:
    line = i[:-1].split(";")
    label = int(line[0][0:2])
    x = np.array(line[2:-1])
    #
    #print(len(x))
    if(len(x) == nr_features):
        X.append(x.astype(np.float))
        if(label in relevant):
            Y.append(0)
        else:
            Y.append(1)
        Z.append(line[1])
    else:
	    print("{} {}".format(line[0],line[1]))
#
print(len(X), len(Y), len(Z))     
#
X_train, X_test, Y_train, Y_test, Z_train, Z_test = train_test_split(X, Y, Z, test_size=percentage, random_state=10)
#
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-1, 1e-2, 1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
#
#scores = ['precision_macro', 'recall_macro', 'accuracy']
scores = ['accuracy']
#
for i in scores:
    clf = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring=i, n_jobs=4)
    clf.fit(X_train, Y_train)
    grid_report(clf, X_test, Y_test)
    joblib.dump(clf,'filter-'dest_dir+files_ref_name+'.pkl')
    dump_image_names(Y_test, Z_test, 'images_test-'+dest_dir+files_ref_name+'.txt')
    dump_image_names(Y_train, Z_train, 'images_train-'+dest_dir+files_ref_name+'.txt')
#

#
#print(len(X_train), len(Y_train), len(Z_train))
#
