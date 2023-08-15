#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 10000

int x = 0, y = 0; // [x, y]

void walker(FILE *walk);

void main(void){

	long seed = 1234567;

    FILE *walk;
    walk = fopen("./w.txt", "w");
	
	// Amotragem
	for(int samp = 0 ; samp < 1000 ; samp++){

		seed += 2;
		srand(seed);
		fprintf(walk, "#Amostra %ld\n", seed);
	    fprintf(walk, "#N x y dr2\n");

		walker(walk);
	}

    fclose(walk);
}

void walker(FILE *walk){

	int c;
    double dr2 = 0;
    x = 0;
    y = 0;

    for(int n = 0 ; n < N ; n++){
        
        dr2 = pow(x,2) + pow(y,2);

        fprintf(walk, "%d %d %d %f\n", n, x, y, dr2);
        
        c = (int) rand()%4;
        
        if(c == 0){
            x = x + 1; // direita
        }
        else if(c == 1){
            y = y + 1; // sobe
        }
        else if(c == 2){
            x = x - 1; // esquerda
        }
        else if(c == 3){
            y = y - 1; // desce
        }
    }
}
