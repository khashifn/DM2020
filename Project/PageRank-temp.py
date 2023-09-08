import numpy as np
import json


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


def search(mystr,dataset,Linkmatrix,Pmatrix,cat=None):     
    #creating Q matrix from Link matrix
    Qmatrix=l_to_q(Linkmatrix)
    #ranking pages
    if cat is None:
        Pagerank=pagerank(Qmatrix)
    elif cat=='news':
        Pagerank=pagerank(Qmatrix,personalize=True,pvec=Pmatrix[:,0])
    elif cat=='sport':
        Pagerank=pagerank(Qmatrix,personalize=True,pvec=Pmatrix[:,1])
    elif cat=='fun':
        Pagerank=pagerank(Qmatrix,personalize=True,pvec=Pmatrix[:,2])
    #h&a vectors    
    Hvec,Avec=h_and_a(Linkmatrix)
    
    nodes=[]

    for i in dataset:
        #listing nodes containing searched string 
        if mystr.lower() in i['content'].lower():
            nodes.append(i['id'])
    #sorting based on ranking vector        
    result=[x for _,x in sorted(zip(Pagerank[nodes],nodes))]
    hresult=[x for _,x in sorted(zip(Hvec[nodes],nodes))]
    aresult=[x for _,x in sorted(zip(Avec[nodes],nodes))]    
    return result,hresult,aresult
#loads documents    
def load_documents(filename):
    with open(filename) as fp:
        documents = json.load(fp)['websites']
    return documents
#creates q matrix from Link matrix
def l_to_q(L):
#second part of sum is for stopping divide by zero    
    return L/(np.sum(L,axis=0)+(np.sum(L,axis=0)==0)*np.ones(L.shape[1]))

#page rank algorithm
def pagerank(q,personalize=False,pvec=None,pweight=2,alpha=0.85,maxiter=1000,epsilon=10**-6):
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
    i=0;
    while (np.linalg.norm((r-np.dot(A,r)))>=epsilon):
        i=i+1
        r=np.dot(A,r)
        if i==maxiter: 
            break;
    return r

#H&A algorithm
def h_and_a(L,maxiter=1000,epsilon=10**-6):
    h=np.ones([L.shape[0],1])
    a=np.ones([L.shape[0],1])
    i=0
    while (True):
        i+=1
        temp_a=a
        temp_h=h
        a=np.dot(L,h)
        a=a/np.max(a)
        h=np.dot(L.transpose(),a)
        h=h/np.max(h)
        if np.linalg.norm(h-temp_h)<epsilon and np.linalg.norm(a-temp_a)<epsilon:
            break
        elif i>=maxiter:
            break
    return h,a



data=load_documents('DATASET.json')

Linkmatrix,Pmatrix=matrixgenerator(data)

res,hres,ares=search('race',data,Linkmatrix,Pmatrix)
p1res,_,_=search('race',data,Linkmatrix,Pmatrix,cat='fun')
p2res,_,_=search('race',data,Linkmatrix,Pmatrix,cat='news')
p3res,_,_=search('race',data,Linkmatrix,Pmatrix,cat='sport')
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