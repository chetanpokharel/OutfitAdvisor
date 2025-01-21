import pickle
import  tensorflow 
import numpy as np
from numpy.linalg import norm
from   keras.api._v2.keras.applications.resnet50 import ResNet50,preprocess_input
from sklearn.neighbors import NearestNeighbors
from keras.api._v2.keras.preprocessing import image
from keras.api._v2.keras import Sequential
from keras.api._v2.keras.layers import GlobalMaxPooling2D
import os
import cv2

feature_list = np.array(pickle.load(open('./shoppinglyx/embeddings.pkl','rb')))
filenames = pickle.load(open('./shoppinglyx/filenames.pkl','rb'))

model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
model.trainable = False

model = Sequential([
    model,
    GlobalMaxPooling2D()
])

img = image.load_img('./shoppinglyx/watch.jpg',target_size=(224,224))
img_array = image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocessed_img = preprocess_input(expanded_img_array)
result = model.predict(preprocessed_img).flatten()
normalized_result = result / norm(result)

neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
neighbors.fit(feature_list)

distances,indices = neighbors.kneighbors([normalized_result])

print(indices)
#from google.colab.patches import cv2_imshow

from matplotlib import pyplot as plt
# import cv2 
result_urls=[]
for file in indices[0][0:5]:
   image_name=filenames[file].split("/")[-1]
   #temp_img = plt.imread(filenames[file])
   img_url='../fashion-dataset/images'

   result_urls.append(img_url)
  

print(result_urls)
#   # plt.imshow('output',plt.resize(temp_img,(512,512)))
#   plt.figure(figsize=(2,2))
#   plt.axis('off')

#   # cv2.waitkey(0)

#   plt.imshow(temp_img)
#   plt.show()

