import pandas as pd
import csv
from itertools import chain, combinations

def read_data(file_loc):
    trans = dict()
    with open(file_loc) as f:
        filedata =csv.reader(f)

        count=0
        for line in filedata:
            count+=1
            lst=[]
            for i in line:
                lst.append(i)
            trans[count]=lst
    return trans

def increment(x, support_matrix):
    if x in support_matrix.keys():
        return support_matrix[x]+1
    return 1

def item_counter(trans, min_sup):
    support_matrix=dict()
    for i in trans.values():
        for x in i:
            support_matrix[x]=increment(x,support_matrix)
    print("C: ",support_matrix)
    return large_support(support_matrix, min_sup)

def pattern_generator(n , x, patterns, l):
    temp=x.copy()
    if(n==0):
        patterns.append(tuple(l))
    elif (len(x)==0):
        return
    else:
        ele=temp.pop()
        pattern_generator(n,temp,patterns,l)
        lt=l.copy()
        lt.append(ele)
        pattern_generator(n-1,temp,patterns,lt)

def calculate_support(n, prev_support_matrix, trans, items, min_sup):
    if n>1:
        patterns = []
        x = set()

        if n==2:
            for i in prev_support_matrix:
                    x.add(i)
        else:
            for i in prev_support_matrix:
                for j in i:
                    x.add(j)

        pattern_generator(n, x, patterns, [])

        support_matrix=dict()
        for i in patterns:
            for line in trans.values():
                if set(i).issubset(line):
                    support_matrix[i] = increment(i, support_matrix)

        print("C: ",support_matrix)
        return large_support(support_matrix,min_sup)

    return item_counter(trans, min_sup)


def large_support(support_matrix, min_sup):
    for i in list(support_matrix):
        if(support_matrix[i]<min_sup):
            support_matrix.pop(i)
    print("L: ",support_matrix, '\n')
    return support_matrix

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))

def association(trans,final_support_matrix,min_conf):
    for key in final_support_matrix:
        power_set=list(powerset(key))
        count=dict()


        for i in power_set:
            for j in trans.values():
                if set(i).issubset(j):
                    count[i]=increment(i,count)

        d=dict()
        for i in count.keys():
            if i!=key and count[key]/count[i]>=min_conf:
                temp = list(key)
                for x in i:
                    temp.remove(x)
                print(i,"->",temp)

def main(file):
    trans=read_data(file)
    print("data: ",trans,"\n")

    """
    min_sup_perct = float(input("Enter minimum support : "))
    min_sup=min_sup_perct*len(trans)
    print("Minimum support count is: ",min_sup,"\n")
    min_conf = float(input("Enter minimum confidence: "))
    """
    
    min_sup_perct=0.15
    min_sup = min_sup_perct * len(trans)
    min_conf=0.75


    items=item_counter(trans, min_sup)
    prev_support_matrix=[]
    support_matrix=items
    i=1
    while(support_matrix):
        i+=1
        prev_support_matrix=support_matrix
        support_matrix=calculate_support(i,support_matrix,trans, items, min_sup)

    print("association rules: ")
    association(trans,prev_support_matrix,min_conf)

main("GroceryStoreDataSet.csv")

