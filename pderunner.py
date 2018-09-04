from sys import exit
from os import remove
import numpy as np
import pickle
from subprocess import run
from splitter import split_into_groups
from pathlib import Path
import path_conf
import time

def main():
    temperatures = np.array([25.0])
    ums = np.array([-13.0*10.0**(-3.0)]) 
    phases = ['i']
    cells_ferro = np.array([15.0])
    cells_para = cells_ferro / 2
    thickness = np.array([10.0])
    sigma = np.linspace(0.0, 1.0, 1000)
    need_prev = [False] + [True] * (len(sigma) - 1)

    chunks = 1

    unique_names_container = 'unique_names_container'
    unpath = Path('./{}'.format(unique_names_container))
    if unpath.exists():
        for f in unpath.iterdir():
            if f.is_file():
                remove(f)
    else:
        unpath.mkdir()
    
    unique_names = ['{:0>10}'.format(str(i)) for i in range(chunks)]

    with open('calculation_template') as template:
        calculation_template = template.readlines()
    for nn, spl in enumerate(split_into_groups(fields, chunks, offset = True)):
        args = {'temperatures' : {'name' : 't', 'order' : 0, 'values' : temperatures}, 
                'need_prev' : {'name' : 'need_prev', 'order' : 0, 'values' : need_prev},
                'sigma' : {'name' : 'sigma', 'order' : 1, 'values' : sigma},
                'ums' : {'name' : 'um', 'order' : 0, 'values' : ums},  
                'phases' : {'name' : 'phase', 'order' : 0, 'values' : phases},
                'cells_ferro' : {'name' : 'ferro_width', 'order' : 0, 'values' : cells_ferro},
                'cells_para' : {'name' : 'para_width', 'order' : 0, 'values' : cells_para},
                'thickness' : {'name' : 'thickness', 'order' : 0, 'values' : thickness}} 
        uniname = str(unpath.joinpath(unique_names[nn]))
        
        with open(uniname, 'wb') as output:
            pickle.dump(args, output, pickle.HIGHEST_PROTOCOL)
          
        run_line = '{} pde.py --sfile {}'.format(path_conf.python_path, uniname)
        job_name = 'job_{}.sh'.format(nn)
        
        try:
            with open(job_name, 'w') as new_job:
                new_job.writelines(calculation_template)
                new_job.write('\n')
                new_job.write(run_line)
        except Exception as e:
            print(e)
            exit(1)

        retcode = run("bash {}".format(job_name), shell=True)
        
if __name__ == '__main__':
    main()
