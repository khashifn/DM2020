import numpy as np
import pandas as pd
import Kmeans as km


class cluster:

    def __init__(self,points=None):
        if points is not None:
            self.f=points.shape[1]
            self.n=points.shape[0]
            self.sum=np.sum(points,axis=0).reshape([1,self.f])
            self.sqsum=np.sum(np.multiply(points,points),axis=0).reshape([1,self.f])
        else:
            self.f=None
            self.n=None
            self.sum=None
            self.sqsum=None

    def add_point(self,point):
        point=point.reshape([1,len(point)])            
        if self.n is None:
            self.n=1
            self.sum=point
            self.sqsum=np.sum(np.multiply(point,point),axis=0,keepdims=True)
        else:
            self.n+=1
            self.sum+=point
            self.sqsum+=np.sum(np.multiply(point,point),axis=0,keepdims=True)

    def std(self):
        return np.sqrt(((self.sqsum/self.n)-(self.sum/self.n)**2))

    def centroid(self):
        return self.sum/self.n

    def nozerostd(self):
        return (self.std()!=0).all()

#merging 2 clusters
def merge_cluster(c1,c2):
    c=cluster()
    c.f=c1.f
    c.n=c1.n+c2.n
    c.sum=c1.sum+c2.sum
    c.sqsum=c1.sqsum+c2.sqsum
    return c


def mahalanobis(point,cluster):
    return np.linalg.norm(np.divide(point-cluster.centroid(),cluster.std()))

def euclidien(point, cluster):
    return np.linalg.norm(point-cluster.centroid())

def shuffle(data,ids):
    ids=np.random.permutation(ids)
    data=data[ids-1,:]
    return data,ids

#initializing clusters based on Kmeans centroids on first chunk of data
#algorithm continues to joins points to cluster until std on all dimensions is non zero
#if std is zero mahalanobis distance is not usable
def init_clusters(data,centroids):
    ds=[]
    cid=[i for i in range(data.shape[0])]
    for i in range(centroids.shape[0]):
        for j in range(len(cid)):
            best=np.inf
            idx=np.inf
            dist=np.linalg.norm(data[cid[j],:]-centroids[i,:])
            if best>dist:
                idx=j
                best=dist
        ds.append(cluster(data[idx,:].reshape([1,data.shape[1]])))
        cid.pop(idx)
        while not ds[-1].nozerostd():
            best=np.inf
            idx=np.inf
            for k in range(len(cid)):
                dist=euclidien(data[cid[k],:].reshape([1,data.shape[1]]),ds[-1])
                if best>dist:
                    idx=k
                    best=dist
            ds[-1].add_point(data[cid[idx],:])
            cid.pop(idx)
    return ds,cid

#checks to see if merged std is in threshold or not
def merge_check(c1,c2,t_merge):
    c=merge_cluster(c1,c2)
    c_std=c.std()
    c1_std=c1.std()
    c2_std=c2.std()
    if (c_std<(c1_std+c2_std)*t_merge).all():
        return True
    return False
