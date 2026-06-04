import numpy as np
import matplotlib.pyplot as plt

'''
    Plot one type of particle Mean Square Displacement.
'''

# MSD
def MSD_graph(file):

    msd_x = []
    msd_y = []
    msd_z = []
    msd_tot = []
    t = []

    with open(file, 'r') as f:
        lines = f.readlines()[3:]

        for i in range(0, len(lines)-4, 5):
            
            line = lines[i].split(' ')
            t.append(float(line[0]))

            line = lines[i+1].split(' ')
            msd_x.append(float(line[1].strip('\n')))
            
            line = lines[i+2].split(' ')
            msd_y.append(float(line[1].strip('\n')))

            line = lines[i+3].split(' ')
            msd_z.append(float(line[1].strip('\n')))

            line = lines[i+4].split(' ')
            msd_tot.append(float(line[1].strip('\n')))
    

    
    plt.scatter(t, msd_tot)
    plt.xlabel('Time')
    plt.ylabel('MSD')
    plt.title('MSD Total')
    plt.show()    
    
    plt.scatter(t, msd_x)
    plt.xlabel('Time')
    plt.ylabel('MSD')
    plt.title('MSD em x')
    plt.show()

    plt.scatter(t, msd_y)
    plt.xlabel('Time')
    plt.ylabel('MSD')
    plt.title('MSD em y')
    plt.show()

    plt.scatter(t, msd_z)
    plt.xlabel('Time')
    plt.ylabel('MSD')
    plt.title('MSD em z')
    plt.show()



# MAIN

file_msd = '../NVT/msd.out'

MSD_graph(file_msd)








