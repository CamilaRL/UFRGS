#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define kB 1 // 1.38e-23 kg.m^2/K.s^2
#define L 30
#define MCS_max 10000

void inicial_sys(int (*s)[L]);

void spins_positions(FILE *arq_Spins, int (*s)[L], int t);

int BC(int k);

void energy_sys(int (*s)[L], double *E);

void magnetization_sys(int (*s)[L], double *M);

void metropolis(int (*s)[L], double *E, double *M, double T);

/////////////////////////////////////////// MAIN //////////////////////////////////////////////////

void main(void){

    int s[L][L] = {}; // Spins sites
    char filename[30] = {0};
    double E = 0.0, M = 0.0, T = 1.5;
    double E2_med = 0.0, M2_med = 0.0;
    long N = L*L;
    double E_med = 0.0, M_med = 0.0, X_med = 0.0, C_med = 0.0; // Mean values of energy, magnetization, 
                                                      // susceptibility and specific heat.

    // Files to save the data
    FILE *arq_Energias;
    sprintf(filename, "%s/energiaT_%i.txt", "./Resultados", L);
    arq_Energias = fopen(filename, "w");
    fprintf(arq_Energias, "# L: %i\n#T E\n", L);

    FILE *arq_Magnetiz;
    sprintf(filename, "%s/magnetizacaoT_%i.txt", "./Resultados", L);
    arq_Magnetiz = fopen(filename, "w");
    fprintf(arq_Magnetiz, "# L: %i\n#T M\n", L);
    
    FILE *arq_Suscep;
    sprintf(filename, "%s/susceptibilidadeT_%i.txt", "./Resultados", L);
    arq_Suscep = fopen(filename, "w");
    fprintf(arq_Suscep, "# L: %i\n#T X\n", L);

    FILE *arq_CalorEsp;
    sprintf(filename, "%s/calorespecificoT_%i.txt", "./Resultados", L);
    arq_CalorEsp = fopen(filename, "w");
    fprintf(arq_CalorEsp, "# L: %i\n#T C\n", L);

    FILE *arq_Spins;
    sprintf(filename, "%s/spinsT_%i.txt", "./Resultados", L);
    arq_Spins = fopen(filename, "w");

    // Inicialization
    inicial_sys(s);
    energy_sys(s, &E);
    magnetization_sys(s, &M);


    do
    {
        //fprintf(arq_Spins, "# L: %i T: %f\n#t S\n", L, T);

        // Monte Carlo Step Evolution
        for(int MCS = 0 ; MCS < MCS_max ; MCS++)
        {
            // Time evolution
            for(int t = 0 ; t < 100 ; t++)
            {   
                //printf("\nt: %i E: %f M: %f\n", t, E, M);
                // Metropolis Method Aplication
                metropolis(s, &E, &M, T);
            }
            
            if(MCS > MCS_max/10000) // Após o equilíbrio
            {
                E_med += E; // The division is by L*L because is the mean of time and mean of spin 
                M_med += fabs(M); // Take the absolute value due to degeneration of magnetization
                E2_med += E*E;
                M2_med += M*M;

                //spins_positions(arq_Spins, s, MCS);
            }
            
        }

        E_med = E_med/(MCS_max);
        M_med = M_med/(MCS_max);
        E2_med = E2_med/(MCS_max);
        M2_med = M2_med/(MCS_max);

        X_med = (M2_med - (M_med*M_med))/(N*kB*T); // Susceptibilility
        C_med = (E2_med - (E_med*E_med))/(N*kB*T*T); // Specific Heat

        E_med = E_med/N; // Energia por spin
        M_med = M_med/N; // Magnetizacao por spin

        fprintf(arq_Energias, "%f %f\n", T, E_med);
        fprintf(arq_Magnetiz, "%f %f\n", T, M_med);
        fprintf(arq_Suscep, "%f %f\n", T, X_med);
        fprintf(arq_CalorEsp, "%f %f\n", T, C_med);

        printf("T: %f E: %f M: %f X: %f C: %f\n", T, E_med, M_med, X_med, C_med);

        E_med = 0.0;
        M_med = 0.0;
        E2_med = 0.0;
        M2_med = 0.0;

        T += 0.010;

    } while (T < 3);
    
    fclose(arq_Energias);
    fclose(arq_Magnetiz);
    fclose(arq_Spins);
}

/////////////////////////////////////////// FUNCTIONS //////////////////////////////////////////////////

void inicial_sys(int (*s)[L])
{
    /*
    Random initialization of the spin grid

    INPUT
        int (*s)[L] : 2D array with the spin values
    */
    for(int i = 0 ; i < L ; i++)
    {   
        for(int j = 0 ; j < L ; j++)
        {
            s[i][j] = pow(-1, rand() % 2);
        } 
    }    
}

void spins_positions(FILE *arq_Spins, int (*s)[L], int t)
{
    
    /*
    Save each spin value

    INPUT
        FILE *arq_Spins : file for saving spin values
        int (*s)[L] : 2D array with the spin values
        int t : simuçation time / Monte Carlo Steps (MCS)
    */
    fprintf(arq_Spins, "%i  ", t);

    for(int i = 0 ; i < L ; i++)
    {            
        for(int j = 0 ; j < L ; j++)
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
    /*
    Function to compute the Boundary Condition
    
    INPUT
        int k : spin index
    OUTPUT
        int test : new index if the boundary conidtion is applied
    */ 

    int test = k;
    if (k > (L-1))
    {
        test = 0;
    }
    else if (k < 0)
    {
        test = L-1;
    }

    return test;
}

void energy_sys(int (*s)[L], double *E)
{
    /*
    Compute the total energy of the system

    INPUT
        int (*s)[L] : 2D array with the spin values
        double *E : total energy of the system
    */
    int col, lin;
    float J = 1.;
    
    for(int i = 0 ; i < L ; i++)
    {
        for(int j = 0 ; j < L ; j++)
        {
            col = BC(i + 1); // Nao conta par de vizinhos duas vezes
            lin = BC(j + 1);

            *E += s[i][j]*s[col][j] + s[i][j]*s[i][lin];
        }
    }
    *E = -J*(*E/2.0); // Dividir por 2 para nao contar repetido 
}

void magnetization_sys(int (*s)[L], double *M)
{
    /*
    Compute the total magnetization of the system

    INPUT
        int (*s)[L] : 2D array with the spin values
        double *M : total magnetization of the system
    */
    
    for(int i = 0 ; i < L ; i++)
    {
        for(int j = 0 ; j < L ; j++)
        {
            *M += s[i][j];
        }
    }
}

void metropolis(int (*s)[L], double *E, double *M, double T)
{
    /*
    Apply the Monte Carlo algorithm: Metropolis

    INPUT
        int (*s)[L] : 2D array with the spin values
        double *E : total energy of the system
        double *M : total magnetization of the system
        double *T : temperature of the system
    */

    int sn = 0, dE = 0, v = 0;
    int i, j, col, lin;
    double En = 0, Mn = 0;
    double n, boltz;

    // Lovo estado
    i = rand() % (L);
    j = rand() % (L);

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
    n = (double)rand()/(double)(RAND_MAX);
    boltz = exp(-dE/(kB*T));

    //printf("Delta E: %i n: %f boltz: %f\n", dE, n, boltz);
    
    if(dE < 0 || n < boltz)
    {
        s[i][j] = sn;
        *E += dE;
        *M += 2*sn;
    }
}