#main algorithm
def BFR(data,chunksize=50,K=5,t_m=3,t_e=10,t_merge=1):
#ds - discard set
#cs - compressed set
#rs - retained set    
    compressed_set=[]
    retained_set=np.empty([0,data.shape[1]])
    if data.shape[0]%chunksize==0:
        chunkno=data.shape[0]//chunksize
    else:
        chunkno=data.shape[0]//chunksize+1
        
    for chunknumber in range(chunkno):
        print('chunk',chunknumber)
        if (chunknumber+1)*chunksize>data.shape[0]:
            chunkdata=data[chunknumber*chunksize:,:]
        else:
            chunkdata=data[chunknumber*chunksize:(chunknumber+1)*chunksize,:]   
        #initializing clusters based on 
        if chunknumber==0:
            _,centroids=km.runkmeans(chunkdata,10)
            detained_set,not_used_ids=init_clusters(chunkdata,centroids[K-2])
            chunkdata=chunkdata[not_used_ids,:]    
        
        ids=[idx for idx in range(chunkdata.shape[0])]
        used_ids=[]
       
        #updating detained set
        print('updating detained set')
        for j in ids:
            ds_best_dist=np.inf
            ds_best_idx=np.inf
            for k in range(len(detained_set)):
                dist=mahalanobis(chunkdata[j,:].reshape([1,chunkdata.shape[1]]),detained_set[k])
                if ds_best_dist>dist:
                    ds_best_dist=dist
                    ds_best_idx=k
            if ds_best_dist < t_m:
                detained_set[ds_best_idx].add_point(chunkdata[j,:])
                used_ids.append(j)
        for j in used_ids:
            ids.remove(j)
        
        j=0
        #updating compressed set
        print('updating compressed set')
        while(j<len(ids)):
            close=[]
            for k in range(j+1,len(ids)):
                if (np.linalg.norm(chunkdata[ids[j],:]-chunkdata[ids[k],:])<t_e):
                    close.append(ids[k])
            if len(close)>0:
                close.append(ids[j])
                compressed_set.append(cluster(chunkdata[close,:]))
                for k in close:
                    ids.remove(k)
                continue
            j+=1
        
        #updating retained set
        print('updating retained set')
        if retained_set.shape[0]<1: 
            retained_set=np.concatenate((retained_set,chunkdata[ids,:]),axis=0)
        else:
            j=0
            while(j<len(ids)):
                rids=[idx for idx in range(retained_set.shape[0])]
                close=[]
                for k in range(len(rids)):
                    if np.linalg.norm(chunkdata[ids[j],:]-retained_set[rids[k],:])<t_e:
                        close.append(rids[k])
                if len(close)>0:
                    temp=np.concatenate((chunkdata[j,:].reshape([1,chunkdata.shape[1]]),retained_set[close,:]),axis=0)
                    compressed_set.append(cluster(temp))
                    retained_set=np.delete(retained_set,close,axis=0)
                    ids.pop(j)
                    continue
                j+=1
            retained_set=np.concatenate((retained_set,chunkdata[ids,:]),axis=0)
        
        
        #merging clusters
        print('merging clusters of compressed set together')
        while(True):
            flag=False
            for clust1 in range(len(compressed_set)):
                c1=compressed_set[clust1]
                for clust2 in range(clust1+1,len(compressed_set)):
                    c2=compressed_set[clust2]
                    if merge_check(c1,c2,t_merge):
                        compressed_set.append(merge_cluster(c1,c2))
                        compressed_set.remove(c1)
                        compressed_set.remove(c2)
                        flag=True
                        break
                if flag:
                    break
            if not flag:
                break
        #merging cs with ds
        print('merging compressed set with detained set')
        while(True):
            flag=False
            for clust1 in range(len(detained_set)):
                c1=detained_set[clust1]
                for clust2 in range(len(compressed_set)):
                    c2=compressed_set[clust2]
                    if merge_check(c1,c2,t_merge):
                        detained_set[clust1]=merge_cluster(c1,c2)
                        compressed_set.remove(c2)
                        flag=True
                        break
                if flag:
                    break
            if not flag:
                break
    #merging reaminings of compressed set with Detained set        
    if len(compressed_set)>0:
        for clust1 in compressed_set:    
            bestdist=np.inf
            bestidx=np.inf
            for i,clust in enumerate(detained_set):
                dist=np.linalg.norm(clust.centroid()-clust1.centroid())
                if dist<bestdist:
                    bestdist=dist
                    bestidx=i
            detained_set[bestidx]=merge_cluster(clust1,detained_set[bestidx])
    #merging reaminings of retained set with Detained set
    if retained_set.shape[0]>0:
        for k in range(retained_set.shape[0]):
            bestdist=np.inf
            bestidx=np.inf
            for i,clust in enumerate(detained_set):
                dist=euclidien(retained_set[k,:], clust)
                if dist<bestdist:
                    bestdist=dist
                    bestidx=i
            detained_set[bestidx].add_point(retained_set[k,:])
    print('mission complete')
    return detained_set
#prediction function
def BFR_pred(clusters,data):
    distances=np.zeros([data.shape[0],len(clusters)])
    eudistances=np.zeros([data.shape[0],len(clusters)])
    for i in range(data.shape[0]):
        for j,clust in enumerate(clusters):
            distances[i,j]=mahalanobis(data[i,:],clust)
            eudistances[i,j]=euclidien(data[i,:],clust)
    labels=np.argmin(distances,axis=1).reshape([data.shape[0]])
    cost=0
    for i in range(data.shape[0]):
        cost+=eudistances[i,labels[i]]
    return labels,cost
            
pddata=pd.read_csv('customers.csv')
data=pddata[['Annual Income (k$)','Spending Score (1-100)']].to_numpy(dtype=float)
ids=pddata['CustomerID'].to_numpy()
sdata,sids=shuffle(data,ids)
#Runing Kmeans to find K for first chunk of data
costs,centroids=km.runkmeans(sdata[:40,:],10)
print(costs)
K=4
print(centroids[K-2])

#costlist,centroids=km.runkmeans(data)
costs,centroids=km.runkmeans(sdata,10)
preds=km.predict(data,centroids[K-2])    

print('Kmeans Results')
for i in range(K):
    print(centroids[K-2][i])
    print(np.sum(preds==i))


A=BFR(sdata,chunksize=50,K=K,t_m=3,t_e=20,t_merge=.1)
print('BFR Results')
bfrcent=[]
for k in A:
    print(k.centroid())
    print(k.n)
    bfrcent.append(np.squeeze(k.centroid()))

#checking BFR cost against Kmeans:
_,cost=BFR_pred(A,data)
print('bfr cost based on bfr prediction:' , cost)

_,cost=km.findclosestcentroid(data,np.array(bfrcent))
print('bfr cost based on kmeans prediction:' , cost)

print('kmeans cost:',costs[K])