#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*** Constantes do Sistema ***/
#define rho 0.75 //Densidade
#define N 256 //Numeros de particulas
#define T0 1.0
#define teq 4000
#define TEMPO_MAX 10000 //Tempo de simula��o
#define nhis 108 // estatistica g(r)
#define nmsd 100 // estatistica msd
#define PI 3.14159

/*********VARIAVEIS GLOBAIS******************/
double x[N],y[N],z[N];
double x_msd[N], y_msd[N], z_msd[N]; // posicoes sem correcao de contorno
double x_0[N], y_0[N], z_0[N]; // posicoes de referencia
double vx[N],vy[N],vz[N];
double vx_0[N], vy_0[N], vz_0[N]; // velocidades de referencia
double fx[N],fy[N],fz[N];
double uk,pe; // Energia cinetica e potencial
double T;
double et, et0, r2;

/*********CONSTANTES GLOBAIS #2******************/
double l=3*N;// Variaveis reais - Frenkel --> L=3N
double L;
double delt=0.0002, delt2, delt4, delt8;
double To = 1.0;//Temperatura de interesse

/********************FUN��ES*********************/
//void init(float *delg);
//void force(void);
//void integrate(int passo);
//void chain(double *xi, double *vxi, double T);

/********************************************/

/****INICIAR AS POSICOES E VELOCIDADES********/
void init (float *delg)
/*******************************************/
{
    double sumvx = 0.0, sumvy = 0.0, sumvz = 0.0;
    double fac, espaco;
    int n3;

    /** Tamanho da caixa e espacamento entre as particulas **/
    L = cbrt((float)N/rho);
    n3 = ceil(cbrt(N));
    espaco = (float) L/n3;
    
    /*** Distribuicao radial da inicializacao ***/
    *delg = L/(2*nhis);

    /** Impressao das caracteristicas da caixa **/
    printf("\n\t|Box Characteristics|\n");
    printf("\tSide: %.4f\n\tParticles per dimension: %i\n\tSpace between sequential particles: %.4f\n", L, n3, espaco);

    /** Inicializacao de cada particula com posicoes e velocidades **/
    for (int i = 0; i < N; i++)
    {
        x[i] = (i%n3) * espaco;
        y[i] = ((i/n3)%n3) * espaco;
        z[i] = ((i/(n3*n3))%n3) * espaco;

        vx[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        vy[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        vz[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;

        sumvx += vx[i];
        sumvy += vy[i];
        sumvz += vz[i];
        
        vx[i] -= sumvx/N;
        vy[i] -= sumvy/N;
        vz[i] -= sumvz/N;
        
        uk += (vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])/2;
    }
    /** Correcao de escala se temperatura inicial for maior que 0 **/
    if (T0 > 0.0)
    {

        T = (2*uk)/(3*N);
        fac = sqrt(T0/T);

        for (int i = 0; i < N; i++)
        {
            vx[i] *= fac;
            vy[i] *= fac;
            vz[i] *= fac;

            uk += (vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])/2;
        }
    }    
 }

/*********CALCULAR FORCAS******************/
void force(float *g, int *ngr, float delg, float t)
{
    /*
        Funcao para calcular as forcas entre cada particula a partir do potencial de Lennard-Jones
        e a energia potencial.

        Entrada:

            fx, fy, fz : arrays com as forcas em cada coordenada
            U : energia potencial total por partícula
            x, y, z : arrays com as posicoes de cada particula em cada coordenada
            L : tamanho da lateral da caixa
            *g : array da distribuição radial
            *ngr = número de cálculos de g(r)
            delg : tamanho dos intervalos do histograma
    */

    double dx, dy, dz, r2i, r6i;
    double ff, rc, rc2;
    double ecut;
    double r;
    int ig;

    /** Distância máxima de interação e potencial de Lennard-Jones **/
    rc = L/2;
    rc2 = rc*rc;
    ecut = 4*((1/pow(rc2, 6)) - (1/pow(rc2, 3)));

    /** Forcas e energia nulas **/
    pe = 0.0;
    for (int i = 0; i < N; i++)
        fx[i] = fy[i] = fz[i] = 0.0;

    /** Calculo das forcas para cada par de particulas **/
    for (int i = 0; i < (N-1); i++)
    {
        for (int j = i+1; j < N; j++)
        {

            dx  = (x[i] - x[j]);
            dy  = (y[i] - y[j]);
            dz  = (z[i] - z[j]);

            dx = dx - round(dx/L)*L;
            dy = dy - round(dy/L)*L;
            dz = dz - round(dz/L)*L;

            r2 = dx*dx + dy*dy + dz*dz;

            // Distribuição Radial
            if((int)t >= teq)
            {
                r = sqrt(r2);

                if(r < L/2)
                {
                    ig = (int) (r/delg);
                    g[ig] += 2;
                }
            }

            if (r2 < rc2)
            {

                r2i = 1.0/r2;
                r6i  = r2i*r2i*r2i;
                ff = 48.0*r6i*r2i*(r6i-0.5);

                fx[i] += dx*ff;
                fx[j] -= dx*ff;

                fy[i] += dy*ff;
                fy[j] -= dy*ff;

                fz[i] += dz*ff;
                fz[j] -= dz*ff;

                pe += 4.0 * r6i * (r6i - 1.0) - ecut;
            }
        }
    }
    
    /*** Contagem de cálculos de g(r) ***/
    if((int) t >= teq)
        *ngr = *ngr + 1;
}
/*******************************************/
void integrate (int passo)
/*******************************************/
{
    switch(passo)
    {
        case 1:
            uk = 0.0;
            for (int i = 0; i < N; i++)
            {
                x[i] += vx[i]*delt2;
                y[i] += vy[i]*delt2;
                z[i] += vz[i]*delt2;

                x[i] -= floor(x[i]/L)*L;
                y[i] -= floor(y[i]/L)*L;
                z[i] -= floor(z[i]/L)*L;
            }
            break;
        case 2:
            for (int i=0;i<N;i++)
            {
                vx[i] += delt*fx[i];
                vy[i] += delt*fy[i];
                vz[i] += delt*fz[i];

                x[i] += vx[i]*delt2;
                y[i] += vy[i]*delt2;
                z[i] += vz[i]*delt2;

                uk += (vx[i]*vx[i]+vy[i]*vy[i]+vz[i]*vz[i])/2;
            }
    }
}
/*******************************************/

void chain (double *xi, double *vxi, double T)
/*******************************************/
{

    double G1, G2, s;
    float Q[2] = {10, 10}; // Q1, Q2

    delt2 = delt/2;
    delt4 = delt/4;
    delt8 = delt/8;

    G2 = (Q[0]*vxi[0]*vxi[0]-T);
    vxi[1] = vxi[1] + G2*delt4;
    vxi[0] = vxi[0]*exp(-vxi[1]*delt8);

    G1 = (2*uk-l*T)/Q[0];
    vxi[0] = vxi[0] + G1*delt4;
    vxi[0] = vxi[0]*exp(-vxi[1]*delt8);

    xi[0] = xi[0] + vxi[0]*delt2;
    xi[1] = xi[1] + vxi[1]*delt2;

    s = exp(-vxi[0]*delt2);

    for (int i=0;i<N;i++)
    {
    vx[i] = s*vx[i];
    vy[i] = s*vy[i];
    vz[i] = s*vz[i];

    }
    uk = uk*s*s;

    vxi[0] = vxi[0]*exp(-vxi[1]*delt8);
    G1 = (2*uk-l*T)/Q[0];
    vxi[0] = vxi[0] + G1*delt4;

    vxi[0] = vxi[0]*exp(-vxi[1]*delt8);
    G2 = (Q[0]*vxi[0]*vxi[0]-T)/Q[1];
    vxi[1] = vxi[1] + G2*delt4;
}

void gr(float delg, float *g, float *r, int ngr){

    /*
        Função que normaliza a distribuição radial, g(r).

        Entrada:
            *delg : tamanho dos intervalos do histograma
            *g : array distribuição radial
            *r : raio da região contabilizada
            *ngr : número de cálculos de g(r)
    */

    float vb, nid;

    FILE *arq_Gr;
    arq_Gr = fopen("g_r.txt", "w");
    fprintf(arq_Gr, "g  r\n");

    for(int i = 0; i < nhis; i++)
    {

        r[i] = delg*(i + 0.5); // Distância do raio
        vb = (pow(i+1, 3) - pow(i, 3))*pow(delg, 3); // Volume da esfera avaliada
        nid = (4/3.) * PI * vb * rho; // Número de partículas
        g[i] = g[i]/(ngr * N * nid); // Normalização da g(r)

        fprintf(arq_Gr, "%f %f\n", g[i], r[i]);
    }

    fclose(arq_Gr);
}

/*******************************************/
int main ( void )
/*******************************************/
{
    /** Criacao de arquivos para salvamento de dados **/

    // Energias
    FILE *arq_Energias;
    arq_Energias = fopen("energias.txt", "w");
    fprintf(arq_Energias, "# t U K E\n");

    // Temperatura
    FILE *arq_Temp;
    arq_Temp = fopen("temperaturas.txt", "w");
    fprintf(arq_Temp, "# t T\n");

    // Posicoes e Velocidades
    FILE *arq_pos;
    FILE *arq_vel;

    // Declaracao de variaveis
    int ngr = 0;
    float delg;
    float g[nhis] = {0}, r[nhis];
    double dr2[nmsd] = {0}, vac[nmsd] = {0};
    double xi[2] = {0}, vxi[2] = {0};

    init(&delg);
    force(g, &ngr, delg, 0);

    for (int t = 1; t <= TEMPO_MAX; t++)
    {
        /** Impressao de resultados em arquivos **/
        if(t % 100 == 0) // salva as posicoes a cada 100 passos
        {
            char filename[30] = {0};
            sprintf(filename, "%s//pos%d.txt", "./posicoes", t);
            arq_pos = fopen(filename, "w");
            fprintf(arq_pos, "256\n");
            fprintf(arq_pos, "Caixa no tempo %d\n", t);
            for(int part = 0; part < N; part++)
                fprintf(arq_pos, "W %f %f %f\n", x[part], y[part], z[part]);
        }
        if(t == 9900) // salva as velocidades em tempo determinado
        {
            char filename[30] = {0};
            sprintf(filename, "velocidades%d.txt", t);
            arq_vel = fopen(filename, "w");
            fprintf(arq_vel, "vx vy vz\n");
            for(int part = 0; part < N; part++)
                fprintf(arq_vel, "%f %f %f\n", vx[part], vy[part], vz[part]);
        }

        /** Impressao de resultados em arquivos **/
        fprintf(arq_Energias, "%d %f %f %f\n", t, pe, uk, et);
        fprintf(arq_Temp, "%d %f\n", t, T);
        
        chain(xi, vxi, To);
        integrate(1);
        force(g, &ngr, delg, t);
        integrate(2);
        chain(xi, vxi, To);

        T = (2/3.)*(uk/N);
        et = pe + uk;

        /** Impressao do tempo em execucao **/
        if(t % 1000 == 0)
	      printf("\nArrived on time %d", t);
    }
    
    /*** Normalizacao da g(r) calculada em force ***/
    gr(delg, g, r, ngr);

    /** Fechamento dos arquivos **/
    fclose(arq_Energias);
    fclose(arq_Temp);
    fclose(arq_pos);
    fclose(arq_vel);

    /** Impressao das condicoes finais **/
    printf("\n\n|Final Conditions|");
    printf("\nPotential Energy: %.4f", pe);
    printf("\nTotal Energy per Particle: %.4f", et);
    printf("\nKinetic Energy: %.4f", uk);
    printf("\nTemperature: %.4f\n", T);

    return 0;
}
