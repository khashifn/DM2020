from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol,ReprProtocol

nodeno=1000

class h(MRJob):
    INPUT_PROTOCOL = RawValueProtocol
    OUTPUT_PROTOCOL = ReprProtocol
    
    def mapper(self, _, line):
        a=line.split()
        if len(a)==2:
            for i in range(nodeno):    
                yield (i,a)
        elif len(a)==3:
            yield (int(a[0]),a[1:3])

    def reducer(self,key,values):
        lst=[]
        vals=[]
        for i in values:
            lst.append(int(i[0]))
            vals.append(float(i[1]))
        val=[x for _,x in sorted(zip(lst,vals))]
        value=0
        for i in range(nodeno):
            value+=val[2*i]*val[2*i+1]
        yield (key, value)
        

if __name__ == '__main__':
    h.run()