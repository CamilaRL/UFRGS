import numpy as np
import math
import matplotlib.pyplot as plt

class Atom:

    def __init__(self, ID, type, x, y, z):
        self.id = ID
        self.type = type
        self.x = x*lbox
        self.y = y*lbox
        self.z = z*lbox
        
    def pos_update(self, x, y, z):    
        self.x = x*lbox
        self.y = y*lbox
        self.z = z*lbox
        
    def print_atom_data(self):
        print('id: ' + self.id + 'type: ' + self.type + 'x: ' + self.x + 'y:' + self.y + 'z:' + self.z)
        
        
class H20:

    def __init__(self, idO, idH1, idH2):
        self.O = idO
        self.H1 = idH1
        self.H2 = idH2
        self.bonds = np.zeros(Nmol)
        self.viz = []
        
        self.xcm = ((atomList[idO-1].x)*15.999 + (atomList[idH1-1].x)*1.008 + (atomList[idH2-1].x)*1.008)/(2*1.008 + 15.999)
        self.ycm = ((atomList[idO-1].y)*15.999 + (atomList[idH1-1].y)*1.008 + (atomList[idH2-1].y)*1.008)/(2*1.008 + 15.999)
        self.zcm = ((atomList[idO-1].z)*15.999 + (atomList[idH1-1].z)*1.008 + (atomList[idH2-1].z)*1.008)/(2*1.008 + 15.999)
    
    def mol_update(self):
        self.xcm = ((atomList[self.O-1].x)*15.999 + (atomList[self.H1-1].x)*1.008 + (atomList[self.H2-1].x)*1.008)/(2*1.008 + 15.999)
        self.ycm = ((atomList[self.O-1].y)*15.999 + (atomList[self.H1-1].y)*1.008 + (atomList[self.H2-1].y)*1.008)/(2*1.008 + 15.999)
        self.zcm = ((atomList[self.O-1].z)*15.999 + (atomList[self.H1-1].z)*1.008 + (atomList[self.H2-1].z)*1.008)/(2*1.008 + 15.999)
    
    def print_mol_data(self):
        print(f'id O: {self.O} id H1: {self.H1} id H2: {self.H2}')


def ReadInitFile(filename):

    '''
        Função para extrair as informações das moléculas
    '''
    xMol = []
    yMol = []
    zMol = []
    
    with open(filename, 'r') as f:
    
        lines = f.readlines()
        totalAtoms = int(lines[2].split(' ')[0])
        
        i = 19
        while(i < totalAtoms + 19):
            
            line = lines[i].split(' ')
            while('' in line): line.remove('')
              
            atom = Atom(int(line[0]), int(line[2]), float(line[4]), float(line[5]), float(line[6]))
                
            atomList.append(atom)
            
            i = i + 1
            
        
    for j in range(0, len(atomList), 3):
        molecula = H20(atomList[j].id, atomList[j+1].id, atomList[j+2].id)
        molList.append(molecula)
        
        xMol.append(molecula.xcm)
        yMol.append(molecula.ycm)
        zMol.append(molecula.zcm)
        
    return xMol, yMol, zMol


def ReadDumpFile(filename):
    
    xMol = []
    yMol = []
    zMol = []
    
    with open(filename, 'r') as f:
        
        lines = f.readlines()
        
        i = 247209
        counter = 0

        while(i < len(lines)):
            
            line = lines[i].split(' ')
            while('' in line): line.remove('')
            
            atomList[int(line[0]) - 1].pos_update(float(line[2]), float(line[3]), float(line[4]))
            
            counter = counter + 1
            i = i + 1
            
            if(counter == 300):
                #i = i + 9
                break
        
        for molecula in molList:
            molecula.mol_update()
            
            xMol.append(molecula.xcm)
            yMol.append(molecula.ycm)
            zMol.append(molecula.zcm)
        
    return xMol, yMol, zMol

    
def BoundaryCondition(df):

    bc = lbox/2
    if(df > bc):
        df = df - math.floor(df/(lbox/2))*lbox
    

    '''if(df > bc):
        df = df - bc'''
        
    return df

    
