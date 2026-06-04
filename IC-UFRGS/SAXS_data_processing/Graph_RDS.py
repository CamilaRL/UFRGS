import matplotlib.pyplot as plt


FilePath_sample = "C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\SAXS\\Tratamento_Dados\\Comparacao\\019_semajuste\\019_4_00225.RAD"
FilePath_buffer = "C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\SAXS\\Tratamento_Dados\\Dados\\cap_03\\B_C3_4_00040.RAD"
#FilePath_ci = "C:\\Users\\camil\\Downloads\\010_4_00180.RDS"
FilePath_cam = "C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\SAXS\\Tratamento_Dados\\Comparacao\\019_semajuste\\019_4_00225.RDS"
FilePath_sa = "C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\SAXS\\Tratamento_Dados\\Comparacao\\019_comajuste\\019_4_00225.RDS"


def Extract_Data(FilePath):

    with open(FilePath, "r") as f:
        lines = []
        dataFile = f.readlines()[3:]

        for line in dataFile:
            lines.append(line.split())
            qB = []
            I = []
            inc = []

            for i in range(len(lines)):

                qB.append(float(lines[i][0]))
                I.append(float(lines[i][1]))
                inc.append(float(lines[i][2]))

    return qB, I, inc

qB_s, I_s, inc_s = Extract_Data(FilePath_sample)
qB_b, I_b, inc_b = Extract_Data(FilePath_buffer)
#qB_c, I_c, inc_c = Extract_Data(FilePath_ci)
qB_m, I_m, inc_m = Extract_Data(FilePath_cam)
qB_sa, I_sa, inc_sa = Extract_Data(FilePath_sa)

'''
fig = plt.figure(figsize=(10, 5))

plt.subplot(121)
plt.plot(qB_s, I_s, label='Sample')
#plt.plot(qB_c, I_c, label='Cilaine')
plt.plot(qB_sa, I_sa, "--", label='Sem ajuste')
#plt.plot(qB_b, I_b, label='Buffer')
plt.legend()

plt.subplot(122)
plt.plot(qB_s, I_s, label='Sample')
plt.plot(qB_m, I_m, label='Com ajuste')
#plt.plot(qB_b, I_b, label='Buffer')
plt.legend()

plt.suptitle("Concentração: 019\nTemperatura: 4°C")

plt.show()'''

#plt.plot(qB_s, I_s, label='Sample')
#plt.plot(qB_b, I_b, label='Buffer')
#plt.plot(qB_c, I_c, '--', label='Cilaine')
plt.plot(qB_m, I_m, label='Com ajuste')
plt.plot(qB_sa, I_sa, label='Sem ajuste')
plt.legend()
plt.title("Concentração: 019\nTemperatura: 4°C")
plt.show()