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
from sklearn.utils import shuffle
import sys
#
if(len(sys.argv) != 7):
    print("generate_filter.py [nr_features] [tissues] [percentage] [dest_dir] [relevant] [irrelevant]")
    exit(0)
#
nr_features = int(sys.argv[1])
tissues = sys.argv[2]
percentage = float(sys.argv[3])
random_state = 10
dest_dir = sys.argv[4]
#
str_relevant = sys.argv[5]
relevant = list()
for i in str_relevant.split(","):
    relevant.append(int(i))
str_irrelevant = sys.argv[6]
irrelevant = list()
for i in str_irrelevant.split(","):
    irrelevant.append(int(i))
print(relevant)
print(irrelevant)
#
#relevant = [1, 2, 3, 4]
#irrelevant = [5, 6, 7, 8]
#
files_ref_name = ""
for i in relevant:
    files_ref_name += str(i)
files_ref_name += "-"
for i in irrelevant:
    files_ref_name += str(i)
files_ref_name += "-{:.2f}-{}".format(percentage, random_state)
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
W = list()
#
#   Load CRC Dataset
#
f = open(tissues, "r")
nr_elem_classes = dict()
for i in f:
    line = i[:-1].split(";")
    label = int(line[0][0:2])
    x = np.array(line[2:-1])
    # discard bad images (with less attributes due to image format)
    if(len(x) == nr_features):
        if(nr_elem_classes.has_key(label)):
            nr_elem_classes[label] += 1
        else:
            nr_elem_classes[label] = 1
        # selection of relevant and irrelevant
        if(label in relevant):
            X.append(x.astype(np.float))
            Z.append(line[1])
            Y.append(0)
            W.append(label)
        if(label in irrelevant):
            X.append(x.astype(np.float))
            Z.append(line[1])
            Y.append(1)
            W.append(label)
    else:
	    print("{} {}".format(line[0],line[1]))
#
print(len(X), len(Y), len(Z))
# shuffle crc images to remove some images to keep the filter balanced
X_sh, Y_sh, Z_sh, W_sh = shuffle(X, Y, Z, W, random_state=10)
rel_num = 0
irrel_num = 0
for i in relevant:
    rel_num += nr_elem_classes[i]
for i in irrelevant:
    irrel_num += nr_elem_classes[i]
print(irrel_num, rel_num)
exit(0) 
#
for i in nr_elem_classes.keys():
    print(nr_elem_classes[i])
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
    joblib.dump(clf,dest_dir+'filter-'+files_ref_name+'.pkl')
    dump_image_names(Y_test, Z_test, dest_dir+'images_test-'+files_ref_name+'.txt')
    dump_image_names(Y_train, Z_train, dest_dir+'images_train-'+files_ref_name+'.txt')
#
#
#print(len(X_train), len(Y_train), len(Z_train))
#
