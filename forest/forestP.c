#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#define L 50


int s[L*L] = {0};			// sitio sem arvore (0) ou sitio com arvore (1)
int f[L*L] = {0};			// sitio sem fogo (0) ou sitio com fogo (1)
int mviz[L*L][4] = {0};		// matriz de vizinhanca (guarda o indice do sitio vizinho) = [inferior, superior, esquerda, direita]


int sitio(int c, int waux);
int queimada(double p);


void main(int argc, char *argv[]){

	FILE *time;
	time = fopen("./Output/time.txt", "a");
	fprintf(time, "# Tempo de simulação para diferentes p\n");
	
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
		//printf("p %f\n", p);
		
	}while(p < 0.9);
	
	fclose(time);
}
	
int queimada(double p){
	
	int fogoEspalhou;
	int t = 0;
	
	// inicializao de arvores aleatorias conforme p
	for(int i = 0 ; i < L*L ; i++){
		
		double r = (double) rand() / (double)(RAND_MAX/1.);
		
		if(r < p){
			
			s[i] = 1;
			
			if(i < L){
				f[i] = 1; 		// fogo nas arvores da primeira linha
			}
		}
		else{
			s[i] = 0;
			f[i] = 0;
		}
	}

	// propagacao do fogo
	do{
		
		fogoEspalhou = false;
		
		for(int w = 0 ; w < L*L ; w++){
			
			// avalia se tem arvore sem fogo
			if(s[w] == 1 && f[w] == 0){
				
				for(int v = 0 ; v < 4 ; v++){

					//checa se algum vizinho tem fogo
					if(f[mviz[w][v]] == 1){
						f[w] = 1;
						fogoEspalhou = true;
					}
				}
			}
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