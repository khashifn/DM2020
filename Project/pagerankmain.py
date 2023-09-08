from mrjob.job import MRJob
from PageRank import PageRank
import os

            
    
def rank_generator(cat=None,max_iter=10):
    if cat is None:
        input_file='A.txt'
        output_dir = 'R_{}/'
    elif cat=='news':
        input_file='A_news.txt'
        output_dir = 'R_news_{}/'
    elif cat=='sport':
        input_file='A_sport.txt'
        output_dir = 'R_sport_{}/'    
    elif cat=='fun':
        input_file='A_fun.txt'
        output_dir = 'R_fun_{}/'
    rank='R.txt'
    iteration = 0
    running = True
    while running:
        print('Running iteration {}'.format(iteration + 1))
        if iteration == 0:
            job = PageRank([input_file,rank,
                         '--output-dir=' + output_dir.format(iteration)])
        else:
            job = PageRank([input_file, output_dir.format(iteration - 1) + '*', '--output-dir=' + output_dir.format(iteration)])    
        with job.make_runner() as runner:
            runner.run()
            
        iteration += 1
        if (iteration==max_iter):
            break
    rank_vector_generator(output_dir.format(iteration-1))
        
def rank_vector_generator(path):
    lst=[]
    vallst=[]
    for filename in os.listdir(os.getcwd()+'\\'+path):
        with open(os.path.join(os.getcwd()+'\\'+path, filename), 'r') as f:
            for i in f.readlines():
                lst.append(float(i.split()[0]))
                vallst.append(float(i.split()[1]))
    temp=[x for _,x in sorted(zip(lst,vallst))]
    with open(path[:-1]+'.txt','w') as fp:
        for i in range(len(temp)):
            fp.write('{}\t{}'.format(i,temp[i]))
            fp.write('\n')


if __name__ == '__main__':
    for i in [None,'news','sport','fun']:
        rank_generator(cat=i,max_iter=10)
        
        