def Bond_Condition():

    countBond = 0

    for i in range(len(molList)):
        for j in range(i+1, len(molList)):
        
            # posicao na lista = id - 1
            O1 = molList[i].O - 1
            H = [molList[i].H1 - 1, molList[i].H2 - 1]
            O2 = molList[j].O - 1
            
            
            #distancia entre os oxigênios
            
            dx = atomList[O1].x - atomList[O2].x
            dx = BoundaryCondition(dx)
            dy = atomList[O1].y - atomList[O2].y
            dy = BoundaryCondition(dy)
            dz = atomList[O1].z - atomList[O2].z
            dz = BoundaryCondition(dz)
            
            R = (dx**2 + dy**2 + dz**2)**(1/2)
            
            if((R <= 3.5)):
                #calcula ângulo:
                
                for k in range(2):
                    # distancia OH molécula 1
                    d = ((atomList[O1].x - atomList[H[k]].x)**2 + (atomList[O1].y - atomList[H[k]].y)**2 + (atomList[O1].z - atomList[H[k]].z)**2)**(1/2)
                    
                    # distancia H da molécula 1 até o oxigênio da molécula 2
                    
                    dx = atomList[O2].x - atomList[H[k]].x
                    dx = BoundaryCondition(dx)
                    dy = atomList[O2].y - atomList[H[k]].y
                    dy = BoundaryCondition(dy)
                    dz = atomList[O2].z - atomList[H[k]].z
                    dz = BoundaryCondition(dz)
                    
                    r = (dx**2 + dy**2 + dz**2)**(1/2)
                   
                    cosbeta = (R**2 + d**2 - r**2)/(2*R*d)

                    if(cosbeta <= ((3**(1/2))/2)): # cos(30) = (3**(1/2))/2
                        countBond = countBond + 1
                        
                        # atualiza lista de ligações
                        molList[i].bonds[j] = 1
                        molList[j].bonds[i] = 1
                        
                        bondList.append([[molList[i].xcm, molList[j].xcm], [molList[i].ycm, molList[j].ycm], [molList[i].zcm, molList[j].zcm]])
    print(countBond)

    
def Plot_Bonds2D(xm, ym, zm):
    
    fig = plt.figure(figsize=(12,5))
    
    plt.subplot(131)
    for i in range(len(bondList)):
        plt.plot(bondList[i][0], bondList[i][1], color='black', linewidth=0.1)
    plt.scatter(xm, ym, color='blue')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('xy')
    
    plt.subplot(132)
    for i in range(len(bondList)):
        plt.plot(bondList[i][0], bondList[i][2], color='black', linewidth=0.1)
    plt.scatter(xm, zm, color='blue')
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title('xz')
    
    plt.subplot(133)
    for i in range(len(bondList)):
        plt.plot(bondList[i][1], bondList[i][2], color='black', linewidth=0.1)
    plt.scatter(ym, zm, color='blue')
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title('yz')
    
    plt.tight_layout()
    plt.show()

def plotBond(xm, ym, zm):
    i = 2
    plt.scatter(xm, ym)
    plt.plot(bondList[i][0], bondList[i][1], color='black')
    plt.show()
    
    r = (np.diff(bondList[i][0])**2 + np.diff(bondList[i][1])**2)**(1/2)
    
    print(r)

def viz():

    rc = 10
    
    for i in range(len(molList)):
        for j in range(i+1, len(molList)):
            
            dx = abs(molList[i].xcm - molList[j].xcm)
            dy = abs(molList[i].ycm - molList[j].ycm)
            dz = abs(molList[i].zcm - molList[j].zcm)
            
            if((dx < rc) and (dy < rc) and (dz < rc)):
            
                rij = (dx**2 + dy**2 + dz**2)**(1/2)
                
                if (rij <= rc):
                    molList[i].viz.append(j)
                    molList[j].viz.append(i)
    
def ClusterCoeffi(i):
    
    sum_ki = 0
    Ei = 0
    ki = len(molList[i].viz)
    
    for j in range(Nmol):
        
        if(molList[i].bonds[j] == 1):
        
            for k in molList[i].viz:
                sum_ki = sum_ki + molList[j].bonds[k]
                
            Ei = Ei + sum_ki
            sum_ki = 0
            
            
    Ci = (2*Ei)/(ki*(ki-1))
    
    return Ci
    
def ClusterCoeffRand():

    k = 0
    klist = []
    
    for m in molList:
    
        kisum = sum(m.bonds) # grau do nodo
        klist.append(kisum)
        
        k = k + kisum # soma do grau de cada nodo (molecula)

    k = k/Nmol

    Crand = k/Nmol
    
    return Crand, k, klist
    
    
#################### MAIN ####################

global atomList, molList, bondList, lbox, Nmol

atomList = []
molList = []
bondList = []
lbox = 14.2
Nmol = 100

xMol, yMol, zMol = ReadInitFile('./init.syst')

Bond_Condition()
#Plot_Bonds2D(xMol, yMol, zMol)
bondList = []

xMol, yMol, zMol = ReadDumpFile('./implicit/0dumpT650.lammpstrj')

Bond_Condition()

Plot_Bonds2D(xMol, yMol, zMol)

viz()
for i in range(len(molList)):

    s = sum(molList[i].bonds)
    if (s == 0):
        print(i)
        print(molList[i].bonds)

Crand, kavg, klist = ClusterCoeffRand()

C = 0
for i in range(len(molList)):
    Ci = ClusterCoeffi(i)
    C = C + Ci
C = C/Nmol

print(f'C: {C} Crand: {Crand} Ci/Crand: {C/Crand} <k>: {kavg}')

plt.hist(klist, density=True)
plt.ylabel('p(k)')
plt.xlabel('k')
plt.show()