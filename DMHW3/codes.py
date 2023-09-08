import pandas as pd
import random

data=pd.read_excel('DK Dataset 2018-08-20.xlsx')
state_name=data['state_name']
pid=data[['product_id','state_name']]


####moments
class counter:
    def __init__(self,value=None,count=0):
        self.value=value
        self.count=count
    def counter(self):
        self.count+=1
    def reset(self,val):
        self.count=0
        self.value=val
        
class moment:   
    def __init__(self,states=[],counters=10):
        #number of counters
        self.counters=counters
        #states list
        self.states=states
        #total stream lenght
        self.totalnum=0
        #stream lenght in each state
        self.statenum=[]
        #counter lists
        self.sclist=[]
        #creating counter for pre difined states
        for j in range(len(self.states)):
            temp=[]
            self.statenum.append(0)
            for i in range(self.counters):
                temp.append(counter())
            self.sclist.append(temp)
    
    def add_state(self,state):
        #addind a new state to state list
        self.states.append(state)
        self.statenum.append(0)
        temp=[]
        for i in range(self.counters):
            temp.append(counter())
        self.sclist.append(temp)
    
    def counter_available(self,state_index):
        #checks if there is a free counter or not
        for i in self.sclist[state_index]:
            if i is None:
                return True
        return False
    
    def counter_vals(self,state_index):
        #creates a list from counter values for finding counter index if it needs update
        temp=[]
        for i in self.sclist[state_index]:
            temp.append(i.value)
        return temp
    
    def update_counter(self,state_index,value):
        #assigning a new value for a counter
        c_num=random.randrange(self.counters)
        self.sclist[state_index][c_num].reset(value)
        
    def assign_new_counter(self,state_index,value):
        #assiging new counter (not used) to a value
        for i in self.sclist[state_index]:
            if i is None:
                i.reset(value)
                
    def countvals(self,state_index,value):
        #finding indexes related to value
        index=[i for i, j in enumerate(self.counter_vals(state_index)) if j == value]
        for i in index:
            self.sclist[state_index][i].counter()

    def new_item(self, product_id , state_name):
        #counting total lenght of stream
        self.totalnum+=1
        #checking if the state has occourd before or not, if not add it to the list
        try:
            state_index=self.states.index(state_name)
        except ValueError:
            self.add_state(state_name)
            state_index=self.states.index(state_name)
        #counting stream related to the state 
        self.statenum[state_index]+=1
        #checking for empty counter
        if self.counter_available(state_index):
            self.assign_new_counter(state_index,product_id)  
        #if no empty counter check to see if any counter should be updated
        elif random.random()<(self.counters/self.statenum[state_index]):
            self.update_counter(state_index,product_id)
        #counting
        self.countvals(state_index,product_id)
    def calc(self):
        #calculates moments
        temp=[]
        for i in range(len(self.states)):
            moments=0
            for j in self.sclist[i]: 
                moments+=self.statenum[i]*((2*j.count)-1)
            moments/=self.counters
            temp.append(moments)
        return dict(zip(self.states,temp))
######flajolet_martin functions
def hash_function(mystr,size=1024):
    return (sum(mystr.encode()))%size

def counting_zeros(num,size=1024):
    counter=0
    if num==0:
        num=size
    while(True):
        if num%2:
            break
        counter+=1
        num=num/2
    return counter

#######

mymax=0        
for i in state_name:
    temp=counting_zeros(hash_function(i))
    if mymax < temp:
        mymax=temp
estimated=2**mymax

print('estimated value from flajolet martin is: ',estimated)

test=moment(counters=100)
for i in pid.iterrows():
    s_name=i[1]['state_name']
    p_id=i[1]['product_id']
    test.new_item(p_id,s_name)
print(test.calc())
    
