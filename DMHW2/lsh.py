import numpy as np

#preparing text to extract shingles
def preprocess(mystring):
    punctuation = [",", "!", "?", ".", "%", "/", "(", ")"]
    for i in punctuation:
        mystring=mystring.replace(i,' ')
    lst=mystring.split()
    for i in range(lst.count('')):
        lst.remove('')
    mystring=' '.join(lst)
    return mystring

#extracting K-lenght shingles
def shingling(mystring,k):
    shingles=[]
    for i in range(len(mystring)):
        shingles.append(mystring[i:i+k])
    return shingles

#Creating minhash matrix from shingles
def minhash(mainshingle,shingles):
    vec=np.zeros((len(mainshingle),len(shingles)))
    for i,j in enumerate(shingles.values()):
        for k in j:
            idx=mainshingle.index(k)
            vec[idx,i]=1
    return vec

#Creating permutations from minhash matrix
def permutation(mainshingle,k):
    t=len(mainshingle)
    permut=np.zeros([k,t])
    for i in range(k):
        permut[i,:]=np.random.permutation(t)
    return permut

#updating signature values
def updatesig(ridx,cidx,sig,permuts):
    for i,val in enumerate(sig[:,cidx]):
        if permuts[i,ridx]<val:
            sig[i,cidx]=permuts[i,ridx]
    return sig

#signature creating function
def signature(matrix,permuts):
    signmatrix=np.full((permuts.shape[0] , matrix.shape[1]), np.inf)
    for ridx,row in enumerate(matrix):
        for cidx,val in enumerate(row):
            if val==0:
                continue
            else:
                signmatrix=updatesig(ridx,cidx,signmatrix,permuts)
    return signmatrix

#creates random vector for hashing
def hashvec(a,b):
    return np.random.randn(a,b)
#int to bool convertor
def int2bool(vec):
    return 1*(vec>0)

#LSH function    
def lsh(signatures,b,r):
    hashtable={}
    for i in range(b):
        hashtable['h'+str(i)]={}
        #creates random vectors
        hashingvec1=hashvec(r,1)
        hashingvec2=hashvec(r,1)
        #hashing data
        vec1=np.multiply(hashingvec1,signatures[i*r:(i+1)*r,:])
        vec2=np.multiply(hashingvec2,signatures[i*r:(i+1)*r,:])
        #converting to boolean
        vec1=int2bool(vec1)
        vec2=int2bool(vec2)
        hashedvals=np.concatenate((vec1,vec2),axis=0)
        for j in range(signatures.shape[1]):
            try:
                hashtable['h'+str(i)][str(hashedvals[:,j])]+=[j]
            except KeyError:
                hashtable['h'+str(i)].update({str(hashedvals[:,j]):[j]})
    return hashtable


#similarity check function
def simcheck(signatures,hashtable):
    comparison_list=[]
    num=signatures.shape[0]
    datasize=signatures.shape[1]
    compmatrix=np.zeros((datasize,datasize))
    simmatrix=np.zeros((datasize,datasize))
    #creating candidate matrix
    for i in hashtable.values():
        for j in i.values():
            if len(j)>1 and len(j)<100:
                comparison_list.append(j)
                for p in j:
                    for q in j:
                        compmatrix[p,q]=1
    #creating similarity matrix
    for i in range(datasize):
        for j in range(i+1,datasize):
            simmatrix[i,j]=np.sum(signatures[:,i]==signatures[:,j])/num
    return simmatrix

#gets similarity matrix and threshold and returns file name
def simpairs(simmatrix,threshold):
#(+1 is to get file name)
    return np.argwhere(simmatrix>threshold)+1
#reading texts and calling shingle functions
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
#removing duplicates and sorting them
mainshingle_sorted=set(mainshingle)
mainshingle_sorted=list(mainshingle_sorted)
mainshingle_sorted.sort()
print(len(mainshingle_sorted))
#creating minhash matrix
minhashmatrix=minhash(mainshingle_sorted,shingles)
#creating signatures
permuts=permutation(mainshingle_sorted,100)
signatures=signature(minhashmatrix,permuts)
#finding similarities
hashtable=lsh(signatures,20,5)
simmatrix=simcheck(signatures,hashtable)
similardocs=simpairs(simmatrix,0.5)
#final results
print(similardocs)