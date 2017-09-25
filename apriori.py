#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 19:01:24 2017

@author: harilsatra
"""
import numpy as np
from collections import Counter
from itertools import combinations
#from itertools import permutations

with open("associationruletestdata.txt") as textFile:
    input_data = [line.split('\t') for line in textFile]
    
transactions_set = []

for i in range(0,len(input_data)):
    input_data[i][-1] = input_data[i][-1].strip()
    
for i in range(0,len(input_data)):
    temp_set = set()
    for j in range(0,len(input_data[0])):
        if j == len(input_data[0])-1:
            temp_set.add(input_data[i][j])
        else:
            input_data[i][j] = 'G' + str(j+1) + '_' + input_data[i][j]
            temp_set.add(input_data[i][j])
    transactions_set.append(temp_set)
        
freq_1 = []
freqset_1 = set()

for j in range(0,len(input_data[0])-1):
    temp_up = 0
    temp_down = 0
    for i in range(0,len(input_data)):
        if(input_data[i][j].split('_')[1] == 'Up'):
            temp_up = temp_up + 1
        else:
            temp_down += 1
    if temp_up >= 40:
        freqset_1.add('G' + str(j+1) + '_' + 'Up')
    if temp_down >= 40:
        freqset_1.add('G' + str(j+1) + '_' + 'Down')
    freq_1.append([temp_up,temp_down])

disease_count = Counter([row[-1] for row in input_data])
for d in Counter([row[-1] for row in input_data]).keys():
    if disease_count[d]>=40:
        freqset_1.add(d)

print(len(freqset_1))

freqset_list = []



def generateFreqItemsets(individual_set,num_comb):
    candidate_list = list(combinations(individual_set,num_comb))
    freqset = set()
    individual_set = set()
    
    for candidate in candidate_list:
        candidate_count = 0
        for transaction in transactions_set:
            if len(candidate) == len(transaction.intersection(candidate)):
                candidate_count += 1
            if candidate_count >= 40:
                freqset.add(candidate)
                for element in candidate:
                    individual_set.add(element)
                break
              
    return len(freqset), freqset, individual_set


for i in range(2,9):
    lenfreqset_2, freqset_2, indset_2 = generateFreqItemsets(freqset_1,i)
    freqset_1=indset_2
    print(lenfreqset_2)


'''
candidate_list = list(combinations(individual_2_set,3))
freqset_2 = set()
individual_2_set = set()

for candidate in candidate_list:
    candidate_count = 0
    for transaction in transactions_set:
        if len(candidate) == len(transaction.intersection(candidate)):
            candidate_count += 1
        if candidate_count >= 30:
            freqset_2.add(candidate)
            for element in candidate:
                individual_2_set.add(element)
            break
                
print(len(freqset_2 ))
#print(len(list(combinations(freqset_1,2))))
#print(len(freqset_1))
#print(freq_1)
'''


