#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

void main(void){
    
    double I = 0;
    float gamma = -0.8; 
    long t = 124867999;
    srand(t);
        
    FILE *saida;
    saida = fopen("saida-08", "w");
    fprintf(saida, "#x I\n");
    
    for(int i = 1 ; i < 1000000 ; i++){

        double x = (double)rand() / (double)(RAND_MAX/1.);
        I = I + pow(x, gamma);
        fprintf(saida, "%d %f\n", i, I/i);
    }
}
