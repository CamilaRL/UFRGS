import numpy as np
import matplotlib.pyplot as plt
# Biblioteca de estruturas básicas para tratamento e análise de dados \
# de SAXS.
import saxspy.saxspy as saxs


def PlotAndDefineLimits(data):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=1)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', \
      color='#11bbff', markersize=1, label=r'I(q)')
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I_\mathrm{\,water} \quad (\,a.\ u.\,)$')
  
  qmax = ((100*max(data.q) + 5)//10)/10
  plt.xticks(np.linspace(0, qmax, 11))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'Scattering intensity of water (measured)\n')
  
  plt.draw()
  plt.pause(0.2)
  
  print("Set the q interval for the fitting of the water scattering intensity (constant).")
  qinf = float(input("Insert the inferior limit of q: "))
  qsup = float(input("Insert the upper limit of q: "))
  
  plt.close()
  
  return qinf, qsup


##################### Faz o gráfico do ajuste. #########################
########################################################################
def PlotFit(data, qinf, qsup, a0, s0, chi2dof, nameOutput, save):

  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=1)
  plt.semilogy(data.q, data.I, ls='', lw=0.5, marker='.', markersize=1, \
      color='#0077cc', label=u'Data')
  x = np.linspace(qinf, qsup, 100)
  y = np.ones(100)*a0
  plt.plot(x, y, ls='-', lw=1.5, marker='', markersize=0.2, \
      color='#bb0022', label=(u'Fit (constant)'))
  #plt.annotate((r'a0 =  %f \pm %f\n chi^2 = %.3e' % (a0, s0, chi2dof)), \
  #xy=[0.3,0.3])
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q \quad (\AA^{-1})$')
  plt.ylabel(r'$I \quad (a.\ u.)$')
  #plt.xlim(0, 0.4)
  #plt.ylim(0, 0.4)
  qmax = ((100*max(data.q) + 5)//10)/10
  plt.xticks(np.linspace(0, qmax, 11))
  #plt.yticks(np.arange(0.05, 0.40, 0.01))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'Fitting of water scattering intensity')
  
  plt.draw()
  plt.show()
  
  if(save):
    plt.savefig(nameOutput+".pdf")


########################################################################


# Ajusta uma constante no espalhamento da água. 
########################################################################
def FitConstant(data, qinf, qsup):
    
  x = data.q[data.q > qinf]
  init = data.Size() - len(x)
  x = x[x < qsup]
  end = init + len(x)

  y = data.I[init:end]
  s = data.sI[init:end]
  
  p, cov = np.polyfit(x, y, 0, w=1/s, cov='unscaled')
  p, chi2, rank, sing_v, rcond = np.polyfit(x, y, 0, w=1/s, full=True)
  
  a0 = p[0]
  s0 = np.sqrt(cov[0,0])
  
  return a0, s0, chi2/(len(x)-1)
