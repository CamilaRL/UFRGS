// Markov != SAW = Self Avoiding Walk (jogo da cobrinha)

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Nmax 1000000

float circulo(float r1, float r2);

void main(void){

	// Arquivo de saida
	FILE *saida;
    saida = fopen("./cr.txt", "w");
    fprintf(saida, "N nq nc x y\n");

	// Semente do gerador de numeros aleatorios
	//long t = time(NULL);
    long t = 124867999;
	srand(t);

	fprintf(saida, "Nmax: %d seed: %ld\n", Nmax, t);
    
    float x = 0.5;
    float y = 0.5;
    float xaux = x;
    float yaux = y;

	float r1;
	float theta;
	int nq = 0;
    int nc = 0;
        printf("x y xaux yaux r1 theta\n");
	for(int N = 0 ; N < Nmax ; N++){


        do{
            xaux = x;
            yaux = y;
            
            // Sorteio dp passo
		    r1 = 0.3 * (float) rand() / (float)(RAND_MAX/1.);    //distancia
		    theta = 2*M_PI * (float) rand() / (float)(RAND_MAX/1.); // angulo

            xaux += r1*cos(theta);
            yaux += r1*sin(theta);

            printf("%f %f %f %f %f %f\n", x, y, xaux, yaux, r1, theta);

        }while((xaux > 1.) || (yaux > 1.) || (xaux < 0) || (yaux < 0));

        x = xaux;
        y = yaux;
        nq++;

		// Verifica se o ponto sorteado esta dentro do circulo
		if(circulo(x, y) < 1){
			nc++;
		}
        
        fprintf(saida, "%d %d %d %f %f\n", N, nq, nc, x, y);
    }
}

float circulo(float r1, float r2){
	return pow(r1, 2) + pow(r2, 2);
}
