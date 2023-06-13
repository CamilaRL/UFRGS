#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Nmax 1000000

void main(void){

	// Arquivo de saida
    FILE *saida;
    saida = fopen("./Pi-buf-huge.txt", "w");
    fprintf(saida, "t Pi r1 r2\n");

	// Semente do gerador de numeros aleatorios
    long t = time(NULL);
	srand(t);

    float r1;
    float r2;
	int n = 0;
    float pi;

    fprintf(saida, "Nmax: %d seed: %ld\n", Nmax, t);
	

    for(int N = 0 ; N < Nmax ; N++){
		// Sorteio de pontos
        r1 = (float) rand() / (float)(RAND_MAX/M_PI);
        r2 = (float) rand() / (float)(RAND_MAX);

		// Verifica se o ponto sorteado esta abaixo da curva
        if(r2 < sin(r1)){
            n++;
        }
		// Inicio de amostragem
        if(N%11 == 0){
            pi = 2.*N/n;

            fprintf(saida, "%d %f %f %f\n", N, pi, r1, r2);
        }
    }
}

