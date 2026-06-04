import numpy as np
import os


path = './hop-0.001/w_state/'

for i in os.listdir(path):
    
    file = os.path.join(path, i)
    
    if os.path.isfile(file) and 'states-' in i:
        
        wList.append(float(i.replace(f'states-','').replace('.txt', '')))
        
wList.sort()