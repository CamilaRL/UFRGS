#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Nmax 1000000

float circulo(float r1, float r2);

void main(void){

	// Arquivo de saida
	FILE *saida;
    saida = fopen("./Pi-cir.txt", "w");
    fprintf(saida, "t Pi r1 r2\n");

	// Semente do gerador de numeros aleatorios
	long t = time(NULL);
	srand(t);

	fprintf(saida, "Nmax: %d seed: %ld\n", Nmax, t);

	float r1;
	float r2;
	int n = 0;
	float pi;

	for(int N = 0 ; N < Nmax ; N++){
		// Sorteio de pontos
		r1 = (float) rand() / (float)(RAND_MAX/1.);
		r2 = (float) rand() / (float)(RAND_MAX/1.);

		// Verifica se o ponto sorteado esta dentro do circulo
		if(circulo(r1, r2) < 1){
			n++;
		}
		// Inicio de amostragem
		if(N > 10000 && N%11 == 0){
            pi = 4.*n/N;

            fprintf(saida, "%d %f %f %f\n", N, pi, r1, r2);
        }
	}
}

float circulo(float r1, float r2){
	return pow(r1, 2) + pow(r2, 2);
}
