#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define kB 1 // 1.38e-23 kg.m^2/K.s^2
#define T 2
#define N 100
#define tmax N*N
#define MCS_max 10000

void inicial_sys(int (*s)[N])
{

    // Gerador de estado inicial aleatório
    for(int i = 0 ; i < N ; i++)
    {   
        for(int j = 0 ; j < N ; j++)
        {
            s[i][j] = pow(-1, rand() % 2);
        } 
    }    
}

void spins_positions(FILE *arq_Spins, int (*s)[N], int t)
{
    // Salvar spins e energias nos arquivos txt
    fprintf(arq_Spins, "%i  ", t);

    for(int i = 0 ; i < N ; i++)
    {            
        for(int j = 0 ; j < N ; j++)
        {
            fprintf(arq_Spins, "%i, ", s[i][j]);
            //printf("%i ", s[i][j]);
        }
        fprintf(arq_Spins, "// ");
        //printf("\n");
    }
    fprintf(arq_Spins, "\n"); 
}

int BC(int k)
{
    // Funcao que calcula a condicao de contorno (Boundary Condition)
    int test = k;
    if (k > (N-1))
    {
        test = 0;
    }
    else if (k < 0)
    {
        test = N-1;
    }

    return test;
}

void energy_sys(int (*s)[N], float *E)
{
    int col, lin, J = 1;
    
    for(int i = 0 ; i < N ; i++)
    {
        for(int j = 0 ; j < N ; j++)
        {
            col = BC(i + 1); // Nao conta par de vizinhos duas vezes
            lin = BC(j + 1);

            *E += s[i][j]*s[col][j] + s[i][j]*s[i][lin];
        }
    }
    *E = -J*(*E/2.0); // Dividir por 2 para nao contar repetido 
}

void magnetization_sys(int (*s)[N], float *M)
{
    for(int i = 0 ; i < N ; i++)
    {
        for(int j = 0 ; j < N ; j++)
        {
            *M += s[i][j];
        }
    }
}

void metropolis(int (*s)[N], float *E, float *M)
{
    int sn = 0, dE = 0, v = 0;
    int i, j, col, lin;
    float En = 0, Mn = 0;
    double n, boltz;

    // Novo estado
    i = rand() % (N-1);
    j = rand() % (N-1);

    sn = s[i][j]*(-1);

    //printf("\ni: %i j: %i\n", i, j);
    //printf("sn: %i s: %i\n", sn, s[i][j]);

    for(int m = 0 ; m < 2 ; m++)
    {
            col = BC(i + (int)pow(-1, m));
            lin = BC(j + (int)pow(-1, m));

            v = v + s[col][j] + s[i][lin];    
    }

    dE = 2*s[i][j]*v;

    // Probabilidade de transição

    n = (float)rand()/(float)(RAND_MAX);
    boltz = exp(-dE/(kB*T));

    //printf("Delta E: %i n: %f boltz: %f\n", dE, n, boltz);

    if(dE < 0 || n < boltz)
    {
        s[i][j] = sn;
        *E = *E + dE;
        *M = *M + 2*sn;
        
        //printf("Trocou!");
    }
}

void main(void){

    int s[N][N] = {}; // Sitios de spins
    float E = 0;
    float M = 0;
    float E_med = 0, M_med = 0;

    // Arquivos para salvar as energias e spins
    FILE *arq_Energias;
    arq_Energias = fopen("energia.txt", "w");
    fprintf(arq_Energias, "# N: %i T: %i\n#MCS E\n", N, T);

    FILE *arq_Magnetiz;
    arq_Magnetiz = fopen("magnetizacao.txt", "w");
    fprintf(arq_Magnetiz, "# N: %i T: %i\n#MCS M\n", N, T);

    FILE *arq_Spins;
    arq_Spins = fopen("spins.txt", "w");
    fprintf(arq_Spins, "# N: %i T: %i\n#MCS S\n", N, T);

    // Inicializacao
    inicial_sys(s);
    energy_sys(s, &E);
    magnetization_sys(s, &M);

    // Evolucao monte carlo
    for(int MCS = 0 ; MCS < MCS_max ; MCS++)
    {
        printf("\nMCS: %i E: %f M: %f\n", MCS, E_med, M_med);

        // Evolucao temporal
        for(int t = 0 ; t < tmax ; t++)
        { 
            // Aplicacao do metropolis
            metropolis(s, &E, &M);
        }

        if(MCS < MCS_max)
            {
                E_med += (E/(tmax*tmax)); // The division is by N*N because is the mean of time and mean of spin 
                M_med += (fabs(M)/(tmax*tmax)); // Take the absolute value due to degeneration of magnetization

                // Salvar spins e energias nos arquivos txt
                fprintf(arq_Energias, "%i %f\n", MCS, E_med);
                fprintf(arq_Magnetiz, "%i %f\n", MCS, M_med);
                spins_positions(arq_Spins, s, MCS);
            }
    }
    
    
    fclose(arq_Energias);
    fclose(arq_Magnetiz);
    fclose(arq_Spins);
}