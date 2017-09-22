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
import matplotlib
import seaborn
import csv
from sklearn.manifold import TSNE

#Read file and store into a 2d array
with open("pca_a.txt") as textFile_a:
    lines_a = [line.split() for line in textFile_a]
    
with open("pca_b.txt") as textFile_b:
    lines_b = [line.split() for line in textFile_b]
    
with open("pca_c.txt") as textFile_c:
    lines_c = [line.split('\t') for line in textFile_c]
    
    
#Convert 2d array into np array    
input_data_a = np.asarray(lines_a)
input_data_b = np.asarray(lines_b)
input_data_c = np.asarray(lines_c)

#Extract disease name (last column) from the variable input_data
disease_name_a = input_data_a[:,-1]
disease_name_b = input_data_b[:,-1]
disease_name_c = input_data_c[:,-1]
for i in range(0,len(disease_name_c)):
    disease_name_c[i] = disease_name_c[i].strip()

#Extract numeric data (all except last column) from the variable input_data
mat_a = input_data_a[:,:(input_data_a.shape[1]-1)]
mat_b = input_data_b[:,:(input_data_b.shape[1]-1)]
mat_c = input_data_c[:,:(input_data_c.shape[1]-1)]

#Convert the string type to float type
data_a = mat_a.astype(float)
data_b = mat_b.astype(float)
data_c = mat_c.astype(float)

#Calculate the mean of all rows for each column resulting in a shape: (1,4)
mean_a = np.mean(data_a,axis = 0)
mean_b = np.mean(data_b,axis = 0)
mean_c = np.mean(data_c,axis = 0)

#Calculate the centered data by subtracting the mean from all rows (X-X')
centered_data_a = np.subtract(data_a,mean_a)
centered_data_b = np.subtract(data_b,mean_b)
centered_data_c = np.subtract(data_c,mean_c)

#Calculate covariance matrix using the formula (X*X_Transpose)/N
cov_mat_a = np.cov(np.transpose(centered_data_a),bias=True)
cov_mat_b = np.cov(np.transpose(centered_data_b),bias=True)
cov_mat_c = np.cov(np.transpose(centered_data_c),bias=True)

#Calculate the eigen values and 
eigen_values_a,eigen_vectors_a = np.linalg.eig(cov_mat_a)
eigen_values_b,eigen_vectors_b = np.linalg.eig(cov_mat_b)
eigen_values_c,eigen_vectors_c = np.linalg.eig(cov_mat_c)

#Append the eigen values to the eigen vector matrix
temp_a = np.c_[eigen_vectors_a,eigen_values_a]
temp_b = np.c_[eigen_vectors_b,eigen_values_b]
temp_c = np.c_[eigen_vectors_c,eigen_values_c]

#Sort the above obtained matrix and sort according to the last column which is the eigen values.
#After sorting extract the top two vectors + eigen values
result_a = temp_a[temp_a[:,-1].argsort()[::-1][:2]]
result_b = temp_b[temp_b[:,-1].argsort()[::-1][:2]]
result_c = temp_c[temp_c[:,-1].argsort()[::-1][:2]]

#Remove the last column that we had appended earlier to obtain only the top two eigen vectors.
result_a = np.delete(result_a,-1,axis = 1)
result_b = np.delete(result_b,-1,axis = 1)
result_c = np.delete(result_c,-1,axis = 1)

new_data_points_a = np.dot(centered_data_a,np.transpose(result_a))
new_data_points_b = np.dot(centered_data_b,np.transpose(result_b))
new_data_points_c = np.dot(centered_data_c,np.transpose(result_c))

final_a = np.c_[new_data_points_a,disease_name_a]
final_b = np.c_[new_data_points_b,disease_name_b]
final_c = np.c_[new_data_points_c,disease_name_c]

#print(np.ravel(final[:,-1]).shape)
with open("a.csv", "w") as a:
    writer = csv.writer(a)
    writer.writerows(final_a)
    
with open("b.csv", "w") as b:
    writer = csv.writer(b)
    writer.writerows(final_b)
    
with open("c.csv", "w") as c:
    writer = csv.writer(c)
    writer.writerows(final_c)

