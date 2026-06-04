#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void main(){

    //Variáveis

    int N = 1000; // total de particulas
    float xB = 0.030; // concentração de soluto (NB/N)
    int NB = round(xB*N); // numero de particulas soluto
    int NA = N - NB; // numero de particulas solvente
    int a = 1;

    double x = 0.0, y= 0.0, z = 0.0; // coordenadas
    //double rho = 0.0875;
    //double l = cbrt(N/rho);
    double l = 50.0;
    double rho = N/(l*l*l);
    double rho_l = cbrt(rho);
    int n3 = floor(cbrt(N));
    double espaco = 1/rho_l - 0.5;
    int i = 0, j = 0, k = 0;
    int countx = 0;
    int county = 0;


    // Arquivos para impressão
    FILE *arq_Init;
    arq_Init = fopen("init.syst", "w");

    fprintf(arq_Init, "#LAMMPS NPT\n\n%d atoms\n\n2 atom types\n\n", N);

    fprintf(arq_Init, "0.0   %.1f   xlo xhi\n0.0   %.1f   ylo yhi\n0.0   %.1f   zlo zhi\n\n", l, l, l);

    fprintf(arq_Init, "Masses\n\n1  1.0\n2  1.0\n\n");

    fprintf(arq_Init, "Atoms\n\n");

    printf("Densidade Total: %f\n", rho);
    printf("Densidade Lateral: %f\n", rho_l);
    printf("Numero de particulas: sum = %d\n", N);
    printf("Soluto: %d\n", NB);
    printf("Solvente: %d\n", NA);
    printf("Tamanho da caixa: %f\n", l);
    printf("Distancias entre particulas: %f\n", espaco);

    for(int n = 1 ; n <= N ; n++){


        x = i*espaco + 0.5;
        y = j*espaco + 0.5;
        z = k*espaco + 0.5;

        if(n > NA){
            a = 2;
        }
        // number   atom-type   x   y   z
        fprintf(arq_Init, "         %3d           %d   %10.16f        %10.16f        %10.16f     \n", n, a, x, y, z);

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