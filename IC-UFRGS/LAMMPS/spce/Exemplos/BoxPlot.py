import matplotlib.pyplot as plt
import numpy as np

def Reading_Pos(file):
    x = []
    y = []
    z = []
    
    with open(file, 'r') as f:
        box_lim = []
        color = []
        lines = f.readlines()[9:]

        # Leitura dos limites da caixa
        for i in range(3):
            line = lines[i].split(' ')
            print(line)
            box_lim.append(float(line[1]) + 1.0)

        # Leitura das posicoes das particulas
        for line in lines[20:311]:
            line = line.split(' ')
            while('' in line): line.remove('')

            color.append(int(line[2]))
            x.append(float(line[4]))
            y.append(float(line[5]))
            z.append(float(line[6]))
    
    return x, y, z, color, box_lim

def Plot_Full_Box(filename):

    #x_ro, y_ro, z_ro, lim = Reading_Pos(file_ro)
    x_ca, y_ca, z_ca, c, lim = Reading_Pos(filename)

    x_box = np.full((1), lim[0])
    y_box = np.full((1), lim[1])
    z_box = np.full((1), lim[2])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #print(lim)

    colormap = np.array(['black', 'blue', 'orange'])
    categorias = np.array(c)

    #ax.scatter(x_ro, y_ro, z_ro, marker='.', color='red')
    ax.scatter(x_ca, y_ca, z_ca, marker='.', c=colormap[categorias])
    #ax.plot_wireframe(x_box, y_box, z_box, color='black')

    # Plot 3D
    ax.set_xlabel('X')
    #ax.set_xlim([-1, float(lim[0])]) # determina os limites do respectivo eixo
    ax.set_ylabel('Y')
    #ax.set_ylim([-1, float(lim[1])])
    ax.set_zlabel('Z')
    #ax.set_zlim([-1, float(lim[2])])
    plt.show()

def Plot_Molecule(filename):

    x_ca, y_ca, z_ca, c, lim = Reading_Pos(filename)

    fig = plt.figure()
    #ax = fig.add_subplot(projection='3d')

    colormap = np.array(['black', 'blue', 'orange'])
    categorias = np.array(c)

    #ax.scatter(x_ca[:3], y_ca[:3], z_ca[:3], marker='.', c=colormap[categorias[:3]])
    plt.scatter(y_ca[:3], z_ca[:3], marker='.', c=colormap[categorias[:3]])

    # Plot 3D
    plt.xlabel('Y')
    plt.ylabel('Z')
    plt.grid(True)
    plt.show()


file = "./Marco/spc.data"
Plot_Full_Box(file)
Plot_Molecule(file)