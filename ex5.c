#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

double dist_inv(double r){
    return -log(1-r);
}

void main(void){
    
    double I = 0;
    float gamma = -0.8;
    long t = 124867999;
    srand(t);
    
    double r;
    double x;
        
    FILE *saida;
    saida = fopen("saida", "w");
    fprintf(saida, "#x I\n");
    
    for(int i = 1 ; i < 100000 ; i++){

        r = (double)rand() / (double)(RAND_MAX/1.);
        x = dist_inv(r);

        fprintf(saida, "%f\n", x);
    }
}
