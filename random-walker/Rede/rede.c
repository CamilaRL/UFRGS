#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
// unison
#define L 20 // lateral da caixa
#define N 1000 // numero de passos

int x = 0, y = 0; // [x, y]

void walker(FILE *file);

void main(void){

	long seed = 1234567;

	FILE *saida;
	saida = fopen("./r.txt", "w");

	// Amotragem
	for(int samp = 0 ; samp < 1000 ; samp++){

		seed += 2;
		srand(seed);
		fprintf(saida, "#Amostra %ld L %d Nmax %d\n", seed, L, N);
	    fprintf(saida, "#N w x y dr2\n");

		walker(saida);
	}

    fclose(saida);  
}

void walker(FILE *file){

    int w = 30;
	int c;
    double dr2 = 0.0;
    int s[L*L] = {0}; // rede quadrada. onde o caminhante estiver é 1
    int bc = 0; // 0 se não cruzou os limites da caixa | 1 se cruzou os limites da caixa
    s[w] = 1;
    x = 0;
    y = 0;

    for(int n = 0 ; n < N ; n++){
        
        dr2 = pow(x,2) + pow(y,2);

        fprintf(file, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);
        
        c = (int) rand()%4;
        
        if(c == 0){
            // sobe
            y = y + 1;

            if(w < L){
                // se estiver na primeira linha
                w = w - L + (L*L);
                bc = 1;
            }
            else{
                w = w - L;
                bc = 0;
            }
        }
        else if(c == 1){
            // desce
            y = y - 1;

            if(w >= (L*L)-L){
                // se estiver na última linha
                w = (w%L);
                bc = 1;
            }
            else{
                w = w + L;
                bc = 0;
            }
        }
        else if(c == 2){
            // direita
            x = x + 1;

            if(w%L == L-1){
                // se estiver na última coluna
                w = w - L + 1;
                bc = 1;
            }
            else{
                w = w + 1;
                bc = 0;
            }
        }
        else if(c == 3){
            // esquerda
            x = x - 1;

            if(w%L == 0){
                // se estiver na primeira coluna
                w = w + L - 1;
                bc = 1;
            }
            else{
                w = w - 1;
                bc = 0;
            }
        }
    }
}
