import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco


############################################################################################
################ Plota o logaritmo da intensidade vs vetor de espalhamento. ################
############################################################################################

def PlotScattering(
    data,
    label,
    close=True, 
    save=False, 
    fileOutput="q-ScaleFit_output1.pdf"):
	
  plt.errorbar(data.q, data.I, yerr=data.sI, linestyle='', color='k', \
      marker='', markersize=1, capsize=2)
  plt.semilogy(data.q, data.I, linestyle='', marker='x', markersize=2, \
      label=(label))
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q \quad (\,\AA^{-1})\,$')
  plt.ylabel(r'$I \quad (\,a.\ u.\,)$')
  
  #plt.xticks(np.arange(0, 0.40, 0.05))
  #plt.yticks(np.arange(0, 0.40, 0.05))
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(u'SAXS scattering intensity')
  plt.draw()
  plt.pause(0.1)
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
  
    plt.show()


############################################################################################
################# Constrói o arquivo com os intervalos para ajuste. ########################
############################################################################################

def InsertPeakRange():
  
  peakOrdering = ["1st", "2nd", "3rd"]
  
  print("Collecting ranges of the peaks to fit...\n")
  fitInterval = []
  for j in range(3):  
    interval = input("Enter the q interval for the %s peak (format 'least:largest'): " % peakOrdering[j])
    fitInterval.append(interval.split(':'))
    for i in range(2):
      fitInterval[j][i] = float(fitInterval[j][i])
  
  print("\n")
  
  return fitInterval


############################################################################################
############ Define uma função lorentziana com deslocamento vertical. ######################
############################################################################################

def lorentzian(x, q0, w, A, Imin):
  
  return (A/(1+((x-q0)/w)**2) + Imin)


############################################################################################
################ Faz o ajuste de uma lorentziana nos picos. ################################
############################################################################################

