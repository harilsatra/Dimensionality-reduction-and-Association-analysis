#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 19:01:24 2017

@author: harilsatra
"""

from collections import Counter
from itertools import combinations


# Read the file as a 2d list
with open("associationruletestdata.txt") as textFile:
    input_data = [line.split('\t') for line in textFile]
    
# Function to generate the frequent itemsets and prune them using apriori principle as well as support count.
def generateFreqItemsets(candidate_list,num_comb,support):
    #candidate_list = list(combinations(individual_set,num_comb))
    
    new_candidate_list = []
    if num_comb-2 == 0:
        new_candidate_list = list(combinations(candidate_list,num_comb))
    else:
        for i in range(len(candidate_list)):
            for j in range(i+1,len(candidate_list)):
                for k in range(num_comb-2):
                    if candidate_list[i][k] != candidate_list[j][k]:
                        #print(candidate_list[i],candidate_list[j])
                        break
                    else:
                        if k == num_comb-3:
                           new_candidate_list.append(sorted(set(candidate_list[i]).union(candidate_list[j])))               
                            
    freqset = set()
    
    for candidate in new_candidate_list:
        candidate_count = 0
        for transaction in transactions_list:
            if len(candidate) == len(transaction.intersection(candidate)):
                candidate_count += 1
            if candidate_count >= support:
                freqset.add(tuple(candidate))
                break
              
    return len(freqset), freqset

# Initialize a list for storing each transaction as a set.
transactions_list = []

# Separate the last column to handle the disease name separately
for i in range(0,len(input_data)):
    input_data[i][-1] = input_data[i][-1].strip()
    
# Process the data to change 'Up' and 'Down' to 'G{column_number}_Up' and 'G{column_number}_Down' respectively
for i in range(0,len(input_data)):
    temp_set = set()
    for j in range(0,len(input_data[0])):
        if j == len(input_data[0])-1:
            temp_set.add(input_data[i][j])
        else:
            input_data[i][j] = 'G' + str(j+1) + '_' + input_data[i][j]
            temp_set.add(input_data[i][j])
    # Also append each transaction as a set to the transaction_list        
    transactions_list.append(temp_set)

for z in range(30,80,10):
    
    #Calculate support
    support = z * len(input_data)//100
    print("\nSUPPORT: "+str(support)+"%\n")                 
    # Initialize a set to store the frequent itemsets of length 1
    freqset_1 = set()
    
    # Count the individual instances of items to generate for length 1
    for j in range(0,len(input_data[0])-1):
        temp_up = 0
        temp_down = 0
        for i in range(0,len(input_data)):
            if(input_data[i][j].split('_')[1] == 'Up'):
                temp_up = temp_up + 1
            else:
                temp_down += 1
        if temp_up >= support:
            freqset_1.add('G' + str(j+1) + '_' + 'Up')
        if temp_down >= support:
            freqset_1.add('G' + str(j+1) + '_' + 'Down')
        #freq_1.append([temp_up,temp_down])
    
    # Also add the disease names which have occured more than the support count to the frequent itemset.
    disease_count = Counter([row[-1] for row in input_data])
    for d in Counter([row[-1] for row in input_data]).keys():
        if disease_count[d]>=support:
            freqset_1.add(d)
    
    # Print the number of lenght-1 frequent itemsets 
    print("Number of length 1 frequent itemsets: "+str(len(freqset_1)))
    
    # Calling the function to generate frequent itemsets of increasing length.
    length = 2
    while True:
        lenfreqset_2, freqset_2 = generateFreqItemsets(list(freqset_1),length,support)
        freqset_1=freqset_2
        print("Number of length " +str(length)+" frequent itemsets: "+str(lenfreqset_2))
        length += 1
        if lenfreqset_2 == 0:
            break


