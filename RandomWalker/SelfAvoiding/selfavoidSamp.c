#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define L 50 // lateral da caixa
#define N 1000 // numero de passos

int x = 0, y = 0; // [x, y]
int s[L*L] = {0}; // rede quadrada. onde o caminhante estiver é 1
int by = 0; // condicao de contorno em y
int bx = 0; // condicao de contorno em x

int walk(int c, int w);
int bcy(int w);
int bcx(int w);
int TemSaida(int w);

void main(void){

    long seed = 1234567;

	FILE *saida;
	saida = fopen("./ssamp.txt", "w");
	
    int c;

    for(int samp = 0 ; samp < 50 ; samp++){
        
        seed = seed + 2;
        srand(seed);

        int w = (int) rand()%(L*L); // sorteia uma posição inicial
        int waux = w;
        int n = 0;
        double dr2 = 0;
        int bc = 0;
        int continua = 0; // 0 é sim | 1 é nao
        x = y = bx = by = 0;
        
		// reinicializa a rede
		for(int i = 0 ; i < L*L ; i++){
			s[i] = 0;
		}
		s[w] = 1;

        fprintf(saida, "# Amostra %ld L %d Nmax %d\n", seed, L, N);
    	fprintf(saida, "# N w x y dr2 bc\n");
        printf("Amostra %d\n", samp);
        
        do{
            c = (int) rand()%4;
            
            waux = walk(c, w);
    
            if(s[waux] == 0){
    
                bc = bcx(w) + bcy(w);
                w = waux;
                s[w] = 1;
                
				// atualiza coordenadas para dr2
                if(c == 0){
                    y = y + 1; // sobe
                }
                else if(c == 1){
                    y = y - 1; // desce
                }
                else if(c == 2){
                    x = x + 1; // direita
                }
                else if(c == 3){
                    x = x - 1; // esquerda
                }

                dr2 = pow(x,2) + pow(y,2);

                fprintf(saida, "%d %d %d %d %f %d\n", n, w, x, y, dr2, bc);

                n++;
            }
			/**if(samp == 9){
			count++;
			printf("%d %d %d %d %d\n", n, count, c, s[w], s[waux]);
			
			FILE *sistema;
			sistema = fopen("./syst.txt", "w");
			fprintf(sistema, "#w %d\n", w);
			for(int i = 0 ; i < L*L ; i++){
				fprintf(sistema, "%d %d\n", i, s[i]);
			}
			break;
			}*/
            continua = TemSaida(w);

        }while(n < N && continua == 0);
    }

    fclose(saida);
}

int walk(int c, int w){

    by = bcy(w);
    bx = bcx(w);
    
    if(c == 0){
        //sobe
        if(by == 1){                                      // Talvez dê para tirar esses if de bc mudando a forma que calculo de waux e b
            // se estiver na primeira linha
                w = w - L + (L*L);
            }
            else{
                w = w - L;
            }
        }
    else if(c == 1){
            // desce

            if(by == 2){
                // se estiver na última linha
                w = (w%L);
            }
            else{
                w = w + L;
            }
        }
    else if(c == 2){
            // direita

            if(bx == 3){
                // se estiver na última coluna
                w = w - L + 1;
            }
            else{
                w = w + 1;
            }
        }
    else if(c == 3){
            // esquerda

            if(bx == 4){
                // se estiver na primeira coluna
                w = w + L - 1;
            }
            else{
                w = w - 1;
            }
        }

    return w;
}

int bcy(int w){
    /* 
       0 : sem condicao de contorno
       1 : primeira linha
       2 : ultima linha
    */

    int loc = 0;

    if(w < L){
        // se estiver na primeira linha
        loc = 1;
    }
    else if(w >= (L*L)-L){
        // se estiver na última linha
        loc = 2;
    }

    return loc;
}

int bcx(int w){
    /* 
       0 : sem condicao de contorno
       3 : ultima coluna
       4 : primeira coluna
    */

    int loc = 0;

    if(w%L == L-1){
        // se estiver na última coluna
        loc = 3;
    }
    else if(w%L == 0){
        // se estiver na primeira coluna
        loc = 4;
    }

    return loc;
}

int TemSaida(int w){

    int boolean = 0;
    int sum = 0;
    int by = bcy(w);
    int bx = bcx(w);

	if(by == 0){
		sum += s[w+L] + s[w-L];
	}
	if(bx == 0){
		sum += s[w+1] + s[w-1];
	}
    if(by == 1){
        sum += s[w+L] + s[w - L + (L*L)];
    }
    if(by == 2){
        sum += s[w%L] + s[w-L];
    }
    if(bx == 3){
        sum += s[w-1] + s[w + 1 - L];
    }
    if(bx == 4){
        sum += s[w - 1 + L] + s[w-1];
    }

    if(sum == 4){
        boolean = 1;
    }

    return boolean;
}
