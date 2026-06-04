{insert:parameter} = place to substitute for the value of your hopping paramter

# Steps to run all programs:

### creating matrices for your system:

- inside of the folder '/Dados_Hop' create a folder named '/hopping-{insert:parameter}'

- inside of '/hopping-{insert:parameter}', create the following folders:
	- '/chiTempOutput'
	- '/operador_ciclo'
	- '/w_state'

- inside of matrix2DBaseH.py adjust
	hop = 'insert:parameter'

> run >> python matrix2DBaseH.py

- move 4_hamiltonian.txt to '/resultados'

> run >> diagonazacao.exe

- move 4_autocoisas.txt to '/hopping-{insert:parameter}'

