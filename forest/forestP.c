#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define L 150


int s[L*L] = {0};			// sitio sem arvore (0) ou sitio com arvore (1)
int f[L*L] = {0};			// sitio sem fogo (0) ou sitio com fogo (1)
int mviz[L*L][4] = {0};		// matriz de vizinhanca (guarda o indice do sitio vizinho) = [inferior, superior, esquerda, direita]
//FILE *fire;

int sitio(int c, int waux);
int queimada(double p);


void main(int argc, char *argv[]){

	FILE *time;
	time = fopen("./Output/time150.txt", "a");
	fprintf(time, "# Tempo de simulação para diferentes p\n");
	
	/*fire = fopen("./Output/fire.txt", "w");
	fprintf(fire, "# Sitios que pegaram fogo a cada tempo (0 = sem arvore , 1 = com arvore , 2 = com fogo)\n");
	fprintf(fire, "# sitio estado");*/
	
	int t;
	int wviz;
	double p = 0.3;
	int seed = atof(argv[1]);
	srand(seed);
	
	// inicializa rede de vizinhos
	for(int i = 0 ; i < L*L ; i++){
		for(int v = 0 ; v < 4 ; v++){
			wviz = sitio(v, i);
			mviz[i][v] = wviz;
		}
	}
	
	
	do{
		t = queimada(p);
		fprintf(time, "%f %d\n", p, t);
		
		p = p + 0.01;
		
	}while(p < 0.9);
	
	fclose(time);
}
	
int queimada(double p){
	
	int fogoEspalhou;
	int t = 0;
	/*if(p > 0.60 && p < 0.61){
		fprintf(fire, "\n%d ", t);
	}*/
	
	// inicializao de arvores aleatorias conforme p
	for(int i = 0 ; i < L*L ; i++){
		
		double r = (double) rand() / (double)(RAND_MAX/1.);
		
		if(r < p){
			
			s[i] = 1;
			
			if(i < L){
				f[i] = 1; 		// fogo nas arvores da primeira linha
			}
			else{
				f[i] = 0;
			}
		}
		else{
			s[i] = 0;
			f[i] = 0;
		}
		
		/*if(p > 0.60 && p < 0.61){
			fprintf(fire, "%d ", s[i]+f[i]);
		}*/
	}

	// propagacao do fogo
	do{
		/*if(p > 0.60 && p < 0.61){
			fprintf(fire, "\n%d ", t);
		}*/
		fogoEspalhou = false;
		
		for(int w = 0 ; w < L*L ; w++){
			
			// avalia se tem fogo
			if(f[w] == 1){
				
				for(int v = 0 ; v < 4 ; v++){

					//checa se algum vizinho tem arvore sem fogo
					if(f[mviz[w][v]] == 0 && s[mviz[w][v]] == 1){
						f[mviz[w][v]] = 1;
						fogoEspalhou = true;
					}
				}
			}
			/*if(p > 0.60 && p < 0.61){
				fprintf(fire, "%d ", s[w]+f[w]);
			}*/
		}
		
		t++;

	}while(fogoEspalhou == true);
	
	return t;
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