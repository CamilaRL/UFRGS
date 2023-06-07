#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Nmax 50000000

float func(float x);

void main(void){

	// Arquivo de saida
	FILE *saida;
    saida = fopen("./I.txt", "w");
    fprintf(saida, "t I x y\n");

	// Semente do gerador de numeros aleatorios
	long t = time(NULL);
	srand(t);

	fprintf(saida, "Nmax: %d seed: %ld\n", Nmax, t);

	
	float x;
	float y;
	int n = 0;
	float I;

	for(int N = 0 ; N < Nmax ; N++){
		// Sorteio de pontos
		x = (float) rand() / (float)(RAND_MAX/1.);
		y = (float) rand() / (float)(RAND_MAX/1.);

		// Verifica se o ponto sorteado esta abaixo da curva
		if(y < func(x)){
			n++;
		}
		// Inicio de amostragem
		if(N > 1000 && N%11 == 0){
            I = (float) n/N;

            fprintf(saida, "%d %f %f %f\n", N, I, x, y);
        }
	}
}

float func(float x){
	// Funcao a ser integrada
	return pow(sin(1/x), 2);
}
