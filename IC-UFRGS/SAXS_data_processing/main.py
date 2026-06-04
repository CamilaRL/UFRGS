import saxspy.saxspy as saxs
import numpy as np
import os as os
import _SAXSPy.MeanMaker as mean
import _SAXSPy.qScaleFit as qscale
import _SAXSPy.CTTqCorrection as cttq
import _SAXSPy.SolventCorrection as solvent
import _SAXSPy.WaterFitScattering as waterfit
import _SAXSPy.AbsoluteScaleCorrection as absolute

print('\n\nEste programa realiza o tratamento dos dados de SAXS de amostras dissolvidas em água.\n')
print('Cada etapa é realzada por funções definidas no pacote _SAXSPy:')
print(' - MeanMaker: realiza as médias dos dados integrados;')
print(' - qScaleFit: realiza o ajuste do vetor de espalhamento (q) com AgBeh para calibração;')
print(' - CTTqCorrection: corrige o espalhamento da amostra e do solvente a partir do capilar, da transmissão e do ajuste de q;')
print(' - SolventCorrection: corrige o espalhamento da amostra pelo do solvente;')
print(' - WaterFitScattering: calcula a constante de normalização a partir do espalhamento da água;')
print(' - AbsoluteScaleCorrection: realiza o ajuste do espalhamento da amostra para escala absoluta;\n\n')

print('Instruções para o arquivo de parâmetros:')
print(' - Linhas 1 a 4: Lista com os arquivos de dados')
print('Amostra, água, capilar e AgBeh (Formato: nome.txt, diretório)')
print(' - Linha 5: parâmetros do solvente')
print('Transmissão solvente, espessura solvente, transmissão capilar')
print(' - Linha 6: parâmetros da amostra')
print('Transmissão amostra, espessura amostra, transmissão capilar')
print(' - Linha 7: Fração Volumétrica do Soluto')
print('Observação: linhas iniciadas por # ou espaços não são contabilizadas.\n')

# Cria pasta para armazenar os dados tratados
folder_name = input('Insira o nome da pasta dos resultados: ')
os.mkdir(f'./{folder_name}')

# Extrai dados de entrada a partir de arquivo de parâmeâtros
fileParameters = input("Insira o arquivo de parâmetros: ")
fileListFiles, directoryFiles, solventList, sampleList, soluteVolumetricFraction = mean.ImportParameters(fileParameters)


########################### Mean Maker #########################

os.mkdir(f'./{folder_name}/MeanMaker')

print("\nInicializando MeanMaker\n")

fileOutput = [f'./{folder_name}/MeanMaker/media_butanol.dat', f'./{folder_name}/MeanMaker/media_water.dat', f'./{folder_name}/MeanMaker/media_capillary.dat', f'./{folder_name}/MeanMaker/media_agbeh.dat']

for i in range(4):
    listFiles = mean.ImportListFiles(fileListFiles[i], directoryFiles[i])

    data = mean.SAXSMean(listFiles, fileOutput[i], printFileNames=False)

    mean.PlotMean(data, label=fileOutput[i])


########################### q-ScaleFit #########################

os.mkdir(f'./{folder_name}/q-ScaleFit')

print("\nInicializando qScaleFit\n")

fileInput = f'./{folder_name}/MeanMaker/media_agbeh.dat'

data = saxs.Saxs()
data.ImportData(fileInput)

qscale.PlotScattering(data, label=u"Standard", close=False)

# Cria um arquivo de dados com os valores de intervalos de ajuste
peakRange = qscale.InsertPeakRange()

# Ajusta os picos para calibração
peakParameters1, peakParameters2, peakParameters3 = qscale.FitPeaks(data, peakRange)
peakParameters = [peakParameters1, peakParameters2, peakParameters3]

# Define os picos mensurados.
peaksMeasured = np.array([peakParameters1[0][0], peakParameters2[0][0], peakParameters3[0][0]])

# Define os picos de referência. Picos do Behenato definidos conforme Huang, et al (1993).
d001 = 58.3803  # Angstrom
peaksReference = np.array([(2 * np.pi / d001), (4 * np.pi / d001), (6 * np.pi / d001)])

# Faz o ajuste da reta de calibração e faz o gráfico.
# Primeiro picos ajustados, depois os picos de referência.
coefficients = qscale.LinearFit(peaksMeasured, peaksReference)
qSlope, qIntercept =  coefficients[0][0], coefficients[1][0]

# Salva resultados dos ajustes.
with open(f'./{folder_name}/q-ScaleFit/ajuste_q.dat', "w") as f:
    f.write("# Results of q-scale calibration for the silver behenate standard.\n")
    f.write("# Calibration using the data file \"%s\".\n" % fileInput)
    f.write("# peak-center, peak-width, peak-amplitude, peak-base\n")

    for i in range(3):
        f.write("# Fitting results for peak %d. reduced-chi-squared: %.3f; R-squared: %.3f;\n" % (
        (i + 1), peakParameters[i][4][0], peakParameters[i][4][1]))
        f.write("%.6e +/- %.1e, %.6e +/- %.1e, %.6e +/- %.1e, %.6e +/- %.1e\n" % \
                (peakParameters[i][0][0], peakParameters[i][0][1], peakParameters[i][1][0], peakParameters[i][1][1], \
                 peakParameters[i][2][0], peakParameters[i][2][1], peakParameters[i][3][0], peakParameters[i][3][1]))

    f.write(
        "# Calibration curve. reduced-chi-squared: %.3f; R-squared: %.3f;\n" % (coefficients[2][0], coefficients[2][1]))
    f.write("# slope, intercept")
    f.write("# %.6f +/- %.6f, %.6e +/- %.1e" % (
    coefficients[0][0], coefficients[0][1], coefficients[1][0], coefficients[1][1]))


