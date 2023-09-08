# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:45:58 2020

@author: Yas
"""
import numpy as np
import json

def load_documents(filename):
    with open(filename) as fp:
        documents = json.load(fp)['websites']
    return documents

def matrixgenerator(dic):
    L=np.zeros([len(dic),len(dic)])
    pvec=np.zeros([len(dic),3])    
    for i in dic:
#creating link matrix
        L[i['links'],i['id']]=1
#subject personalize vectors
        if i['category']=='news':
            pvec[i['id'],0]=1
        elif i['category']=='sport':
            pvec[i['id'],1]=1
        else:
            pvec[i['id'],2]=1
    return L,pvec

def pagerank(L,personalize=False,pvec=None,pweight=2,alpha=0.85,maxiter=1000,epsilon=10**-6):
    q=L/(np.sum(L,axis=0)+(np.sum(L,axis=0)==0)*np.ones(L.shape[1]))
    n=q.shape[0]
    r=(1/n)*np.ones([n,1])
    e=np.ones([n,1])    
    d= (-1*np.sum(q,axis=0)+1).reshape([1,n])
    #solving deadend(no outlink) problem by giving the surfer ability to go to any node from deadends.
    P=q+(1/n)*np.dot(e,d)
    #solving spidertraps problem by giving the surfer ability to teleport form anywhere to any other node
    if not personalize:
        A=alpha*P+(1-alpha)*(1/n)*np.dot(e,e.transpose())
    else:
        pvec=pvec.reshape([n,1])
        A=alpha*P+(1-alpha)*(1/np.sum(e+(pweight*pvec)))*(np.dot(e+(pweight*pvec),e.transpose()))
    return A


data=load_documents('DATASET.json')

Linkmatrix,Pmatrix=matrixgenerator(data)

A=pagerank(Linkmatrix)
A_news=pagerank(Linkmatrix,personalize=True,pvec=Pmatrix[:,0])
A_sport=pagerank(Linkmatrix,personalize=True,pvec=Pmatrix[:,1])
A_fun=pagerank(Linkmatrix,personalize=True,pvec=Pmatrix[:,2])

with open('Hvec.txt','w') as fp:
    for i in range(Linkmatrix.shape[0]):
        fp.write('{}\t{}'.format(i,float(1)))
        fp.write('\n')

with open('L.txt','w') as fp:
    for i in range(Linkmatrix.shape[0]):
        for j in range(Linkmatrix.shape[1]):
            fp.write('{} {} {}'.format(i,j,float(Linkmatrix[i,j])))
            fp.write('\n')

with open('R.txt','w') as fp:
    for i in range(A.shape[0]):
        fp.write('{}\t{}'.format(i,1/A.shape[0]))
        fp.write('\n')
        
with open('A.txt','w') as fp:
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            fp.write('{} {} {}'.format(i,j,A[i,j]))
            fp.write('\n')

with open('A_news.txt','w') as fp:
    for i in range(A_news.shape[0]):
        for j in range(A_news.shape[1]):
            fp.write('{} {} {}'.format(i,j,A_news[i,j]))
            fp.write('\n')
        
with open('A_sport.txt','w') as fp:
    for i in range(A_sport.shape[0]):
        for j in range(A_sport.shape[1]):
            fp.write('{} {} {}'.format(i,j,A_sport[i,j]))
            fp.write('\n')
            
with open('A_fun.txt','w') as fp:
    for i in range(A_fun.shape[0]):
        for j in range(A_fun.shape[1]):
            fp.write('{} {} {}'.format(i,j,A_fun[i,j]))
            fp.write('\n')

with open('A_test.txt','w') as fp:
    for i in range(A.shape[0]):
        fp.write('{} {}'.format(i,A[i,:]))
        fp.write('\n')

        