#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define L 150


int s[L*L] = {0};			// sitio sem arvore (0) ou sitio com arvore (1)
int f[L*L] = {0};			// sitio sem fogo (0) ou sitio com fogo (1)
int mviz[L*L][4] = {0};		// matriz de vizinhanca (com fogo (1) ou sem fogo (0)) = [inferior, superior, esquerda, direita]


int sitio(int c, int waux);
bool TemVida();


void main(void){
	
	/*FILE *fire;
	fire = fopen("fire.txt", "w");
	fprintf(fire, "# Sitios que pegaram fogo a cada tempo");
	
	FILE *forest;
	forest = fopen("forest.txt", "w");
	fprintf(forest, "# Inicializacao da floresta (0 = sem arvore , 1 = com arvore , 2 = com fogo)\n");
	fprintf(forest, "# sitio estado\n");*/
	
	FILE *time;
	time = fopen("time150.txt", "w");
	fprintf(time, "# Tempo de simulação para diferentes p\n");
	
	bool temvida = true;
	int t = 0;
	int wviz;
	long seed = 12345671;
	
	
	for(int samp = 0 ; samp < 100 ; samp++){
		
		seed = seed + 2;
		srand(seed);
		
		printf("Amostra %d", samp);
		fprintf(time, "#Amostra %d seed %ld\n", samp, seed);
		
	double p = 0.3;
	do{
		printf("# %f\n", p);
		
		// inicializao de arvores aleatorias conforme p
		for(int i = 0 ; i < L*L ; i++){
			
			double r = (double) rand() / (double)(RAND_MAX/1.);
		
			if(r < p){
			
				s[i] = 1;
			
				if(i < L){
					f[i] = 1; 		// fogo nas arvores da primeira linha
				}
			
				// atualiza os vizinhos do sitio
				for(int v = 0 ; v < 4 ; v++){
					mviz[sitio(v, i)][v] = f[i];
				}
			}
		
			//fprintf(forest, "%d %d\n", i, s[i]+f[i]);		// soma s[i]+f[i] = 2 (arvore com fogo) ou 1 (arvore sem fogo) ou 0 (sem arvore)
		}
	
		//fclose(forest);
	
	
		// propagacao do fogo
		do{
			//fprintf(fire, "\n%d ", t);
			
			//printf("%d\n", t);
			
			for(int w = 0 ; w < L*L ; w++){
				
				// avalia se tem arvore sem fogo
				if(s[w] == 1 && f[w] == 0){
					
					for(int v = 0 ; v < 4 ; v++){
							
						//checa se algum vizinho tem fogo
						if(mviz[w][v] == 1){
							f[w] = 1;
						}
					}
				}
			}
			
			// atualiza matriz de vizinhos
			for(int w = 0 ; w < L*L ; w++){
				
				mviz[w][0] = f[sitio(1, w)];
				mviz[w][1] = f[sitio(0, w)];
				mviz[w][2] = f[sitio(3, w)];
				mviz[w][3] = f[sitio(2, w)];
			
				//fprintf(fire, "%d ", s[w]+f[w]);
			
			
			}
			temvida = TemVida();
			t++;
		
		}while(temvida == true);
	
	//fclose(fire);
	
	fprintf(time, "%f %d\n", p, t);
	
	t = 0;
	p = p + 0.01;
	temvida = true;
	
	for(int w = 0 ; w < L*L ; w++){
		s[w] = 0;
		f[w] = 0;
		mviz[w][0] = 0;
		mviz[w][1] = 0;
		mviz[w][2] = 0;
		mviz[w][3] = 0;
	}
	
	
	}while(p < 0.9);
	
	}
}


bool TemVida(){
	
	bool temvida = false;
	int w = 0;
	
	do{
		if(f[w] == 0 && s[w] == 1){
			for(int v = 0 ; v < 4 ; v++){
				// se a arvore tiver vizinho com fogo
				if(mviz[w][v] == 1){
					temvida = true;
				}
			}
		}		
		w++;
		
	}while(w < L*L && temvida == false);

	return temvida;
}

int sitio(int c, int waux){

    if(c == 0){							//sobe
	
        if(waux < L){					// se estiver na primeira linha
            waux = waux - L + (L*L);
        }
        else{
            waux = waux - L;
        }
    }
    else if(c == 1){					// desce

        if(waux >= (L*L)-L){			// se estiver na última linha
            waux = (waux%L);
        }
        else{
            waux = waux + L;
        }	
    }
    else if(c == 2){					// direita

        if(waux%L == L-1){				// se estiver na última coluna
            waux = waux - L + 1;
        }
        else{
			waux = waux + 1;
        }	
    }
    else if(c == 3){					// esquerda

        if(waux%L == 0){				// se estiver na primeira coluna
            waux = waux + L - 1;
        }
		else{
            waux = waux - 1;
        }	
    }

    return waux;
}