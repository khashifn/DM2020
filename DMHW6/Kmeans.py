import numpy as np
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
def predict(data,centroids):
    distances=np.zeros([data.shape[0],centroids.shape[0]])
    for k in range(centroids.shape[0]):
        distances[:,k]=np.linalg.norm(data-centroids[k,:],axis=1).reshape([data.shape[0]])
    labels=np.argmin(distances,axis=1).reshape([data.shape[0]])
    return labels
def runkmeans(data,max_k=100,max_iter=50):
    costlist=np.empty((max_k+1))
    costlist[:]=np.nan
    finalcent=[]
    for k in range(2,max_k+1):
        centroids=initcentroids(data,k)
        bestcost=np.inf
        counter=0
        for j in range(max_iter):
            labels,cost=findclosestcentroid(data,centroids)
            if bestcost>cost:
                counter=0
                bestcost=cost
                bestcentroids=centroids
            else:
                counter+=1
            centroids=computecentroids(data,labels,k)
            if counter > 5:
                break
        finalcent.append(bestcentroids)
        costlist[k]=bestcost
    return costlist,finalcent


