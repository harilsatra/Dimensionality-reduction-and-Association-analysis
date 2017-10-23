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
# Module imports
import numpy as np
import csv
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD

i = 1
while True:
    #filename = 'pca_'+chr(97+i)+'.txt'
    #filename = 'pca_demo.txt'
    filename = input("Enter file name with extension or write exit to stop: ")
    
    if filename.upper() == 'EXIT':
        break
                    
    #Read file and store into a 2d array
    with open(filename) as textFile:
        lines = [line.split('\t') for line in textFile]
        
    #Convert 2d array into np array    
    input_data = np.asarray(lines)
    
    #Extract disease name (last column) from the variable input_data
    disease_name = input_data[:,-1]
    for j in range(0,len(disease_name)):
        disease_name[j] = disease_name[j].strip()
        
    #Extract numeric data (all except last column) from the variable input_data    
    mat = input_data[:,:(input_data.shape[1]-1)]
    
    #Convert the string type to float type
    data = np.mat(mat.astype(float))
    #print(data)
    
    #Calculate the mean of all rows for each column resulting in a shape: (1,4)
    mean = np.mean(data,axis = 0)
    
    #Calculate the centered data by subtracting the mean from all rows (X-X')
    centered_data = np.subtract(data,mean)
    
    #Calculate covariance matrix using the formula (X*X_Transpose)/N
    cov_mat = np.cov(np.transpose(centered_data))
    
    #Calculate the eigen values and eigen vectors
    eigen_values,eigen_vectors = np.linalg.eig(cov_mat)
    
    #Append the eigen values to the eigen vector matrix
    eigen_values = np.reshape(eigen_values,(1,data.shape[1]))
    
    #Sort the above obtained matrix and sort according to the last column which is the eigen values.
    #After sorting extract the top two vectors + eigen values[::-1][:2]
    sort_indices = eigen_values.argsort()
    result = np.append(eigen_vectors[:,sort_indices[0][-1]],eigen_vectors[:,sort_indices[0][-2]])
    result = np.reshape(result,(data.shape[1],2),order='F')
    
    #Dot product of the original data and the eigen vectors to obtain the new data points
    new_data_points = centered_data * result
    new_data_points = new_data_points.tolist()
    
    #Append the disease corresponding to the new data points
    for j in range(0,len(new_data_points)):
        new_data_points[j].append(disease_name[j])
    
    output_file = 'pca_'+str(i)+'.csv'
    #output_file = 'demo.csv'
    
    #Write the new data points along with the disease name to a csv file
    with open(output_file, "w") as a:
        writer = csv.writer(a)
        writer.writerows(new_data_points)
        
    # TSNE   
    data_tsne = TSNE(n_components=2).fit_transform(data)
    
    #Append the disease corresponding to the new data points obtained from TSNE
    tsne = np.c_[data_tsne,disease_name]
    
    tsne_output = 'tsne_'+str(i)+'.csv'
    #tsne_output = 'tsne_demo.csv'
    
    #Write TSNE output to a csv file
    with open(tsne_output, "w") as x:
        writer = csv.writer(x)
        writer.writerows(tsne)
        
    # SVD
    svd = TruncatedSVD(n_components=2)
    data_svd = svd.fit_transform(centered_data)
    
    #Append the disease corresponding to the new data points obtained from TSNE
    data_svd = np.c_[data_svd,disease_name]
    
    svd_output = 'svd_'+str(i)+'.csv'
    #svd_output = 'svd_demo.csv'
    
    #Write SVD output to a csv file
    with open(svd_output, "w") as x:
        writer = csv.writer(x)
        writer.writerows(data_svd)
    
    i += 1