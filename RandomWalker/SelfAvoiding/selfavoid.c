#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
// unison
#define L 50 // lateral da caixa
#define N 1000 // numero de passos

int x = 0, y = 0; // [x, y]
int s[L*L] = {0}; // rede quadrada. onde o caminhante estiver é 1

void Walker(FILE *file);
int Gameover(int w);

void main(void){

	long seed = 1234567;

	FILE *saida;
	saida = fopen("./s.txt", "w");

	// Amotragem
	for(int samp = 0 ; samp < 1 ; samp++){

		seed += 2;
		srand(seed);
		fprintf(saida, "#Amostra %ld L %d Nmax %d\n", seed, L, N);
	    fprintf(saida, "#N w x y dr2\n");

		Walker(saida);
	}

    fclose(saida);  
}

void Walker(FILE *file){

    int w = 30;
    int waux = w;
	int c;
    double dr2 = 0.0;
    int bc = 0; // 0 se não cruzou os limites da caixa | 1 se cruzou os limites da caixa
    int gameover = 0; // 0 a cobrinha n travou | 1 a cobrinha travou
    int n = 0;

    x = 0;
    y = 0;

    do{

        // Verifica se já passou pelo sítio
        if(s[waux] == 0){

            w = waux;
            s[w] = 1;
            dr2 = pow(x,2) + pow(y,2);

            fprintf(file, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);

            n++;
        }

        c = (int) rand()%4;
        
        if(c == 0){
            // sobe
            y = y + 1;

            if(w < L){
            // se estiver na primeira linha
                waux = w - L + (L*L);
                bc = 1;
            }
            else{
                waux = w - L;
                bc = 0;
            }
        }
        else if(c == 1){
            // desce
            y = y - 1;

            if(w >= (L*L)-L){
                // se estiver na última linha
                waux = (w%L);
                bc = 1;
            }
            else{
                waux = w + L;
                bc = 0;
            }
        }
        else if(c == 2){
            // direita
            x = x + 1;

            if(w%L == L-1){
                // se estiver na última coluna
                waux = w - L + 1;
                bc = 1;
            }
            else{
                waux = w + 1;
                bc = 0;
            }
        }
        else if(c == 3){
            // esquerda
            x = x - 1;

            if(w%L == 0){
                // se estiver na primeira coluna
                waux = w + L - 1;
                bc = 1;
            }
            else{
                waux = w - 1;
                bc = 0;
            }
        }
        
        gameover = Gameover(w);
        
    }while(n < N && gameover == 0);
}

int Gameover(int w){

    int c = 0;
    int sum = 0;
    
    // superior
    if(w < L){
        sum += s[w - L + (L*L)];
    }
    else{
        sum += s[w-L];
    }
    // inferior
    if(w >= (L*L)-L){
        sum += s[w%L];
    }
    else{
        sum += s[w+L];
    }
    // esquerda
    if(w%L == 0){
        sum += s[w + L - 1];
    }
    else{
        sum += s[w-1];
    }
    // direita
    if(w%L == L-1){
        sum += s[w - L + 1];
    }
    else{
        sum += s[w+L];
    }
    
    
    if(sum == 4){
        c = 1;
    }
    
    return c;
}