def FitLorentz(qran, data, peakNumber):
  
  # Constrói os vetores do intervalo de ajuste. ###########################################
  x = data.q[data.q > qran[0]]
  init = data.Size() - len(x)
  x = x[x < qran[1]]
  end = init + len(x)
 
  y = data.I[init:end]
  s = data.sI[init:end]
  
  # Chute inicial dos parâmetros. #########################################################
  q0 = 0.5*(max(x) + min(x))
  w = (max(x) - min(x))/10
  A = (max(y) - min(y))
  Imin = min(y)
  parameters = [q0, w, A, Imin]
  
  # Ajusta a curva. #######################################################################
  parameters, cov = sco.curve_fit(lorentzian, x, y, p0=parameters, sigma=s, method='lm')
  uncerties = np.sqrt(np.diag(cov))
  ya = lorentzian(x, parameters[0], parameters[1], parameters[2], parameters[3])
  
  ym = np.sum(y/(s**2))/np.sum(1/(s**2))
  tss = np.sum(((y - ym)/s)**2)
  residuals = np.sum(((y - ya)/s)**2)
  chi2dof = residuals/(len(y) - 4)
  R2 = 1 - residuals/tss
  
  # Cria lista de parâmetros e incertezas para o ajuste. #####################################
  fitResults = []
  for j in range(4):
    fitResults.append([parameters[j], uncerties[j]])
  fitResults.append([chi2dof, R2])

  # Insere a curva ajustada no gráfico.
  PlotPeakFit(x, ya, label=("Fitting Peak %d" % peakNumber), close=(peakNumber//3))
  
  return fitResults


##############################################################################################
################ Plota os ajustes junto com os dados de espalhamento. ########################
##############################################################################################

def PlotPeakFit(
    xpeak, 
    ypeak,
    label,
    close=True,
    save=False):
  
  plt.plot(xpeak, ypeak, linestyle='-', label=label, linewidth=2)
  
  plt.legend(loc='upper right')
  plt.grid(True)
  plt.xlabel(r'$q \quad (\AA^{-1})$')
  plt.ylabel(r"$I \quad (a.\ u.\,)$")
  plt.tick_params(axis='x', labelsize=6)
  plt.tick_params(axis='y', labelsize=8)
  plt.title(r'Peak fitting')
  
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig('ajuste_q.dat')
    plt.show()


  
############################################################################################
######### Faz o ajuste dos picos para calibração e salva o resultado em um arquivo. ########
############################################################################################

def FitPeaks(data, peakRange):

  # Faz o gráfico do espalhamento - serve de base para os ajustes.
  plt.close() # Fecha o gráfico anterior (caso não tenha sido fechado).
  PlotScattering(data, label=u"Standard", close=False)
  
  # Faz os ajustes. ########################################################################
  
  # Ajuste para o primeiro pico.
  peak1Parameters = FitLorentz(peakRange[0], data, 1)
  
  # Ajuste para o segundo pico.
  peak2Parameters = FitLorentz(peakRange[1], data, 2)
  
  # Ajuste para o terceiro pico.
  peak3Parameters = FitLorentz(peakRange[2], data, 3)
  
  # Salva os parâmetros do ajuste. ##########################################################

  #arq2 = open(output, 'w')

  #arq2.write("# Parâmetros do ajuste dos picos\n")
  #arq2.write("# Pico 1\t Pico 2\t Pico 3\n")

  #arq2.write("# x0\n%.4e\t %.4e\t %.4e\n" % (param1[0][0], param2[0][0], param3[0][0]))
  #arq2.write("# var(x0)\n%.3e\t %.3e\t %.3e\n" % (param1[0][1], param2[0][1], param3[0][1]))
  #arq2.write("# y\n%.4e\t %.4e\t %.4e\n" % (param1[1][0], param2[1][0], param3[1][0]))
  #arq2.write("# var(y)\n%.3e\t %.3e\t %.3e\n" % (param1[1][1], param2[1][1], param3[1][1]))
  #arq2.write("# I\n%.4e\t %.4e\t %.4e\n" % (param1[2][0], param2[2][0], param3[2][0]))
  #arq2.write("# var(I)\n%.3e\t %.3e\t %.3e\n" % (param1[2][1], param2[2][1], param3[2][1]))
  #arq2.write("# Imin\n%.4e\t %.4e\t %.4e\n" % (param1[3][0], param2[3][0], param3[3][0]))
  #arq2.write("# var(Imin)\n%.3e\t %.3e\t %.3e\n" % (param1[3][1], param2[3][1], param3[3][1]))
  
  #arq2.close()
  
  return peak1Parameters, peak2Parameters, peak3Parameters


###########################################################################################
########################### Faz o gráfico do ajuste linear. ###############################
###########################################################################################

def PlotLinearFit(x, y, coeff, close=True, save=False, fileOutput='Peak_Calib.pdf'):
  
  xa = np.linspace(0, 0.40, 100)
  ya = np.polyval(coeff, xa)
  
  for i in range(3):
    plt.plot(x[i], y[i], linestyle='', marker='x', markersize=8, markeredgewidth=2, label=(r"Peak %d: %.5f $\AA^{-1}$" % ((i+1), y[i])))
  
  plt.plot(xa, ya, linestyle='--', lw=1, label=u'Calibration curve')
  plt.legend(loc='upper left')
  plt.grid(True)
  plt.xlabel(r'$q_{\,measured} \quad (\AA^{-1})$')
  plt.ylabel(r'$q_{\,reference} \quad (\AA^{-1})$')
  
  plt.xticks(np.linspace(0, 0.40, 9))
  plt.yticks(np.linspace(0, 0.40, 9))
  
  plt.tick_params(axis='x', labelsize=8)
  plt.tick_params(axis='y', labelsize=8)
  
  plt.title(u'Calibration curve - silver behenate standard')
  plt.draw()
  
  if(close):
    if(save):
      plt.savefig(fileOutput)
    plt.show()

  

##########################################################################################
############# Faz o ajuste linear para calibrar os picos e salva em arquivo. #############
##########################################################################################

def LinearFit(x, y):
  
  coeff, cov = np.polyfit(x, y, 1, cov=True)
  
  ya = np.polyval(coeff, x)
  ym = np.sum(y)/3
  tss = np.sum(((y - ym))**2)
  residuals = np.sum((ya - y)**2)
  chi2dof = residuals/(3 - 2)
  R2 = 1 - residuals/tss

  coefficients = []
  coefficients.append([coeff[0], np.sqrt(cov[0,0])])
  coefficients.append([coeff[1], np.sqrt(cov[1,1])])
  coefficients.append([chi2dof, R2])
  
  # Faz o gráfico do ajuste de calibração.
  PlotLinearFit(x, y, coeff)

  return coefficients