import numpy as np
import matplotlib.pyplot as plt


'''
    Plot RDF for the mixture of 2 substances
'''

# RDF
def RDF_graph(file):

    bloco = 0
    j = 0
    
    with open(file, 'r') as f:
        lines = f.readlines()[3:]
        
        line = lines[0].split(' ')
        samp_size = int(line[1].strip('\n'))

        rdfAA = np.zeros(samp_size)
        rdfAB = np.zeros(samp_size)
        rdfBB = np.zeros(samp_size)
        bin = np.zeros(samp_size)

        
        for i in range(0, len(lines)):
            
            line = lines[i].split(' ')

            if(len(line) == 2):
                bloco += 1
                j = 0

            elif(len(line) > 2):
                bin[j] += float(line[1])
                rdfAA[j] += float(line[2])
                rdfAB[j] += float(line[4])
                rdfBB[j] += float(line[6])
                j += 1
        
        bin[:] = [b / bloco for b in bin]
        rdfAA[:] = [d / bloco for d in rdfAA]
        rdfAB[:] = [d / bloco for d in rdfAB]
        rdfBB[:] = [d / bloco for d in rdfBB]
    
    return bin, rdfAA, rdfAB, rdfBB

    


# MAIN

file = './isoline/rho1.05/slow-melt-test/0zhangT400.rdf'

bin, rdfAA, rdfAB, rdfBB = RDF_graph(file)

plt.plot(bin, rdfAA, label=f"H-H")
plt.plot(bin, rdfAB, label=f"O-H")
plt.plot(bin, rdfBB, label=f"O-O")

plt.xlabel('r')
plt.ylabel('RDF')
plt.legend()
plt.title('Função de Distribuição Radial - rho = 1.05 (g/cm^3)')
plt.show()

fig = plt.figure(figsize=(10,5))

plt.subplot(131)
plt.plot(bin, rdfAA, label=f"H-H", color='blue')
plt.xlabel('r')
plt.ylabel('RDF')
plt.title('H-H')

plt.subplot(132)
plt.plot(bin, rdfAB, label=f"O-H", color='orange')
plt.xlabel('r')
plt.ylabel('RDF')
plt.title('O-H')

plt.subplot(133)
plt.plot(bin, rdfBB, label=f"O-O", color='green')
plt.xlabel('r')
plt.ylabel('RDF')
plt.title('O-O')

plt.suptitle('Função de Distribuição Radial - rho = 1.05 (g/cm^3)')
plt.tight_layout()
plt.show()
