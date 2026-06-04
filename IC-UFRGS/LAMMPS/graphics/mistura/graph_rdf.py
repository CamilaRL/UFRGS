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
        print(line)

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
#temp = ["0.30", "0.35", "0.40", "0.45", "0.50", "0.55", "0.60"]
temp = ["0.40"]
x = 0.03
e = 1.1

for Titem in temp:
    file_msd = f'../results/eAB-{e}/c_{x}/P_0.13/T_{Titem}/rdf.data'

    bin, rdfAA, rdfAB, rdfBB = RDF_graph(file_msd)

    plt.plot(bin, rdfAA, label=f"T {Titem} AA")
    plt.plot(bin, rdfAB, label=f"T {Titem} AB")
    plt.plot(bin, rdfBB, label=f"T {Titem} BB")

plt.xlabel('r')
plt.ylabel('RDF')
plt.legend()
plt.title('Função de Distribuição Radial\nx = 0.03 eAB = 1.1 P = 0.13')
plt.show()
