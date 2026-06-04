import numpy as np
import matplotlib.pyplot as plt


def Separacao_Frequencia(hop, hopList_sep, porcentagem, porcentagem_media_sep, wList):

    ## separação por frequencia
    cores = ['red', 'orange', 'purple', 'blue', 'black']
    subtitles = [r'$\omega$ ~ 0', r'$\omega$ ~ 1', r'$\omega$ ~ 2', r'$\omega$ ~ 3', r'$\omega$ > 4']

    wList_sep = [[] for i in range(5)]
    porcentagem_sep = [[] for i in range(5)]

    for k in range(len(wList)):

        if wList[k] > 0 and wList[k] < 0.5:
            
            porcentagem_sep[0].append(porcentagem[k])
            
        if wList[k] > 0.5 and wList[k] < 1.5:
            
            porcentagem_sep[1].append(porcentagem[k])
        
        if wList[k] > 1.5 and wList[k] < 2.5:
            
            porcentagem_sep[2].append(porcentagem[k])
            
        if wList[k] > 2.5 and wList[k] < 3.5:
            
            porcentagem_sep[3].append(porcentagem[k])
            
        if wList[k] > 3.5:
            
            porcentagem_sep[4].append(porcentagem[k])
    
    for i in range(5):
        
        if len(porcentagem_sep[i]) > 0:
            media_em_frequencia = sum(porcentagem_sep[i])/len(porcentagem_sep[i])
            porcentagem_media_sep[i].append(media_em_frequencia)
            hopList_sep[i].append(hop)
    
    return hopList_sep, porcentagem_media_sep, subtitles, cores


# MAIN #

hopList = [0.0001, 0.001, 0.01, 0.05, 0.1]

hopList_sep = [[] for i in range(5)]
porcentagem_media_sep = [[] for i in range(5)]

for hop in hopList:
    
    wList, superposicao_zeros, superposicao_um, total = np.loadtxt(f'./superposicao_{hop}.txt', unpack=True)

    porcentagem = []
    for i in range(len(total)):
        porcentagem.append(superposicao_um[i]/(total[i] - superposicao_zeros[i]))

    hopList_sep, porcentagem_media_sep, subtitles, cores = Separacao_Frequencia(hop, hopList_sep, porcentagem, porcentagem_media_sep, wList)


for k in range(5):

    plt.scatter(hopList_sep[k], porcentagem_media_sep[k], s=10)
    plt.plot(hopList_sep[k], porcentagem_media_sep[k], label=subtitles[k])
    
plt.ylabel('Percentage (%)')
plt.xlabel('Hopping Parameter')    
plt.suptitle(f'Mean Superposition of Ciclic Tunneling and Possible State Transitions')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10)
plt.tight_layout()
plt.show()