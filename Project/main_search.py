# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 02:14:44 2020

@author: Yas
"""
import numpy as np
import json
def load_rank_vec(name):
    lst=[]
    vallst=[]
    with open(name) as fp:
        for i in fp.readlines():
                lst.append(float(i.split()[0]))
                vallst.append(float(i.split()[1]))
    ranks=[x for _,x in sorted(zip(lst,vallst))]
    ranks=np.array(ranks)
    return ranks

def search(mystr,dataset,cat=None):     
    #Selecting pagerank matrix
    if cat is None:
        rank='R_9.txt'
    elif cat=='news':
        rank='R_news_9.txt'
    elif cat=='sport':
        rank='R_sport_9.txt'
    elif cat=='fun':
        rank='R_fun_9.txt'
    
    ranks=load_rank_vec(rank)
    hubs=load_rank_vec('h_10.txt')
    auts=load_rank_vec('a_9.txt')
    
    nodes=[]
    
    for i in dataset:
        #listing nodes containing searched string 
        if mystr.lower() in i['content'].lower():
            nodes.append(i['id'])
            
    result=[x for _,x in sorted(zip(ranks[nodes],nodes))]
    hresult=[x for _,x in sorted(zip(hubs[nodes],nodes))]
    aresult=[x for _,x in sorted(zip(auts[nodes],nodes))]
    return result,hresult,aresult

def load_documents(filename):
    with open(filename) as fp:
        documents = json.load(fp)['websites']
    return documents

data=load_documents('DATASET.json')

res,hres,ares=search('race',data)
p1res,_,_=search('race',data,cat='fun')
p2res,_,_=search('race',data,cat='news')
p3res,_,_=search('race',data,cat='sport')
print('Searching "race"')
print('simple search')
print(res)
print('searching in fun category')
print(p1res)
print('searching in news category')
print(p2res)
print('searching in sport category')
print(p3res)
print('searching in hubs')
print(hres)
print('searching in authorities')
print(ares)