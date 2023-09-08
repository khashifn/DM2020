import numpy as np
import pandas as pd
#data must be a numpy array
def initcentroids(data,k):
    permut=np.random.permutation((np.arange(data.shape[0])))
    return data [permut[:k],:]

def computecentroids(data,labels,k):
    centroids=np.zeros([k,data.shape[1]])
    for i in range(k):
        centroids[i,:]=np.mean(data[labels==i],axis=0).reshape([1,data.shape[1]])
    return centroids
def findclosestcentroid(data,centroids):
    distances=np.zeros([data.shape[0],centroids.shape[0]])
    for k in range(centroids.shape[0]):
        distances[:,k]=np.linalg.norm(data-centroids[k,:],axis=1).reshape([data.shape[0]])
    labels=np.argmin(distances,axis=1).reshape([data.shape[0]])
    cost=np.sum(np.min(distances,axis=1))
    return labels,cost
def runkmeans(data,max_k=3,max_iter=10):
    costlist=np.empty((max_k-1,max_iter))
    costlist[:]=np.nan
    finalcent=[]
    selectedj=[]
    for k in range(2,max_k+1):
        costdiff=[]
        centroids=initcentroids(data,k)
        lastj=0
        for j in range(max_iter):
            labels,cost=findclosestcentroid(data,centroids)
            newcentroids=computecentroids(data,labels,k)
            costlist[k-2,j]=cost
            #stop conditions
            if j<1:
                centroids=newcentroids
                lastj=j
                continue
            costdiff.append(costlist[k-2,j-1]-costlist[k-2,j])
            if costdiff[-1]<0:
                break
            if len(costdiff)<2:
                centroids=newcentroids
                lastj=j
                continue
            if costdiff[-1]<.1*costdiff[-2]:
                break
            centroids=newcentroids
            lastj=j
        finalcent.append(centroids)
        selectedj.append(lastj)
    print(selectedj)
    return costlist,finalcent
    
                

pddata=pd.read_csv('customers.csv')
data=pddata.iloc[:,3:5].to_numpy(dtype=float)
costlist,centroids=runkmeans(data)
print(centroids)
print(costlist)