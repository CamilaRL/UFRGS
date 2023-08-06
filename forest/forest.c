#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define L 50


int s[L*L] = {0};			// sitio sem arvore (0) ou sitio com arvore (1) ou sitio com fogo (2)
int f[L*L] = {0};			// sitios
int mviz[L*L][4] = {0};		// matriz de vizinhanca dos sitios = [inferior, superior, esquerda, direita]


int sitio(int c, int waux);
bool TemVida();


void main(void){
	
	FILE *fire;
	fire = fopen("fire.txt", "w");
	fprintf(fire, "# Sitios que pegaram fogo a cada tempo");
	
	FILE *forest;
	forest = fopen("forest.txt", "w");
	fprintf(forest, "# Inicializacao da floresta (0 = sem arvore , 1 = com arvore , 2 = com fogo)\n");
	fprintf(forest, "# sitio estado\n");
	
	bool tem_vida = true;
	int t = 0;
	int wviz;
	
	// inicializao de arvores aleatorias conforme p
	double p = 0.5;
	
	for(int i = 0 ; i < L*L ; i++){
		
		double r = (double) rand() / (double)(RAND_MAX/1.);
		
		if(r < p){
			if(i < L){
				s[i] = 2; 		// fogo nas arvores da primeira linha
			}
			else{
				s[i] = 1;
			}
			
			// atualiza matriz de vizinhos de sitio
			for(int v = 0 ; v < 4 ; v++){
				mviz[sitio(v, i)][v] = s[i];
			}
		}
		
		fprintf(forest, "%d %d\n", i, s[i]);
	}
	
	fclose(forest);
	
	
	// propagacao do fogo
	do{
		fprintf(fire, "\n%d ", t);
		printf("%d\n", t);
		
		for(int w = 0 ; w < L*L ; w++){
			
			// se o sitio tem fogo
			if(s[w] == 2){
				
				for(int v = 0 ; v < 4 ; v++){
					wviz = sitio(v, w); 		// vizinho do sitio com fogo
					
					// passa fogo para os vizinhos com arvores
					if(mviz[wviz][v] = 1){
						
						s[wviz] = 2;
						
						// indica pros vizinhos do vizinho que agora ele tem fogo
						for(int vv = 0 ; vv < 4 ; vv++){
							mviz[sitio(vv, wviz)][vv] = s[wviz];
						}
						
						fprintf(fire, "%d ", wviz);
						
					}
				}
				
			}
		}
		
		tem_vida = TemVida();
		
		t++;
		
	}while(tem_vida == true);
	
	fclose(fire);
}


bool TemVida(){
	
	bool temvida = false;
	int w = 0;
	
	do{
		
		if(s[w] == 1){
			for(int v = 0 ; v < 4 ; v++){
				
				// se a arvore tiver vizinho com fogo
				if(mviz[sitio(v,w)][v] == 2){
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