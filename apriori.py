#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 19:01:24 2017

@author: harilsatra
"""
# Import statements
from collections import Counter
from itertools import combinations


# Read the file as a 2d list
with open("associationruletestdata.txt") as textFile:
    input_data = [line.split('\t') for line in textFile]
    
# Function to generate the frequent itemsets and prune them using apriori principle as well as support count.
def generateFreqItemsets(candidate_list,candidate_dict,num_comb,support):
    #candidate_list = list(combinations(individual_set,num_comb))
    
    new_candidate_list = []
    if num_comb-2 == 0:
        new_candidate_list = list(combinations(sorted(candidate_list),num_comb))

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
            candidate_dict[tuple(candidate)] = candidate_count
              
    return len(freqset), freqset, candidate_dict

# Function for answering template1 queries
def template1(part,occurrence,item,rule_left,rule_right,rule_list):
    count = 0
    result_set = set()
    if part == 'RULE':
        if occurrence == 'ANY':
            for i in range(0,len(rule_left)):
                for element in item:
                    if element in rule_left[i] or element in rule_right[i]:
                        count += 1
                        result_set.add(rule_list[i])
                        break
        if occurrence == 'NONE':
            for i in range(0,len(rule_left)):
                for element in item:
                    if element not in rule_left[i] and element not in rule_right[i]:
                        count += 1
                        result_set.add(rule_list[i])
                        break
        if occurrence == 1:
            for i in range(0,len(rule_left)):
                flag = 0
                for element in item:
                    if element in rule_left[i] or element in rule_right[i]:
                        flag += 1
                if flag == 1:
                    result_set.add(rule_list[i])
                    count += 1
    else:
        if part == "HEAD":
             temp_list = rule_right
        else:
            temp_list = rule_left
        
        if occurrence == 'ANY':
            for i in range(0,len(temp_list)):
                for element in item:
                    if element in temp_list[i]:
                        result_set.add(rule_list[i])
                        count += 1
                        break
        if occurrence == 'NONE':
            for i in range(0,len(temp_list)):
                for element in item:
                    if element not in temp_list[i]:
                        result_set.add(rule_list[i])
                        count += 1
                        break
        if occurrence == 1:
            for i in range(0,len(temp_list)):
                flag = 0
                for element in item:
                    if element in temp_list[i]:
                        flag += 1
                if flag == 1:
                    result_set.add(rule_list[i])
                    count += 1   
    return count,result_set

# Function for answering template2 queries
def template2(part,mincount,rule_left,rule_right,rule_list):
    count = 0
    result_set = set()
    if part == 'RULE':
        for i in range(0,len(rule_left)):
            if len(rule_left[i])+len(rule_right[i]) >= mincount:
                result_set.add(rule_list[i])
                count += 1
    elif part == 'HEAD':
        for i in range(0,len(rule_right)):
            if len(rule_right[i]) >= mincount:
                result_set.add(rule_list[i])
                count += 1
    elif part == 'BODY':
        for i in range(0,len(rule_left)):
            if len(rule_left[i]) >= mincount:
                result_set.add(rule_list[i])
                count += 1
    return count,result_set

# Function for answering template3 queries
def template3(comb,rule_left,rule_right,rule_list, *args):
    if comb == '1or1':
        temp1_count,temp1_result = template1(args[0],args[1],args[2],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template1(args[3],args[4],args[5],rule_left,rule_right,rule_list)
        return len(temp1_result.union(temp2_result)),temp1_result.union(temp2_result)
    
    if comb == '1or2':
        temp1_count,temp1_result = template1(args[0],args[1],args[2],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template2(args[3],args[4],rule_left,rule_right,rule_list)
        return len(temp1_result.union(temp2_result)),temp1_result.union(temp2_result)
        
    if comb == '2or2':
        temp1_count,temp1_result = template2(args[0],args[1],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template2(args[2],args[3],rule_left,rule_right,rule_list)
        return len(temp1_result.union(temp2_result)),temp1_result.union(temp2_result)
    
    if comb == '1and1':
        temp1_count,temp1_result = template1(args[0],args[1],args[2],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template1(args[3],args[4],args[5],rule_left,rule_right,rule_list)
        return len(temp1_result.intersection(temp2_result)),temp1_result.intersection(temp2_result)
    
    if comb == '1and2':
        temp1_count,temp1_result = template1(args[0],args[1],args[2],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template2(args[3],args[4],rule_left,rule_right,rule_list)
        return len(temp1_result.intersection(temp2_result)),temp1_result.intersection(temp2_result)
    
    if comb == '2and2':
        temp1_count,temp1_result = template2(args[0],args[1],rule_left,rule_right,rule_list)
        temp2_count,temp2_result = template2(args[2],args[3],rule_left,rule_right,rule_list)
        return len(temp1_result.intersection(temp2_result)),temp1_result.intersection(temp2_result)


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


for z in range(50,60,10):
    
    #Calculate support
    support = z * len(input_data)//100
    print("\nSUPPORT: "+str(support)+"%\n")  

    #Set min confidence value
    minconf =  0.7   
               
    # Initialize a set to store the frequent itemsets of length 1
    freqset_1 = set()
    freqdict = {}
    freqset_list = []
    total = 0
    
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
            freqdict['G' + str(j+1) + '_' + 'Up'] = temp_up
        if temp_down >= support:
            freqset_1.add('G' + str(j+1) + '_' + 'Down')
            freqdict['G' + str(j+1) + '_' + 'Down'] = temp_down
    
    # Also add the disease names which have occured more than the support count to the frequent itemset.
    disease_count = Counter([row[-1] for row in input_data])
    for d in Counter([row[-1] for row in input_data]).keys():
        if disease_count[d]>=support:
            freqset_1.add(d)
            freqdict[d] = support
    
    freqset_list.append(freqset_1)
    
    # Print the number of lenght-1 frequent itemsets 
    print("Number of length 1 frequent itemsets: "+str(len(freqset_1)))
    total = total + len(freqset_1)
    
    # Calling the function to generate frequent itemsets of increasing length.
    length = 2
    while True:
        lenfreqset_2, freqset_2,freqdict = generateFreqItemsets(list(freqset_1),freqdict,length,support)
        freqset_1=freqset_2
        freqset_list.append(freqset_1)
        print("Number of length " +str(length)+" frequent itemsets: "+str(lenfreqset_2))
        total += lenfreqset_2
        length += 1
        if lenfreqset_2 == 0:
            break
    
    #Print total number of all length frequent itemsets
    print("Number of all lengths frequent itemsets:" + str(total))
    print()
    
    # Generating the Association Rules
    rule_list = []
    rule_left = []
    rule_right = []
    count = 0
    for i in range(1,len(freqset_list)):
        for candidate in freqset_list[i]:
            subsets = []
            #print("Candiate: "+str(candidate))
            for j in range(1,len(candidate)):
                subsets = subsets + list(combinations(candidate,j))
            for subset in subsets:
                #print("Subset: "+str(subset))
                if(len(subset)==1):
                    if subset[0] in freqdict:
                        confidence = freqdict[tuple(candidate)]/freqdict[subset[0]]
                        if confidence >= minconf:
                            count += 1
                            rule_left.append([subset[0]])
                            rule_right.append(set(candidate).difference(subset))
                            rule_string = str(subset[0])+" -> "+str(set(candidate).difference(subset))
                            rule_list.append(rule_string)

                else:
                    if subset in freqdict:
                        confidence = freqdict[tuple(candidate)]/freqdict[subset]
                        if confidence >= minconf:
                            count += 1
                            rule_left.append(subset)
                            rule_right.append(set(candidate).difference(subset))
                            rule_string = str(subset)+" -> "+str(set(candidate).difference(subset))
                            rule_list.append(rule_string)


    # --------------------- Print results of Template 1 queries ---------------------------------
    cnt11,result11 = template1("RULE","ANY",['G59_Up'],rule_left,rule_right,rule_list)
    #print('(result11, cnt) = asso_rule.template1("RULE", "ANY", ["G59_Up"]) '+str(cnt11))
    #print(result11)
    #print()
    
    cnt12,result12 = template1("RULE","NONE",['G59_Up'],rule_left,rule_right,rule_list)
    #print('(result11, cnt) = asso_rule.template1("RULE", "NONE", ["G59_Up"]) '+str(cnt12))
    #print(result12)
    #print()
    
    cnt13,result13 = template1("RULE",1,['G59_Up','G10_Down'],rule_left,rule_right,rule_list)
    #print('(result13, cnt) = asso_rule.template1("RULE", 1, ["G59_Up","G10_Down"]) '+str(cnt13))
    #print(result13)
    #print()
    
    cnt14,result14 = template1("BODY","ANY",['G51_Up'],rule_left,rule_right,rule_list)
    print('(result14, cnt) = asso_rule.template1("BODY", "ANY", ["G51_Up"]) '+str(cnt14))
    #print(result14)
    #print()
    
    cnt15,result15 = template1("BODY","NONE",['G1_Up'],rule_left,rule_right,rule_list)
    print('(result15, cnt) = asso_rule.template1("BODY", "NONE", ["G1_Up"]) '+str(cnt15))
    #print(result15)
    #print()
    
    cnt16,result16 = template1("BODY",1,['G59_Up','G10_Down'],rule_left,rule_right,rule_list)
    #print('(result16, cnt) = asso_rule.template1("BODY", 1, ["G59_Up","G10_Down"]) '+str(cnt16))
    #print(result16)
    #print()
    
    cnt17,result17 = template1("HEAD","ANY",['G59_Up'],rule_left,rule_right,rule_list)
    #print('(result17, cnt) = asso_rule.template1("HEAD", "ANY", ["G59_Up"]) '+str(cnt17))
    #print(result17)
    #print()
    
    cnt18,result18 = template1("HEAD","NONE",['G59_Up'],rule_left,rule_right,rule_list)
    #print('(result18, cnt) = asso_rule.template1("HEAD", "NONE", ["G59_Up"]) '+str(cnt18))
    #print(result18)
    #print()
    
    cnt19,result19 = template1("HEAD",1,['G59_Up','G10_Down'],rule_left,rule_right,rule_list)
    #print('(result19, cnt) = asso_rule.template1("HEAD", 1, ["G59_Up","G10_Down"]) '+str(cnt19))
    #print(result19)
    #print()
    
    print()
    
    # --------------------- Print results of Template 2 queries ---------------------------------
    cnt21,result21 = template2("RULE",3,rule_left,rule_right,rule_list)
    #print('(result21, cnt) = asso_rule.template2("RULE", 3) ' +str(cnt21))
    #print(result21)
    #print()
    
    cnt22,result22 = template2("BODY",2,rule_left,rule_right,rule_list)
    print('(result22, cnt) = asso_rule.template2("BODY", 2) '+ str(cnt22))
    #print(result22)
    #print()
    
    cnt23,result23 = template2("HEAD",1,rule_left,rule_right,rule_list)
    #print('(result23, cnt) = asso_rule.template2("HEAD", 1) '+str(cnt23))
    #print(result23)
    #print()
    
    print()
    
    # --------------------- Print results of Template 3 queries ---------------------------------
    cnt31,result31 = template3("1or1", rule_left,rule_right,rule_list, "BODY", "ANY", ['G10_Down'],"HEAD", 1, ['G59_Up'])
    #print('(result31, cnt) = asso_rule.template3("1or1", "BODY", "ANY", ["G10_Down"],"HEAD", 1, ["G59_Up"]) ' + str(cnt31))
    #print(result31)
    #print()
    
    cnt32,result32 = template3("1and1", rule_left,rule_right,rule_list, "BODY", "ANY", ['G1_Up'],"HEAD", 2, ['G59_Up'])
    #print('(result32, cnt) = asso_rule.template3("1and1", "BODY", "ANY", ["G10_Down"],"HEAD", 1, ["G59_Up"]) ' + str(cnt32))
    #print(result32)
    #print()
    
    cnt33,result33 = template3("1or2", rule_left,rule_right,rule_list, "BODY", "ANY", ['G1_Up'],"HEAD", 2)
    print('(result33, cnt) = asso_rule.template3("1or2", "BODY", "ANY", ["G1_Up"],"HEAD", 2) ' + str(cnt33))
    #print(result33)
    #print()
    
    cnt34,result34 = template3("1and2", rule_left,rule_right,rule_list, "BODY", "ANY", ['G1_Up'],"HEAD", 2)
    print('(result34, cnt) = asso_rule.template3("1and2", "BODY", "ANY", ["G1_Up"],"HEAD", 2) ' + str(cnt34))
    #print(result34)
    #print()
    
    cnt35,result35 = template3("2or2",rule_left,rule_right,rule_list, "BODY", 1,"HEAD", 2)
    #print('(result35, cnt) = asso_rule.template3("2or2", "BODY", 1, "HEAD", 2) '+str(cnt35))
    #print(result35)
    #print()
    
    cnt36,result36 = template3("2and2",rule_left,rule_right,rule_list, "BODY", 1,"HEAD", 2)
    #print('(result35, cnt) = asso_rule.template3("2and2", "BODY", 1, "HEAD", 2) '+str(cnt36))
    #print(result36)
    #print()
    
    print()