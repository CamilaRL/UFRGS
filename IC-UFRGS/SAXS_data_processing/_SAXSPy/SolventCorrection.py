import numpy as np
import matplotlib.pyplot as plt
# Biblioteca de estruturas básicas para tratamento e análise de dados \
# de SAXS.
import saxspy.saxspy as saxs


########################################################################
#################### Faz o gráfico do ajuste linear. ###################
########################################################################

def PlotCorrection_Solvent(
    data,
    label, 
    close=True, 
    save=False, 
    fileOutput="Solvent_output.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q_\mathrm{\,calibrated} \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I_\mathrm{\,solute} \quad (\,a.\ u.\,)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'SAXS scattering intensity corrected\n for the solvent scattering')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
    
    plt.show()