from mrjob.job import MRJob
import numpy as np
import os
from h import h
from a import a
from normalize import normalize

if __name__ == '__main__':
    input_file = 'L.txt'
    H='Hvec.txt'
    h_output_dir = 'h_{}'
    a_output_dir = 'a_{}'
    h_vec='h_{}.txt'
    a_vec='a_{}.txt'
    iteration = 0
    running = True
    while running:
        print('Running A iteration {}'.format(iteration + 1))
        if iteration == 0:
            job = h([input_file,H,
                         '--output-dir=' + a_output_dir.format(iteration)])
        else:
            job = h([input_file, h_vec.format(iteration), '--output-dir=' + a_output_dir.format(iteration)])    
        with job.make_runner() as runner:
            runner.run()
        normalize(a_output_dir.format(iteration))
        print('Running H iteration {}'.format(iteration + 1))
           
        job = a([input_file,a_vec.format(iteration),'--output-dir=' + h_output_dir.format(iteration+1)])
        with job.make_runner() as runner:
            runner.run()
        normalize(h_output_dir.format(iteration+1))
        iteration += 1
        if (iteration==10):
            break