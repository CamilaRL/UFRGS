#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define L 50 				// lateral da caixa
#define N 1000				// numero de passos



int xaux = 0, yaux = 0;		// posição (sem condicao de contorno)
int bcaux = 0;				// condicao de contorno : 1 passou | 0 não pasou

int s[L*L] = {0};			// rede quadrada. onde o caminhante estiver é 1
int viz[L*L][4] = {0};		// matriz de vizinhos = [inferior, superior, esquerda, direita]



int walk(int c, int w);

void main(void){

    long seed = 1236255;

	FILE *saida;
	char filename[30] = {0};

	int c, x, y, bc, w, waux, n, continua, sum;		// bc: condição de contorno do passo dado (impressa)
	double dr2;


	for(int fnum = 0 ; fnum < 3 ; fnum++){		// separa em arquivos as amostras
		
		sprintf(filename, "./ssamp%d.txt", fnum);
		saida = fopen(filename, "w");

		for(int samp = 0 ; samp < 100000 ; samp++){

        
			seed = seed + 2;
			srand(seed);

			w = (int) rand()%(L*L); // sorteia uma posição inicial
			n = 0;
			dr2 = 0;
			continua = 0;		// 0 é sim | 1 é nao
			bc = 0;
			x = y = xaux = yaux = 0;
        
			for(int i = 0 ; i < L*L ; i++){ 	// reinicializa a rede
				s[i] = 0;
				viz[i][0] = 0;
				viz[i][1] = 0;
				viz[i][2] = 0;
				viz[i][3] = 0;
			}
			s[w] = 1;
			
			for(int i = 0 ; i < 4 ; i++){
				viz[walk(i, w)][i] = s[w];
			}
	
	
			fprintf(saida, "# Amostra %d seed %ld L %d Nmax %d\n", samp, seed, L, N);
			fprintf(saida, "# N w x y dr2 bc\n");
			fprintf(saida, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);
			printf("Amostra %d\n", samp);
			
			
			do{
				c = (int) rand()%4;
	
				waux = walk(c, w);
	
				if(s[waux] == 0){
		
					n++;
					
					w = waux;
					bc = bcaux;
					y = yaux;
					x = xaux;
					
					s[w] = 1;
					
					dr2 = pow(x,2) + pow(y,2);
					
					for(int i = 0 ; i < 4 ; i++){
						viz[walk(i, w)][i] = s[w];
					}
	
					fprintf(saida, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);                
				}
				
				yaux = y;
				xaux = x;
			
				// avalia se tem saida
				sum = viz[w][0] + viz[w][1] + viz[w][2] + viz[w][3];
				
				if(sum == 4){
					continua = 1;
					printf("Sem saida %d\n", n);
				}
            
			}while(n < N && continua == 0);
		}	

		fclose(saida);
	}
}

int walk(int c, int waux){

    if(c == 0){				//sobe
        if(waux < L){			// se estiver na primeira linha
            waux = waux - L + (L*L);
			bcaux = 1;
        }
        else{
            waux = waux - L;
			bcaux = 0;
        }
		yaux = yaux + 1;
    }
    else if(c == 1){		// desce

        if(waux >= (L*L)-L){	// se estiver na última linha
            waux = (waux%L);
			bcaux = 1;
        }
        else{
            waux = waux + L;
			bcaux = 0;
        }	
		yaux = yaux - 1;
    }
    else if(c == 2){		// direita

        if(waux%L == L-1){		// se estiver na última coluna
            waux = waux - L + 1;
			bcaux = 1;
        }
        else{
			waux = waux + 1;
			bcaux = 0;
        }	
		xaux = xaux + 1;
    }
    else if(c == 3){		// esquerda

        if(waux%L == 0){		// se estiver na primeira coluna
            waux = waux + L - 1;
			bcaux = 1;
        }
		else{
            waux = waux - 1;
			bcaux = 0;
        }	
		xaux = xaux - 1;
    }

    return waux;
}