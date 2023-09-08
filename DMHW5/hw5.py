# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:25:20 2020

@author: Yas
"""
import numpy as np

#if items are not number they must be converted to number for this implantation to work
with open('retail.dat','r') as data:
    retail=[]
    lines=data.readlines()
    for k in lines:
        retail.append(k.split())

#counts itemlists in basket
        
#hadaf az yeki kardan tabe count va sakhtane bitmap in bude ke ba falsafe koli sazegar bashad,
#yani hengami bitmap sakhte shavad ke baraye shomaresh be disk dastrasi darim va bayad dastrasi be disk
#ra minimum konim

def count(baskets,items_list,pcy=False,pcy_item=None,support=None,l=1000000):
    target=set(items_list)
    counter=0
    total=len(baskets)
    hashtable=np.zeros(l)
#if we are using pcy alg. when counting for each level, it starts counting for creating bitmap data
    if pcy:
        for basket in baskets:
            for items in pcy_item:
                if set(basket).issuperset(items):
                    hashtable[pcyhash(items,l)]+=1
            if set(basket).issuperset(target):
                counter+=1
    else:
        for basket in baskets:
            if set(basket).issuperset(target):
                counter+=1
    if not pcy:
        return counter
    else:
        bitmap= (hashtable/total) > support
        return counter , bitmap

#Hash function for PCY
def pcyhash(itemset,l):
    a=1
    for item in itemset:
        a=a*(int(item)+1)
    return (a%l)

#joins old sets to create new sets
def joinSet(itemSet, length,pcy=False,bitmap=None,l=1000000):
    temp=[]
    for items in itemSet:
        for items_ in itemSet:
            if len(items.union(items_)) == length:
                temp.append(items.union(items_))
    temp2=[]
#if all the subsets of an itemlist is in the previous level then
#the itemlist must be generated (length*(length-1)) times
#if Using PCY it check bitmap created last level before creating frequent set for next level      
    for items in temp:
        if pcy:
            if bitmap[pcyhash(items,l)]:
                if temp.count(items)==(length*(length-1)):
                    if not items in temp2:    
                        temp2.append(items)
        else:
            if temp.count(items)==(length*(length-1)):
                if not items in temp2:    
                    temp2.append(items)
    return temp2

#creating frequent sets with length of 1 in apriori 
def l1(baskets,support):
    l1dict={}
    total=len(baskets)
#reading each basket and counting each element
    for basket in baskets:
        for item in basket:
            if item in l1dict.keys():
                l1dict[item]+=1
            else:
                l1dict[item]=1
    items=list(l1dict.keys())
    item_set=[]
    supports=[]
#checking supports
    for item in items:
        if (l1dict[item]/total) >= support:
            item_set.append(set([item]))
            supports.append(l1dict.pop(item))
    return item_set,supports
#apriori main function
#returns different level item sets and their supports
def apriori(baskets,support):
    aprioridata={}
    supportsdata={}
    total=len(baskets)    
#creates l1 frequent sets
    current_set,support_list=l1(baskets,support)
#saving data of each level 
    aprioridata[1]=current_set
    supportsdata[1]=support_list
    level=2
    last_set=current_set
#runs untill there is no item in created frequent set
#in each iteration creates possible frequent sets based on last iteration frequent items    
    while(True):
        current_set=[]
        support_list=[]
#creates possible frequent set
        last_set=joinSet(last_set,level)
        print('Apriori level', level ,'\nNumber of candidates:',len(last_set), '\nCandidates:\n', last_set)
#counting and checking for frequent sets        
        for item in last_set:
            sup=count(baskets,item)/total
            if sup > support:
                current_set.append(item)
                support_list.append(sup)
#end condition        
        if len(current_set)<1:
            break
#saving data of each level
        aprioridata[level]=current_set
        supportsdata[level]=support_list
        last_set=current_set
        level+=1
    return aprioridata,supportsdata

#creating frequent sets with length of 1 in pcy
def pcyl1(baskets,support,l=1000000):
    l1dict={}
    total=len(baskets)
    hashtable=np.zeros(l)
    for basket in baskets:
        l2itemset=set([])
#k_ is just a copy of each basket in format of a frozen set for creating next item set
        k_=[]
        for item in basket:
            k_.append(frozenset([item]))
            if item in l1dict.keys():
                l1dict[item]+=1
            else:
                l1dict[item]=1
        l2itemset=joinSet(k_,2)
        for items in l2itemset:
            hashtable[pcyhash(items,l)]+=1
    itemlist=list(l1dict.keys())
    item_set=[]
    supports=[]
    for item in itemlist:
        if (l1dict[item]/total) >= support:
            item_set.append(set([item]))
            supports.append(l1dict.pop(item))
    bitmap=list((np.array(hashtable)/total)>support)
    return item_set,supports,bitmap


#Main PCY function
#returns different level item sets and their supports and **bitmaps data(removed)
def pcy(baskets,support,l=1000000):
    total=len(baskets)
    pcydata={}
    supportsdata={}
    #bitmapsdata={}
#creates l1 frequent set and l2 bitmap
    current_set,support_list,bitmap=pcyl1(baskets,support,l=1000000)
    pcydata[1]=current_set
    supportsdata[1]=support_list
    #bitmapsdata[1]=bitmap
    level=2
    last_set=current_set
    while(True):
        l=l//2
        current_set=[]
        support_list=[]
#creating possible frequent set with checking bitmap created level before
        last_set=joinSet(last_set,level,True,bitmap,l)
        print('PCY level', level ,'\nNumber of candidates:',len(last_set), '\nCandidates:\n', last_set)
#creating possible next level itemsets to create bitmap
        pcy_set=joinSet(last_set,level+1)
        for c,items in enumerate(last_set):
            if c==len(last_set)-1:
                sup,bitmap=count(baskets,items,True,pcy_set,support,l)
            else:
                sup=count(baskets,items)
            sup=sup/total
            if sup > support:
                current_set.append(items)
                support_list.append(sup)
        if len(current_set)<1:
            break
#saving data        
        pcydata[level]=current_set
        supportsdata[level]=support_list
        #bitmapsdata[level]=bitmap
#updating for next iteration
        last_set=current_set
        level+=1
    return pcydata,supportsdata



apriori_freq_itemsets,apriori_supports=apriori(retail,0.03)
pcy_freq_itemsets,pcy_support=pcy(retail,0.03)
print('apriori item sets:',apriori_freq_itemsets)
print('pcy item sets:',pcy_freq_itemsets)

