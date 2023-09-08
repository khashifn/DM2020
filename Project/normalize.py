import os
import numpy as np

def normalize(path):
    lst=[]
    vallst=[]
    for filename in os.listdir(os.getcwd()+'\\'+path):
        with open(os.path.join(os.getcwd()+'\\'+path, filename), 'r') as f:
            for i in f.readlines():
                lst.append(float(i.split()[0]))
                vallst.append(float(i.split()[1]))
    temp=[x for _,x in sorted(zip(lst,vallst))]
    nptemp=np.array(temp)
    nptemp=nptemp/np.max(nptemp)
    with open(path+'.txt','w') as fp:
        for i in range(nptemp.shape[0]):
            fp.write('{}\t{}'.format(i,nptemp[i]))
            fp.write('\n')
