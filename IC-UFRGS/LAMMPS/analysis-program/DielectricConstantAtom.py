import numpy as np
import matplotlib.pyplot as plt

class Atom:

    def __init__(self, ID, type, x, y, z):
        self.id = ID
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.q = 0
        
        if(type == 1):
            self.q = 0.5270*1.6*(10**-19) # carga hidrogenio em C
        elif(type == 2):
            self.q = -1.0540*1.6*(10**-19) # carga oxigenio em C
        
        
    def pos_update(self, x, y, z):    
        self.x = x
        self.y = y
        self.z = z
        
    def print_atom_data(self):
        print('id: ' + self.id + 'type: ' + self.type + 'x: ' + self.x + 'y:' + self.y + 'z:' + self.z)
        
        
class H20:

    def __init__(self, idO, idH1, idH2):
        self.O = idO
        self.H1 = idH1
        self.H2 = idH2
        
    def print_mol_data(self):
        print(f'id O: {self.O} id H1: {self.H1} id H2: {self.H2}')

def ReadInitFile(filename):

    '''
        Função para extrair as informações das moléculas
    '''
    
    color = []
    x = []
    y = []
    z = []
    
    with open(filename, 'r') as f:
    
        lines = f.readlines()
        totalAtoms = int(lines[2].split(' ')[0])
        Lbox = float(lines[8].split('  ')[1])
        
        i = 19
        while(i < totalAtoms + 19):
            
            line = lines[i].split(' ')
            while('' in line): line.remove('')
              
            atom = Atom(int(line[0]), int(line[2]), float(line[4])*angs, float(line[5])*angs, float(line[6])*angs)
                
            atomList.append(atom)
            
            color.append(int(line[2]))
            x.append(float(line[4]))
            y.append(float(line[5]))
            z.append(float(line[6]))
            
            i = i + 1
            
        
    for j in range(0, len(atomList), 3):
        molecula = H20(atomList[j].id, atomList[j+1].id, atomList[j+2].id)
        molList.append(molecula)
        
    return x, y, z, color, totalAtoms, Lbox


def ReadDumpFile(filename):
    
    Mlist = []
    time = []
    Mx = []
    My = []
    Mz = []
    
    with open(filename, 'r') as f:
        
        lines = f.readlines()
        t = 0

        i=9
        counter = 0
        
        while(i < len(lines)):
        
            if(counter == 300):
                i = i + 9
                t = t + 1
                counter = 0
                
                M = TotalDipoleMoment()
                Mlist.append(M)
                Mx.append(M[0])
                My.append(M[1])
                Mz.append(M[2])
                time.append(t*10**(-6))

            line = lines[i].split(' ')
            while('' in line): line.remove('')
            #print(f'{i} {line}')
            atomList[int(line[0]) - 1].pos_update(float(line[2])*angs, float(line[3])*angs, float(line[4])*angs)

            counter = counter + 1
            i = i + 1

        
        for atom in atomList:
            x.append(atom.x)
            y.append(atom.y)
            z.append(atom.z)
            
            
        fig = plt.figure(figsize=(12,5))
        
        plt.subplot(131)
        plt.plot(time, Mx, label='Mx')
        plt.xlabel('Time (ns)')
        plt.ylabel('M')
        plt.legend()
        
        plt.subplot(132)
        plt.plot(time, My, label='My')
        plt.xlabel('Time (ns)')
        plt.ylabel('M')
        plt.legend()
        
        plt.subplot(133)
        plt.plot(time, Mz, label='Mz')
        plt.xlabel('Time (ns)')
        plt.ylabel('M')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        
    return x, y, z, Mlist
    
def TotalDipoleMoment():

    M = [0, 0, 0] # momento de dipolo total

    for a in atomList:
        pos = [a.x, a.y, a.z]
        for i in range(3):
            M[i] = M[i] + a.q*pos[i]
    
    return M

def DielectricConstantWater(Mlist, N, V, T):

    kB = 1.38*(10**(-23))
    e0 = 8.85*(10**(-12))
    k0 = 8.9875*(10**(9))
    M2 = 0
    Mmean = 0
    
    # loop sobre o momento de dipolo total de cada passo
    for M in Mlist:
        
        Mmod = (M[0]**2 + M[1]**2 + M[2]**2)**(1/2)
        
        M2 = M2 + Mmod**2
        Mmean = Mmean + Mmod
    
    Mvar = ((M2/len(Mlist)) - (Mmean/len(Mlist))**2)#/10**(-15)
    
    #e = 1 + (4*np.pi*Mvar)/(3*V*kB*T)
    e = 1 + (Mvar)/(3*e0*V*kB*T)
    
    return e


### MAIN

global atomList, molList, bondList, angs

T = 300

angs = 10**(-10) # 1 angstrom = 10^{-10} metros
atomList = []
molList = []

x, y, z, color, N, Lbox = ReadInitFile('./init.syst')

x, y, z, Mlist = ReadDumpFile(f'./implicit/3dumpT{T}.lammpstrj')

e = DielectricConstantWater(Mlist, N, (Lbox*angs)**3, T)

print(f'{T} {e}')