#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 16:55:39 2017

@author: Haril Satra
"""

'''
SHAPES (pca_a):
    input_data : (150,5)
    disease_name: (150,1)
    data: (150,4)
    mean: (1,4)
    centered_data: (150,4)
'''

import numpy as np

#Read file and store into a 2d array
with open("pca_a.txt") as textFile:
    lines = [line.split() for line in textFile]
    
#Convert 2d array into np array    
input_data = np.asarray(lines)

#Extract disease name (last column) from the variable input_data
disease_name = input_data[:,-1]

#Extract numeric data (all except last column) from the variable input_data
mat = input_data[:,:(input_data.shape[1]-1)]

#Convert the string type to float type
data = mat.astype(float)

#Calculate the mean of all rows for each column resulting in a shape: (1,4)
mean = np.mean(data,axis = 0)

#Calculate the centered data by subtracting the mean from all rows (X-X')
centered_data = np.subtract(data,mean)

#Calculate covariance matrix using the formula (X*X_Transpose)/N
cov_mat = np.cov(np.transpose(centered_data),bias=True)

#Calculate the eigen values and 
eigen_values,eigen_vectors = np.linalg.eig(cov_mat)

#Append the eigen values to the eigen vector matrix
temp = np.c_[eigen_vectors,eigen_values]

#Sort the above obtained matrix and sort according to the last column which is the eigen values.
#After sorting extract the top two vectors + eigen values
result = temp[temp[:,-1].argsort()[::-1][:2]]

#Remove the last column that we had appended earlier to obtain only the top two eigen vectors.
result = np.delete(result,-1,axis = 1)
print(result)

new_data_points = np.dot(centered_data,np.transpose(result))

final = np.c_[new_data_points,disease_name]
#print(final[:2,:])
