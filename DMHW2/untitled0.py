# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 20:59:04 2020

@author: Yas
"""

import numpy as np

#amade sazi matn ha baraye estekhraj shingle ha
def preprocess(mystring):
    #hazf alaeme negareshi
    punctuation = [",", "!", "?", ".", "%", "/", "(", ")"]
    for i in punctuation:
        mystring=mystring.replace(i,' ')
    #hazfe space haye motevali
    lst=mystring.split()
    for i in range(lst.count('')):
        lst.remove('')
    mystring=' '.join(lst)
    return mystring
#estekhraj shingle ba tul K az matn
def shingling(mystring,k):
    shingles=[]
    for i in range(len(mystring)):
        shingles.append(mystring[i:i+k])
    return shingles
#sakhtan matrix minhash az majmue kolie shingle ha va har shignle
def minhash(mainshingle,shingles):
    vec=np.zeros((len(mainshingle),len(shingles)))
    for i,j in enumerate(shingles.values()):
        for k in j:
            idx=mainshingle.index(k)
            vec[idx,i]=1
    return vec
#sakhtan permutation haye mokhtalef az jadvale minhash va dar edame sakhte signature
def permutation(mainshingle,k):
    t=len(mainshingle)
    permut=np.zeros([k,t])
    for i in range(k):
        permut[i,:]=np.random.permutation(t)
    return permut

#bakhshi az algurithm sakhte signature
#in bakhsh maghadir signature ra update mikonad
def updatesig(ridx,cidx,sig,permuts):
    for i,val in enumerate(sig[:,cidx]):
        if permuts[i,ridx]<val:
            sig[i,cidx]=permuts[i,ridx]
    return sig
#tabe aslie sakht signature
#in bakhsh ebteda yek matrix avalie signature misazad
#sepas ba raftan satr be satr dar matrix avalie va barrasi maghadir permutation ha
#maghadir signature ra update mikonad
def signature(matrix,permuts):
    signmatrix=np.full((permuts.shape[0] , matrix.shape[1]), np.inf)
    for ridx,row in enumerate(matrix):
        for cidx,val in enumerate(row):
            if val==0:
                continue
            else:
                signmatrix=updatesig(ridx,cidx,signmatrix,permuts)
    return signmatrix

#sakhtane vector random baraye hash kardan
def hashvec(a,b):
    return np.random.randn(a,b)
#tabdil vector int be bool
def int2bool(vec):
    return 1*(vec>0)
#piade sazi lsh
#in algurithm ba loop ruye band ha data haye har matn ra hash mikonad
#dar surate hash shodan do matn be yek meghdar yeksan an ha ra dar yek
#dictionary zakhire mikonad ta bad barrasi shavand
#data haye hash shode be fazaye 10 biti hash mishavand

def lsh(signatures,b,r):
    hashtable={}
    for i in range(b):
        hashtable['h'+str(i)]={}
        #sakht bordar random
        hashingvec1=hashvec(r,1)
        hashingvec2=hashvec(r,1)
        #hash kardan data ha
        vec1=np.multiply(hashingvec1,signatures[i*r:(i+1)*r,:])
        vec2=np.multiply(hashingvec2,signatures[i*r:(i+1)*r,:])
        #tabdil be boolian
        vec1=int2bool(vec1)
        vec2=int2bool(vec2)
        hashedvals=np.concatenate((vec1,vec2),axis=0)
        for j in range(signatures.shape[1]):
            try:
                hashtable['h'+str(i)][str(hashedvals[:,j])]+=[j]
            except KeyError:
                hashtable['h'+str(i)].update({str(hashedvals[:,j]):[j]})
    return hashtable

#baraye barrasi mavaredi ke mashkuk be tashaboh hastand
#dar ebteda bar asas dataye lsh matrixi tashkil midahad ke mavared moshabeh ra
#dar tamami band ha kenar ham gharar midahad va baraye har matn candid haye
#barrasi ro moshakhas mikonad
#sepas bar asase matrix ghabl ye matrix tashaboh misazim ke darsade tashaboh
#mavarede mashkuk dar an update mishavad
def simcheck(signatures,hashtable):
    comparison_list=[]
    num=signatures.shape[0]
    datasize=signatures.shape[1]
    compmatrix=np.zeros((datasize,datasize))
    simmatrix=np.zeros((datasize,datasize))
    #sakht matrix candida ha
    for i in hashtable.values():
        for j in i.values():
            if len(j)>1 and len(j)<100:
                comparison_list.append(j)
                for p in j:
                    for q in j:
                        compmatrix[p,q]=1
    #sakht matrix tashaboh
    for i in range(datasize):
        for j in range(i+1,datasize):
            simmatrix[i,j]=np.sum(signatures[:,i]==signatures[:,j])/num
    return simmatrix
#ba gereftane matrix tashaboh va threshold tayin shode va yaftan zowj haye moshabeh
def simpairs(simmatrix,threshold):
#jam shodane 1 ba location jahate tabdile location be esm file mibashad
    return np.argwhere(simmatrix>threshold)+1
        
#%%
#khandane matn ha az file va farakhani tavabe shingle 
texts={}
ptexts={}
shingles={}
mainshingle=[]

for i in range(1,437):
    txt=open("documents/"+str(i), "r").read()
    texts[i]=txt
    ptexts[i]=preprocess(txt)
    shingles[i]=shingling(ptexts[i],9)
    mainshingle+=shingles[i]

print(len(mainshingle))

#%%
#tabdile list main shingle be set jahate hazfe mavarede tekrari va sort kardane an
mainshingle_sorted=set(mainshingle)
mainshingle_sorted=list(mainshingle_sorted)
mainshingle_sorted.sort()
print(len(mainshingle_sorted))
#%%
#sakhtane matrix minhash
minhashmatrix=minhash(mainshingle_sorted,shingles)
#%%
#sakhtane signature az matrix minhash
permuts=permutation(mainshingle_sorted,100)
signatures=signature(minhashmatrix,permuts)

#%%
#piade sazi lsh va yaftane darsade tashabohe mavarede mojud
hashtable=lsh(signatures,20,5)
simmatrix=simcheck(signatures,hashtable)
similardocs=simpairs(simmatrix,0.5)
#%%
#print khuruji nahayi
print(similardocs)