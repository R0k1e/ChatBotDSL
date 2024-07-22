import os
import subprocess
from datetime import datetime
    
if not os.path.isdir('test_log'):
    os.mkdir('test_log')

if not os.path.isdir('test_out'):
    os.mkdir('test_out')
    
if not os.path.isdir('test_in'):
    os.mkdir('test_in')
    print('Please put the test input file in test_in')
    exit()

if not os.path.isdir('test_program'):
    os.mkdir('test_program')
    print('Please put the test program file in test_program')
    exit()


for file_name in os.listdir('test_program'):
    file_path = os.path.join('test_program', file_name)
    in_path = os.path.join('test_in', file_name  )
    out_path = os.path.join('test_out', file_name + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') )
    
    
    if os.path.isfile(file_path):
        log_file = os.path.join('test_log', (file_name + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.log' ))
        with open(log_file, 'w') as f:
            subprocess.run(['python', 'main.py', '--program_file', file_path, '-i', in_path, '-o', out_path, '-d', '-m', 'file'], stdout=f, stderr=f)

