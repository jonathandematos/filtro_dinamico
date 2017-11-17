#!/usr/bin/python
#
import os
import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile
import numpy as np 


def create_graph (model_path):
#    "" "
#    create_graph loads the inception model to memory, should be called before
#    calling extract_features.
#                  
#    model_path: path to inception model in protobuf form.
#    " "" 
    with gfile.FastGFile (model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString (f.read ())
        tensor_loaded = tf.import_graph_def (graph_def, name = '') 
        return tensor_loaded
        
def extract_features (image_paths, verbose = False):
#    "" "
#    extract_features computed the inception bottleneck feature for a list of images
#                                                                         
#    image_paths: array of image path
#    return: 2-d array in the shape of (len(image_paths), 2048)
#    
#    " "" 
    feature_dimension = 2048
    features = np.empty ((len (image_paths), feature_dimension)) 

    f = open("features_crc.txt","w")

    with tf.Session ()as sess:
        flattened_tensor = sess.graph.get_tensor_by_name ('pool_3:0') 
        for i, image_path in enumerate (image_paths):
            if verbose:
                print ('Processing %s...' % (image_path)) 
            if not gfile.Exists (image_path):
                tf.logging.fatal ('File does not exist %s', image)
            else:
	        image_data = gfile.FastGFile (image_path, 'rb').read ()
                feature = sess.run (flattened_tensor,{'DecodeJpeg/contents:0':image_data})
                f.write("{}".format(image_path))
                for j in np.squeeze(feature):
                    f.write(";{:.8f}".format(float(j)))
                f.write("\n")
                features[i,:] = np.squeeze (feature)

    f.close()
    return features

directories = ('adenosis','ductal_carcinoma','fibroadenoma','lobular_carcinoma','mucinous_carcinoma','papillary_carcinoma','phyllodes_tumor','tubular_adenoma')

path_images = '/home/jonathan/bioinfo/tissues/Kather_texture_2016_image_tiles_5000_png/'

directories = ('01_TUMOR','02_STROMA','03_COMPLEX','04_LYMPHO','05_DEBRIS','06_MUCOSA','07_ADIPOSE','08_EMPTY')

#path_images = '/home/jonathan/Documents/uepg/pesquisa/alceu/tissues/Kather_texture_2016_image_tiles_5000/' 

images = list()
for i in directories:
    for x in os.listdir(path_images+i+"/"):
        if x.endswith(".png"):
            images.append(path_images+i+"/"+x)

#print(images)
#exit(0)

tensor_loaded = create_graph("tensorflow_inception_graph.pb")

feats = extract_features(images, True)
print(feats)
#print(feats)

