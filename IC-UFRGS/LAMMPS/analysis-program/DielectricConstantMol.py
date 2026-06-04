import numpy as np
import matplotlib.pyplot as plt

class Atom:

    def __init__(self, ID, type, x, y, z):
        self.id = ID
        self.type = type
        self.x = x*angs
        self.y = y*angs
        self.z = z*angs
        self.q = 0
        
        if(type == 1):
            self.q = 0.5270*1.6*(10**-19) # carga hidrogenio em C
        elif(type == 2):
            self.q = -1.0540*1.6*(10**-19) # carga oxigenio em C
        
        
    def pos_update(self, x, y, z):    
        self.x = x*angs
        self.y = y*angs
        self.z = z*angs
        
    def print_atom_data(self):
        print('id: ' + self.id + 'type: ' + self.type + 'x: ' + self.x + 'y:' + self.y + 'z:' + self.z)
        
        
class H20:

    def __init__(self, idO, idH1, idH2):
        self.O = idO
        self.H1 = idH1
        self.H2 = idH2
        
        # calculo momento de dipolo da molecula
        mux = (atomList[idO-1].q * atomList[idO-1].x) + (atomList[idH1-1].q * atomList[idH1-1].x) + (atomList[idH2-1].q * atomList[idH2-1].x)
        muy = (atomList[idO-1].q * atomList[idO-1].y) + (atomList[idH1-1].q * atomList[idH1-1].y) + (atomList[idH2-1].q * atomList[idH2-1].y)
        muz = (atomList[idO-1].q * atomList[idO-1].z) + (atomList[idH1-1].q * atomList[idH1-1].z) + (atomList[idH2-1].q * atomList[idH2-1].z)
        
        self.mu = [mux, muy, muz]
        
    def DipoleMoment_update(self):
    
        mux = (atomList[self.O-1].q * atomList[self.O-1].x) + (atomList[self.H1-1].q * atomList[self.H1-1].x) + (atomList[self.H2-1].q * atomList[self.H2-1].x)
        muy = (atomList[self.O-1].q * atomList[self.O-1].y) + (atomList[self.H1-1].q * atomList[self.H1-1].y) + (atomList[self.H2-1].q * atomList[self.H2-1].y)
        muz = (atomList[self.O-1].q * atomList[self.O-1].z) + (atomList[self.H1-1].q * atomList[self.H1-1].z) + (atomList[self.H2-1].q * atomList[self.H2-1].z)
        
        self.mu = [mux, muy, muz]
        
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
              
            atom = Atom(int(line[0]), int(line[2]), float(line[4]), float(line[5]), float(line[6]))
                
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
    x = []
    y = []
    z = []
    
    with open(filename, 'r') as f:
        
        lines = f.readlines()
        
        i = 433536
        counter = 0

        while(i < len(lines)):
   
            if(counter == 300):
                for m in molList:
                    m.DipoleMoment_update()

                i = i + 9
                counter = 0
                M = TotalDipoleMoment()
                Mlist.append(M)
                

            line = lines[i].split(' ')
            while('' in line): line.remove('')
            
            atomList[int(line[0]) - 1].pos_update(float(line[2]), float(line[3]), float(line[4]))

            counter = counter + 1
            i = i + 1

        
        for atom in atomList:
            x.append(atom.x)
            y.append(atom.y)
            z.append(atom.z)
        
    return x, y, z, Mlist
    
def TotalDipoleMoment():

    M = [0, 0, 0] # momento de dipolo total

    for m in molList:
        for i in range(3):
            M[i] = M[i] + m.mu[i]
    
    return M

def DielectricConstantWater(Mlist, N, V, T):

    kB = 1.38*(10**(-23))
    e0 = 8.85*(10**(-12))
    k0 = 8.9875*(10**(9))
    M2 = 0
    Mmean = 0
    
    for M in Mlist:
    
        Mmod = (M[0]**2 + M[1]**2 + M[2]**2)**(1/2)
        
        M2 = M2 + Mmod**2
        Mmean = Mmean + Mmod
    
    Mvar = ((M2/len(Mlist)) - (Mmean/len(Mlist))**2)#/10**(-15)
    
    e = 1 + (Mvar)/(3*e0*V*kB*T)
    
    return e
    
def Plot_Bonds2D(e, T):
    
    plt.plot(e, T)


global atomList, molList, bondList, angs

angs = 10**(-10) # 1 angstrom = 10^{-10} metros
T = 320

atomList = []
molList = []

x, y, z, color, N, Lbox = ReadInitFile('./init.syst')

x, y, z, Mlist = ReadDumpFile('./implicit/2dumpT320.lammpstrj')

e = DielectricConstantWater(Mlist, N, (Lbox*angs)**3, 320)

print(f'{T} {e}')