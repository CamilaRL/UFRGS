import numpy as np
import matplotlib.pyplot as plt

'''
    Plot the radial distribution function.
'''


# RDF
def RDF_graph(file):

    bloco = 0
    j = 0
    
    with open(file, 'r') as f:
        lines = f.readlines()[3:]
        
        line = lines[0].split(' ')
        samp_size = int(line[1].strip('\n'))

        rdf = np.zeros(samp_size)
        bin = np.zeros(samp_size)

        
        for i in range(0, len(lines)):
            
            line = lines[i].split(' ')

            if(len(line) == 2):
                bloco += 1
                j = 0

            elif(len(line) > 2):
                bin[j] += float(line[1])
                rdf[j] += float(line[2])
                j += 1
        
        bin[:] = [b / bloco for b in bin]
        rdf[:] = [d / bloco for d in rdf]
    
    return bin, rdf

    


# MAIN
temp = ["0.20", "0.35", "0.40", "0.45", "0.50", "0.55"]

for i in range(len(temp)):
    file_msd = f'../Two_Scale_Potential/Results/CaseB/rho_100/T{temp[i]}/tmp.data'
    print(temp[i])

    bin, rdf = RDF_graph(file_msd)

    plt.plot(bin, rdf, label=f"T {temp[i]}")

plt.xlabel('r')
plt.ylabel('RDF')
plt.legend()
plt.title('Função de Distribuição Radial\nrho = 0.100 b = -0.25')
plt.show()








