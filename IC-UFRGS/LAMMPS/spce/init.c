#include <stdio.h>
#include <stdlib.h>
#include <math.h>


void main(void){
	double avogadro = 6.022*pow(10, 23);
	
	// DADOS DE MOLECULAS
	int N = 300; // total de particulas
	int Nmol = (int) N/3; //numero de moleculas
	int bonds = Nmol*2;
	int angles = Nmol;
	
	double q[2] = {0.4238, -0.8476}; // carga do hidrogenio e oxigenio (respectivamente)
	double m[2] = {1.0079401, 15.999400}; // massa do hidrogenio e oxigenio (respectivamente)
	float theta = 1.910632; // angulo entre moleculas é 109.4712
	
	
	// TAMNHO DA CAIXA
	double rho = 1.05; // (g/cm^3)
	double l_box = pow(10,8) * cbrt(Nmol * (2 * m[0] + m[1])/(rho * avogadro)); // (cm) lateral para caber todas as moleculas

	int n3 = ceil(cbrt(Nmol));
	double space = l_box/(n3); //(cm)
	
	
	double rhocalc = pow(10, 24) * Nmol * (2 * m[0] + m[1]) / (avogadro * pow(l_box, 3));
	
	printf("\nDensidade Total Calculada: %f\n", rhocalc);
	printf("Densidade Total Definida: %f\n", rho);
	printf("Numero de particulas: %d\n", N);
	printf("Dimensão da caixa: %f\n", l_box);
	printf("Partículas por linha: %d\n", n3);
	printf("Distancias entre particulas: %f\n", space);
	
	
	// Arquivos para impressão
    FILE *arq_Init;
    arq_Init = fopen("init.syst", "w");
    
    fprintf(arq_Init, "#LAMMPS SPC-WATER\n");
    fprintf(arq_Init, "        \n%d atoms        \n%d bonds        \n%d angles", N, bonds, angles);
    fprintf(arq_Init, "           \n2 atom types           \n1 bond types           \n1 angle types\n");
    fprintf(arq_Init, "0.0   %.1f   xlo xhi\n0.0   %.1f   ylo yhi\n0.0   %.1f   zlo zhi\n\n", l_box, l_box, l_box);
    fprintf(arq_Init, "Masses\n\n     1  1.0079401\n     2  15.999400\n\n");
    fprintf(arq_Init, "Atoms\n\n");


	// Cria 1 molécula
	
	double d = 1.; // distancia O-H
	int a = 2; // atom 1 = hy ; atom 2 = ox
    double mol[3][4]; // [id do atomo][0:tipo de atomo | 1:x | 2:y | 3:z ]
	double rmol = d + 0.1;
	
	double x = rmol, y = rmol, z = rmol;
	
    for(int n = 0 ;  n <= 2 ; n++){

        mol[n][0] = a; //guarda o tipo de partícula

        y = (n+1)*d + 0.1;
        
        if(n == 2){
            y = rmol + d*cos(theta);
            z = rmol + d*sin(theta);
        }

        // guarda as posições
        mol[n][1] = x;
        mol[n][2] = y;
        mol[n][3] = z;
		//printf("%d %f %f %f\n", a, x, y, z);

        a = 1;
    }
	

	// Atomic Position
	
    int p = 0;
	int r = 1;
	int i = 0, j = 0, k = 0;
    int mol_counter = 1;
	
    for(int n = 1 ; n <= N ; n++){

        //x = mol[p][1] + i*(l + space);
        //y = mol[p][2] + j*(l + space);
        //z = mol[p][3] + k*(l + space);
		x = mol[p][1] + i*(space);
        y = mol[p][2] + j*(space);
        z = mol[p][3] + k*(space);

        fprintf(arq_Init, "         %3d           %d           %d   %10.4f        %10.16f        %10.16f        %10.16f     \n", n, r, (int) mol[p][0], q[((int) mol[p][0]) - 1], x, y, z);

        p++;
        if(p == 3){
            p = 0;
            r++;

            i++;
            if(i == n3){
                i = 0;
                j++;
                if(j == n3){
                    j = 0;
                    k++;
                }
            }
        }
    }

	// Bonds
    fprintf(arq_Init, "\nBonds\n\n");
    int b = 1;

    for(int a = 1 ; a <= bonds; a = a + 2){

        fprintf(arq_Init, "         %4d        1        %4d        %4d\n", a, b, b+1);
        fprintf(arq_Init, "         %4d        1        %4d        %4d\n", a+1, b, b+2);
        b = b + 3;
    }

	// Angles
    fprintf(arq_Init, "\nAngles\n\n");
    b = 1;

    for(int a = 1 ; a <= angles; a++){

        fprintf(arq_Init, "         %4d        1        %4d        %4d        %4d\n", a, b+1, b, b+2);
        b = b + 3;
    }

    fclose(arq_Init);
}

