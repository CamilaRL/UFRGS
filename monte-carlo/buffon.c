#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


void main(void){

    FILE *saida;
    saida = fopen("./P.txt", "w");
    fprintf(saida, "t Pi r1 r2\n");

	srand(time(NULL));
	int n = 0;
    float pi;
	

    for(int N = 0 ; N < 1000000 ; N++){

        float r1 = (float) rand() / (float)(RAND_MAX/M_PI);
        float r2 = (float) rand() / (float)(RAND_MAX);

        if(r2 < sin(r1)){
            n++;
        }
        if(N > 100 && N%100 == 0){
            pi = 2.*N/n;

            fprintf(saida, "%d %f %f %f\n", N, pi, r1, r2);
        }
    }
}