########################### CTTq-Correction #########################

os.mkdir(f'./{folder_name}/CTTq-Correction')

print("\nInicializando CTTq-Correction\n")
fileSample, fileSolvent, fileCapillary = f'./{folder_name}/MeanMaker/media_butanol.dat', f'./{folder_name}/MeanMaker/media_water.dat', f'./{folder_name}/MeanMaker/media_capillary.dat'

transmissionSample, thicknessSample, transmissionCapillarySample = sampleList[0], sampleList[1], sampleList[2]
transmissionSolvent, thicknessSolvent, transmissionCapillarySolvent = solventList[0], solventList[1], solventList[2]

correctionSample = saxs.CorrectTo_CTTq(qSlope, qIntercept, \
                                     fileSample, transmissionSample, thicknessSample, \
                                     fileCapillary, transmissionCapillarySample, save=True, \
                                     fileOutput=(f'./{folder_name}/CTTq-Correction/cttq_butanol.dat'))

cttq.PlotCorrection_CTTq(correctionSample, 'cttq_butanol', close=True, save=False)

correctionSolvent = saxs.CorrectTo_CTTq(qSlope, qIntercept, \
                                     fileSolvent, transmissionSolvent, thicknessSolvent, \
                                     fileCapillary, transmissionCapillarySolvent, save=True, \
                                     fileOutput=(f'./{folder_name}/CTTq-Correction/cttq_water.dat'))

cttq.PlotCorrection_CTTq(correctionSolvent, 'cttq_water', close=True, save=False)


########################### Solvent Correction #########################

os.mkdir(f'./{folder_name}/Solvent-Correction')

print("\nInicializando Solvent Correction\n")

# Define os arquivos a serem corrigidos.
fileSample, fileSolvent = f'./{folder_name}/CTTq-Correction/cttq_butanol.dat', f'./{folder_name}/CTTq-Correction/cttq_water.dat',

# Corrige os dados e salva em arquivo.
correction = saxs.CorrectTo_Solvent(fileSample, fileSolvent, soluteVolumetricFraction, save=True, fileOutput=(f'./{folder_name}/Solvent-Correction/solvent_corrected.dat'))

# Faz o gráfico do ajuste de calibração.
solvent.PlotCorrection_Solvent(correction, "solvent_corrected.dat", save=False, close=True)


########################### Water Fit Scattering #########################

print("\nInicializando Water Fit Scattering\n")

# Cria diretório para o Absolute Correction.
os.mkdir(f'./{folder_name}/Absolute-Correction')

# Define o arquivo da água corrigida.
fileWater = f'./{folder_name}/CTTq-Correction/cttq_water.dat'

# Importa os dados SAXS.
water = saxs.Saxs()
water.ImportData(fileWater)

# Faz o gráfico da intensidade de espalhamento e registra os limites do ajuste, em q, definidos pelo usuário.
qinf, qsup = waterfit.PlotAndDefineLimits(water)

# Corrige os dados e salva em arquivo.
a0, s0, chi2dof = waterfit.FitConstant(water, qinf, qsup)

# Espalhamento da água em cm^-1, a 293K (Orthaber; Bergmann; Glatter, 2000).
absoluteScaleFactor = a0/0.01632

# Cria um arquivo com os resultados.
with open(f'./{folder_name}/Absolute-Correction/WaterFitScattering_Results.txt', 'w+') as f:
    f.write('Water scattering intensity (constant): %.5e +/- %.2e' % (a0, s0))
    f.write('Chi2 per degree of freedom: %.3e\n' % (chi2dof))
    f.write("Normalization factor for the absolute scale: %.5e" % (absoluteScaleFactor))

# Faz o gráfico do ajuste.
nameOutput = fileWater.split('.')[0]
waterfit.PlotFit(water, qinf, qsup, a0, s0, chi2dof, nameOutput, save=False)


########################### Absolute Correction #########################

print("\nInicializando Absolute Correction\n")

fileSample = f'./{folder_name}/Solvent-Correction/solvent_corrected.dat'

# Corrige os dados e salva em arquivo.
correction = saxs.CorrectTo_AbsoluteScale(absoluteScaleFactor, fileSample, save=True, fileOutput= f'./{folder_name}/Absolute-Correction/absolute_butanol.dat')

# Faz o gráfico do ajuste de calibração.
absolute.PlotCorrection_AbsoluteScale(correction, 'absolute_butanol.dat', save=False, close=True)

print('Sucesso! Programa finalizado.')
