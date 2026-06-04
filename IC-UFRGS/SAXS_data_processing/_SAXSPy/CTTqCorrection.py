import numpy as np
import matplotlib.pyplot as plt
# Biblioteca para tratamento e análise de dados de medidas de SAXS.
import saxspy.saxspy as saxs

########################################################################
###################### Faz o gráfico da correção. ######################
########################################################################

def PlotCorrection_CTTq(
    data,
    label,
    close=True, 
    save=False, 
    fileOutput="CTTq_output.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q_\mathrm{\,calibrated} \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I_\mathrm{\,pre-corrected} \quad (\,a.\ u.\,)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'SAXS scattering intensity corrected\n for capilar, transmission and thickness. q-scale calibrated.')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
  
    plt.show()