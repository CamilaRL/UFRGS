#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <string.h>
#include <stdbool.h>



#define N 256 //1024
#define nO 4 //6

#define PI 3.14159
#define kB 1 //1.38e-23
#define e0 1 //8.854e-12
#define hbar 1 //1.054e-34;


extern int dsyev_(char*, char*, int*, double*, int*, double*, double*, int*, int*);
	// JOBZ, UPLO, N, A, LDA, W, WORK, LWORK, INFO

extern void dgemv_(char*, int*, int*, double*, double*, int*, double*, int*, double*, double*, int*);
	// trans, m, n, alpha, A, lda, x, incx, beta, y, incy

extern double ddot_(int*, double*, int*, double*, int*);


void diagonalizacao(void);

void main(void){

	diagonalizacao();
}

void diagonalizacao(void){

    printf("## Diagonalizacao\n");

    char filename[30] = {0};
    char matriz[50] = {0};

    FILE *output;
    sprintf(filename, "./resultados/%i_autocoisas.txt", nO);
    output = fopen(filename, "a+");

    FILE *input;
    sprintf(matriz, "./resultados/%i_hamiltoniano.txt", nO);
    input = fopen(matriz, "r");


    double **M = (double **)malloc(N * sizeof(double *));
    for (int i = 0 ; i < N ; i++) {
        M[i] = (double *)malloc(N * sizeof(double));
    }

    char linha[20];

    printf("Leitura da Matriz\n");
    for(int i = 0 ; i < N ; i++){

	for(int j = 0 ; j < N ; j++){

	     fgets(linha, 20, input);
	     sscanf(linha, "%lf", &M[i][j]);
	}
    }

    fclose(input);


    char jobz = 'V';
    char uplo = 'U';

    int n = N;
    int lda = N;
    int lwork = (3*N) - 1;
    int info;

    double *A = (double *)malloc(lda * N * sizeof(double));
    double w[N];
    double work[lwork];


	// Mapeamento da matriz M para a estrutura de Fortran:
    for(int i =  0 ; i < N ; i++){
        for(int j = 0 ; j < N ; j++){

            A[j + i*N] = M[i][j];
        }
    }

    // Liberação de memória alocada para a matriz M
    for (int i = 0; i < N; i++) {
        free(M[i]);
    }
    free(M);

    dsyev_(&jobz, &uplo, &n, A, &lda, w, work, &lwork, &info);

    fprintf(output, "Autovalores\n");
    for(int i = 0 ; i<n ; i++){
        fprintf(output, "%f\n", w[i]);
    }


    fprintf(output, "Autovetores\n");
    for(int i = 0 ; i < N ; i++){
		for(int j = 0 ; j < N ; j++){

			// Ajusta o índice para acessar os elementos na ordem de Fortran
			double element = A[i*N + j];
			fprintf(output, "%f\n", element);
		}
    }

    fclose(output);

}
