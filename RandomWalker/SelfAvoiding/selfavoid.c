#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
// unison
#define L 50 // lateral da caixa
#define N 1000 // numero de passos

int x = 0, y = 0; // [x, y]

void walker(FILE *file);

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

		walker(saida);
	}

    fclose(saida);  
}

void walker(FILE *file){

    int w = 50;
    int waux = w;
	int c;
    double dr2 = 0.0;
    int s[L*L] = {0}; // rede quadrada. onde o caminhante estiver é 1
    int bc = 0; // 0 se não cruzou os limites da caixa | 1 se cruzou os limites da caixa
    int gameover = 0; // 0 a cobrinha n travou | 1 a cobrinha travou
    int n = 0;

    x = 0;
    y = 0;

    do{
		// Verifica se já passou pelo sítio e se ele tem para onde ir
		//fprintf(file, "%d %d %d %d w=%d L=%d\n", s[w-1], s[w+1], s[w-L], s[w+L], w, L);
		
        if( (s[w-1]+s[w+1]+s[w-L]+s[w+L]) == 4){
            gameover = 1;
        }
        else if(s[waux] == 0){
			
			dr2 = pow(x,2) + pow(y,2);

			fprintf(file, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);
            
			w = waux;
            s[w] = 1;
            n++;
        }
		
        c = (int) rand()%4;
        //fprintf(file, "c=%d gameover=%d %d,%d ",c, gameover, x, y);
        if(c == 0){
            // sobe
            y = y + 1; //fprintf(file, "sobe\n");

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
            y = y - 1; //fprintf(file, "desce\n");

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
            x = x + 1; //fprintf(file, "direita\n");

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
            x = x - 1; //fprintf(file, "esquerda\n");

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
        
    }while(n < N && gameover == 0);
}
