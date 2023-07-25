// Markov != SAW = Self Avoiding Walk (jogo da cobrinha)

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Nmax 100000
#define smax 1000

float circulo(float r1, float r2);

void main(void){

    // Arquivo de saida de cada amostra
    FILE *saida;
    saida = fopen("./sampsr.txt", "w");
    fprintf(saida, "#N nq nc x y\n");

    // Arquivo de saida do ultimo resultado de cada amostra
    FILE *amostra;
    amostra = fopen("./lastsr.txt", "w");
    fprintf(amostra, "#Sample Snq Snc Sx Sy\n");
    fprintf(amostra, "#Nmax: %d Total de amostras: %d\n", Nmax, smax);

	// Variaveis 1 simulacao
    float x = 0.5;
    float y = 0.5;
    float xaux = x;
    float yaux = y;

    float r = 0.3;
    float theta;
    int nq = 0;
    int nc = 0;
    
	long seed = 123450;

    printf("x y xaux yaux r1 theta\n");


	for(int samp = 0 ; samp < smax ; samp++){

        printf("Amostra %d", samp);

		// Semente do gerador de numeros aleatorios
    	seed = seed + 3;
		srand(seed);

        fprintf(saida, "\n#Sample: %d Seed: %ld Nmax: %d\n", samp, seed, Nmax);
	
	    for(int N = 0 ; N < Nmax ; N++){

    	    xaux = x;
    	    yaux = y;

    	    // Sorteio do passo
			theta = 2*M_PI * (float) rand() / (float)(RAND_MAX/1.); // angulo
	
    	    xaux += r*cos(theta);
    	    yaux += r*sin(theta);

    	    printf("%d %f %f %f %f %f %f\n", N, x, y, xaux, yaux, r, theta);

    	    if((xaux < 1.) && (yaux < 1.) && (xaux > 0) && (yaux > 0)){
			    x = xaux;
			    y = yaux;
		    }
	
    	    nq++;
	
			// Verifica se o ponto sorteado esta dentro do circulo
			if(circulo(x, y) < 1){
				nc++;
			}
    	    
    	    fprintf(saida, "%d %d %d %f %f\n", N, nq, nc, x, y);
    	}
		
		fprintf(amostra, "%d %d %d %f %f\n", samp, nq, nc, x, y);
	}

    fclose(amostra);
    fclose(saida);
}

float circulo(float r1, float r2){
	return pow(r1, 2) + pow(r2, 2);
}
