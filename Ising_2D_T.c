#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define kB 1 // 1.38e-23 kg.m^2/K.s^2
//#define T 1
#define N 20
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
    int col, lin;
    float J = 1;
    
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

void metropolis(int (*s)[N], float *E, float *M, float T)
{
    int sn = 0, dE = 0, v = 0;
    int i, j, col, lin;
    float En = 0, Mn = 0;
    double n, boltz;

    // Novo estado
    i = rand() % (N);
    j = rand() % (N);

    sn = s[i][j]*(-1);

    //printf("\ni: %i j: %i\n", i, j);
    //printf("sn: %i s: %i\n", sn, s[i][j]);

    for(int m = 0 ; m < 2 ; m++)
    {
            col = BC(i + (int)pow(-1, m));
            lin = BC(j + (int)pow(-1, m));

            v += s[col][j] + s[i][lin];    
    }

    dE = 2*s[i][j]*v;

    // Probabilidade de transição
    n = (float)rand()/(float)(RAND_MAX);
    boltz = exp(-dE/(kB*T));

    //printf("Delta E: %i n: %f boltz: %f\n", dE, n, boltz);
    
    if(dE < 0 || n < boltz)
    {
        s[i][j] = sn;
        *E += dE;
        *M += 2*sn;
    }
}

/////////////////////////////////////////// MAIN //////////////////////////////////////////////////

void main(void){

    int s[N][N] = {}; // Spins sites
    float E = 0.0, M = 0.0, T = 2.0;
    float E_med = 0.0, M_med = 0.0, X_med = 0.0, C_med = 0.0; // Mean values of energy, magnetization, 
                                                      // susceptibility and specific heat.
    float E2_med = 0.0, M2_med = 0.0;
    long tmax = N*N;

    // Files to save the energy, magnetization and spin
    FILE *arq_Energias;
    arq_Energias = fopen("energiaT.txt", "w");
    fprintf(arq_Energias, "# N: %i\n#T E\n", N);

    FILE *arq_Magnetiz;
    arq_Magnetiz = fopen("magnetizacaoT.txt", "w");
    fprintf(arq_Magnetiz, "# N: %i\n#T M\n", N);
    
    FILE *arq_Suscep;
    arq_Suscep = fopen("susceptibilidadeT.txt", "w");
    fprintf(arq_Suscep, "# N: %i\n#T X\n", N);

    FILE *arq_CalorEsp;
    arq_CalorEsp = fopen("calorespecificoT.txt", "w");
    fprintf(arq_CalorEsp, "# N: %i\n#T C\n", N);

    FILE *arq_Spins;
    arq_Spins = fopen("spinsT.txt", "w");

    // Inicialization
    inicial_sys(s);
    energy_sys(s, &E);
    magnetization_sys(s, &M);


    do
    {
        fprintf(arq_Spins, "# N: %i T: %f\n#t S\n", N, T);

        // Monte Carlo Step Evolution
        for(int MCS = 0 ; MCS < MCS_max ; MCS++)
        {
            // Time evolution
            for(int t = 0 ; t < tmax ; t++)
            {   
                //printf("\nt: %i E: %f M: %f\n", t, E, M);
                // Metropolis Method Aplication
                metropolis(s, &E, &M, T);
            }
            
            if(MCS > MCS_max/100) // Após o equilíbrio
            {
                E_med += E; // The division is by N*N because is the mean of time and mean of spin 
                M_med += fabs(M); // Take the absolute value due to degeneration of magnetization
                E2_med += E*E;
                M2_med += M*M;
            }
            
        }

        E_med = E_med/(MCS_max*tmax);
        M_med = M_med/(MCS_max*tmax);
        E2_med = E2_med/(MCS_max*tmax*tmax);
        M2_med = M2_med/(MCS_max*tmax*tmax);

        X_med = tmax*(M2_med - (M_med*M_med))/(kB*T);
        C_med = tmax*(E2_med - (E_med*E_med))/(kB*T*T);

        fprintf(arq_Energias, "%f %f\n", T, E_med);
        fprintf(arq_Magnetiz, "%f %f\n", T, M_med);
        fprintf(arq_Suscep, "%f %f\n", T, X_med);
        fprintf(arq_CalorEsp, "%f %f\n", T, C_med);

        printf("T: %f E: %f M: %f X: %f C: %f\n", T, E_med, M_med, X_med, C_med);

        E_med = 0.0;
        M_med = 0.0;

        T += 0.010;

    } while (T < 3);
    
    fclose(arq_Energias);
    fclose(arq_Magnetiz);
    fclose(arq_Spins);
}