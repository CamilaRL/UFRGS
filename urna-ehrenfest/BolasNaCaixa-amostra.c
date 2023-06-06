#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 100

void main(void){

    FILE *saida;
    saida = fopen("./saida2.txt", "w");
    fprintf(saida, "t A\n");

    FILE *hist;
    hist = fopen("./hist2.txt", "w");
    fprintf(hist, "t hist\n");

	// A=0 B=1
	int bolas[N] = {0};
    int contagem[N+1] = {0}; // cada posição no array corresponde a uma configuração
    int A = N;
    int i = 0;
    int samples = 0;

    long t = time(NULL);
    srand(t);
	
    // tempo de equilíbrio = 200 passos
	for(int t = 0; t < 10000000 ; t++){
		i = rand()%N;
        
        if(t>200 && t%11 == 0){
            samples++; // numero de amostras para normalizar
            contagem[A]++; // soma 1 na posição da configuração A
        }


        if(bolas[i]==0){
            // vai para B
            bolas[i] = 1;
            A--;
        }
        else if(bolas[i]==1){
            // vai para A
            bolas[i] = 0;
            A++;
        }

        fprintf(saida, "%i %i\n", t, A);
	}

    fprintf(saida, "samples: %d tempo: %d N: %d seed: %ld\n", samples, 10000000, N, t);
    fprintf(hist, "samples: %d tempo: %d N: %d seed: %ld\n", samples, 10000000, N, t);

    // salva o histograma
    for(int n = 0 ;  n <= N ; n++){
        fprintf(hist, "%i %f\n", n, (float)contagem[n]/samples);
    }
}