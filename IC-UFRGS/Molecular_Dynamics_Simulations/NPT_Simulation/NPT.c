#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*** Constantes do Sistema ***/
#define T 1 // temperatura desejada
#define P 1// pressao desejada
#define N 256 // numero de particulas
#define rho 0.75 // densidade
#define dt 0.001 // passo de integracao
#define tmax 10000 // tempo maximo de simulacao
#define teq 3000 // tempo de equilibrio
#define nhis 108 // estatistica g(r)
#define nmsd 100 // estatistica msd
#define PI 3.14159

/*** Variaves Globais ***/
float x[N], y[N], z[N]; // posicoes das particulas
float x_msd[N], y_msd[N], z_msd[N]; // posicoes sem correcao de contorno
float x_0[N], y_0[N], z_0[N]; // posicoes de referencia
float vx[N], vy[N], vz[N]; // velocidades das particulas
float vx_0[N]; // velocidades de referencia
float fx[N], fy[N], fz[N]; // forcas entre as particulas
float L, temp = 1, pres = 1; // tamanho da caixa e temperatura atingida
double U = 0, etot = 0, K = 0; // energias

/*** Declaracao de Funcoes ***/
void init(float *delg);
void force(float *g, int *ngr, float delg, float t);
void chain_NH(float *xi, float *vxi, float tempc, float presc);
void integrate_NPT(float *xi, float *vxi, float tempc);
void integrate(int passo);
void gr(float delg, float *g, float *r, int ngr);
void msd(int ref, double *dr2, double *vac);

int main(){

    /*** Impressão do cabeçalho do programa ***/
    printf("\nThis is a Molecular Dynamic Simulation with Verlet Algorithm.\n");
    printf("It positions a determined number of particles in a box, calculates the forces between them and integrate these forces.\n");
    printf("It also computes the g(r) function, saving r and g(r) in a file.\n");
    printf("Energy for each step is also saved in a file.\n");
    printf("This program uses Verlet algorithm and Lennard-Jones potential.\n");
    printf("Authors: Camila Raupp and Vitoria Henkes, from Federal University of Rio Grande do Sul.\n\n");
    printf("\t|Initial Conditions|\n");
    printf("\tTemperature: %.2d\n\tNumber of particles: %d\n\tDensity: %.4f\n\tMaximum time: %.0d\n\tTime step: %.3f\n", T, N, rho, tmax, dt);

    /*** Declaracao de variaveis para calculo de g(r), msd, vac e termostato ***/
    int ngr = 0, counter_msd = 0;
    float delg;
    double dr2[nmsd] = {0}, vac[nmsd] = {0};
    float g[nhis] = {0}, r[nhis];
    float xi[2] = {0}, vxi[2] = {0};

    /*** Criacao de arquivos para salvamento de dados ***/
    // Energias
    FILE *arq_Energias;
    arq_Energias = fopen("energias.txt", "w");
    fprintf(arq_Energias, "# T U K E\n");

    // Deslocamento quadrático médio
    FILE *arq_MSD;
    arq_MSD = fopen("msd.txt", "w");
    fprintf(arq_MSD, "# T dr\n");

    // Autocorrelação das velocidades
    FILE *arq_VAC;
    arq_VAC = fopen("vac.txt", "w");
    fprintf(arq_VAC, "# T vac\n");

    // Posições
    FILE *arq_pos;

    // Temperatura
    FILE *arq_Temp = fopen("temp.txt", "w");
    fprintf(arq_Temp, "# t T\n");

    // Distribuição de Velocidades
    FILE *arq_PVel = fopen("pvel.txt", "w");
    fprintf(arq_PVel, "# vx vy vz\n");

    /*** Inicialização da caixa ***/
    init(&delg);
    force(g, &ngr, delg, 0);

    /*** Loop sobre tempo ***/
    for(int t = 1; t <= tmax; t++){

        /*** Criacao de arquivos para salvar as posições a cada 100 passos ***/
        if(t % 100 == 0)
        {
            char filename[30] = {0};
            sprintf(filename, "%s//pos%d.txt", "./posicoes", t);
            arq_pos = fopen(filename, "w");
            fprintf(arq_pos, "108\n");
            fprintf(arq_pos, "Caixa no tempo %d\n", t);
            for(int part = 0; part < N; part++)
                fprintf(arq_pos, "W %f %f %f\n", x[part], y[part], z[part]);
        }

   	    /*** Cálculo e integração das forças com termostato ***/
        chain_NH(xi, vxi, T, P);
        integrate(1);
        force(g, &ngr, delg, t);
        integrate(2);
        chain_NH(xi, vxi, T, P);

        temp = (2/3.)*(K/N);
        etot = U + K;

        /*** Deslocamento quadrado médio (Mean Square Displacement, MSD) ***/
        if(t >= teq){
            msd(t % nmsd, dr2, vac);
            counter_msd++;
        }

        /*** Impressão dos resultados em arquivos ***/
        fprintf(arq_Energias, "%d %f %f %f\n", t, U, K, etot);
        fprintf(arq_Temp, "%d %f\n", t, temp);

        /*** Impressão do tempo em execução ***/
        if(t % 100 == 0)
	      printf("\nArrived on time %d", t);

    }

    /*** Normalizacao de g(r), calculada em force ***/
    gr(delg, g, r, ngr);

    /*** Impressao do MSD e da VAC em arquivo + normalizacao ***/
    counter_msd = counter_msd/nmsd;
    printf("\nref: %i\n", counter_msd);
    for(int i = 0 ; i < nmsd ; i++)
    {
        fprintf(arq_MSD, "%d %f\n", i, dr2[i]/counter_msd);
        fprintf(arq_VAC, "%d %f\n", i, vac[i]/counter_msd);
    }

    for(int part = 0 ; part < N ; part++)
    {
        fprintf(arq_PVel, "%f %f %f\n", vx[part], vy[part], vz[part]);
    }

    /*** Fechamento dos arquivos ***/
    fclose(arq_Energias);
    fclose(arq_MSD);
    fclose(arq_pos);
    fclose(arq_VAC);

    /*** Impressao das condicoes finais ***/
    printf("\n\n|Final Conditions|");
    printf("\nPotential Energy: %.4f", U);
    printf("\nTotal Energy per Particle: %.4f", etot);
    printf("\nKinetic Energy: %.4f", K);
    printf("\nTemperature: %.4f\n", temp);

    return 0;
}

void init(float *delg){

    /*
        Funcao para posicionar as particulas em uma rede cristalina e
        designar a velocidade inicial de cada uma aleatoriamente.
        Variáveis utilizadas:
            L : tamanho da lateral da caixa
            x, y, z : arrays com as posicoes de cada particula em cada coordenada
            xm, ym, zm : arrays com as posicoes anteriores em cada coordenada
            vx, vy, vz : arrays com as velocidades em cada coordenada
            *delg : tamanho dos intervalos do histograma
    */

    /*** Definicao de variáveis ***/
    float espaco;
    int n3, part, i = 0, j = 0, k = 0;
    float sumvx = 0, sumvy = 0, sumvz = 0;
    float sumv2_x = 0, sumv2_y = 0, sumv2_z = 0;
    float sumv2 = 0, fs;

    /*** Tamanho da caixa e espacamento entre as particulas ***/
    L = cbrt((float)N/rho);
    n3 = ceil(cbrt(N));
    espaco = (float) L/n3;

    /*** Distribuicao radial da inicializacao ***/
    *delg = L/(2*nhis);

    /*** Impressao das caracteristicas da caixa ***/
    printf("\n\t|Box Characteristics|\n");
    printf("\tSide: %.4f\n\tParticles per dimension: %i\n\tSpace between sequential particles: %.4f\n", L, n3, espaco);

    /*** Inicializacao de cada particula com posicoes e velocidades ***/
    for(part = 0 ; part < N ; part++){

        x[part] = i * espaco;
        y[part] = j * espaco;
        z[part] = k * espaco;

        x_msd[part] = i * espaco;
        y_msd[part] = j * espaco;
        z_msd[part] = k * espaco;

        i++;
        if(i == n3){
            i = 0;
            j++;
            if(j == n3){
                j = 0;
                k++;
            }
        }

        // Velocidades aleatorias
        vx[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        vy[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        vz[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;

        sumvx += vx[part];
        sumvy += vy[part];
        sumvz += vz[part];

        sumv2_x += pow(vx[part], 2);
        sumv2_y += pow(vy[part], 2);
        sumv2_z += pow(vz[part], 2);
    }

    /*** Media das velocidades ***/
    sumvx /= N;
    sumvy /= N;
    sumvz /= N;

    /*** Media das velocidades quadradas ***/
    sumv2 = (sumv2_x + sumv2_y + sumv2_z)/ N;

    K = sumv2*N/2;
    temp = (2/3.)*(K/N);

    // Fator de escala das velocidades
    //fs = sqrt(3 * temp / sumv2);
    fs = sqrt(T/temp);

    // Correcao das velocidades
    for(i = 0 ; i < N ; i++){

        vx[i] = (vx[i] - sumvx) * fs;
        vy[i] = (vy[i] - sumvy) * fs;
        vz[i] = (vz[i] - sumvz) * fs;
    }
}

void force(float *g, int *ngr, float delg, float t){

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

    /*** Definição de variaveis ***/
    float xr, yr, zr;
    float rc2, ecut;
    float r2, r2i, r6i, ff;
    float r;
    int ig;

    /*** Forcas e energia nulas ***/
    double en = 0;
    for(int i = 0 ; i < N ; i++)
        fx[i] = fy[i] = fz[i] = 0;

    /*** Distância máxima de interação e potencial de Lennard-Jones ***/
    rc2 = pow(L/2, 2);
    ecut = 4 * ((1/pow(rc2, 6)) - (1/pow(rc2, 3)));

    /*** Calculo das forcas para cada par de particulas ***/
    for(int i = 0 ; i < N-1 ; i++)
    {
        for(int j = i+1 ; j < N ; j++)
        {
            // Cálculo das distâncias de um par de partículas em cada coordenada
            xr = x[i] - x[j];
            xr = xr - (L * round(xr/L));

            yr = y[i] - y[j];
            yr = yr - (L * round(yr/L));

            zr = z[i] - z[j];
            zr = zr - (L * round(zr/L));

            // Cálculo da distância total de um par de partículas
            r2 = pow(xr, 2) + pow(yr, 2) + pow(zr, 2);

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


            // Calculo da forca se r2 for menor que a distancia mínima
            if(r2 < rc2 && r2 != 0)
            {
                r2i = 1/r2;
                r6i = pow(r2i, 3);
                ff = 48 * r2i * r6i * (r6i - 0.5);

                fx[i] = fx[i] + ff * xr;
                fx[j] = fx[j] - ff * xr;

                fy[i] = fy[i] + ff * yr;
                fy[j] = fy[j] - ff * yr;

                fz[i] = fz[i] + ff * zr;
                fz[j] = fz[j] - ff * zr;

                // Atualizacao da energia potencial total
                en += (4 * r6i * (r6i - 1)) - ecut;
            }
        }
    }

    /*** Energia potencial ***/
    U = en;

    /*** Contagem de cálculos de g(r) ***/
    if((int) t >= teq)
        *ngr = *ngr + 1;
}

void chain_NH(float *xi, float *vxi, float tempc){

    double G1, G2, s; // G são acelerações na integracao do Velocity-Verlet, cada um relacionado a um termostato (Martyna1996, Eq. 25)
    float dt2, dt4, dt8;

    float Q[2] = {10, 10}; // Q1, Q2

    dt2 = dt/2;
    dt4 = dt/4;
    dt8 = dt/8;

    G2 = (Q[0]*vxi[0]*vxi[0]-tempc); //
    vxi[1] = vxi[1] + G2*dt4;
    vxi[0] = vxi[0]*exp(-vxi[1]*dt8);

    G1 = (2*K-3*N*tempc)/Q[0];
    vxi[0] += G1*dt4;
    vxi[0] = vxi[0]*exp(-vxi[1]*dt8);

    xi[0] += vxi[0]*dt2;
    xi[1] += vxi[1]*dt2;

    s = exp(-vxi[0]*dt2); // scale

    for (int i = 0; i < N; i++)
    {
        vx[i] = s*vx[i];
        vy[i] = s*vy[i];
        vz[i] = s*vz[i];
    }
    K = K*s*s;

    vxi[0] = vxi[0]*exp(-vxi[1]*dt8);
    G1 = (2*K-3*N*tempc)/Q[0];
    vxi[0] += G1*dt4;

    vxi[0] = vxi[0]*exp(-vxi[1]*dt8);
    G2 = (Q[0]*vxi[0]*vxi[0]-tempc)/Q[1];
    vxi[1] += G2*dt4;
}

void integrate_NPT(int passo, float *xi, float *vxi, float tempc){
    
    double X = 0, n = 0;
    
    switch (passo)
    {
        case 1:
            
    }
}

void integrate(int passo){

    /*
        Funcao que computa as proximas posicoes e velocidades.
        Entrada:
            U : energia potencial por partícula
            temp : temperatura do sistema
            etot : energia total do sistema (potencial + cinetica)
            K : energia cinética por partícula
            L : tamamnho da caixa
            fx, fy, fz : arrays com as forcas em cada coordenada
            x, y, z : arrays com as posicoes de cada particula em cada coordenada
            xd, yd, zd : arrays com o deslocamento real de cada particula em cada coordenada
            xm, ym, zm : arrays com as posicoes anteriores em cada coordenada
    */

    /*** Definicao de variaveis ***/
    float sumvi = 0, sumvj = 0, sumvk = 0, sumv2 = 0;
    float xx = 0, yy = 0, zz = 0;

    switch (passo)
    {
        /*** Pimeira integracao ***/
        case 1:
            K = 0.0;
            for(int i = 0 ; i < N ; i++){
                // Calculo do deslocamento de meio intervalo
                xx = vx[i]*dt/2;
                yy = vy[i]*dt/2;
                zz = vz[i]*dt/2;

                // Calculo das proximas posicoes na metade do intervalo com contorno
                x[i] += xx;
                y[i] += yy;
                z[i] += zz;

                // Calculo das proximas posicoes na metade do intervalo sem contorno
                x_msd[i] += xx;
                y_msd[i] += yy;
                z_msd[i] += zz;

                // Condicao de contorno
                x[i] = x[i] - floor(x[i]/L)*L;
                y[i] = y[i] - floor(y[i]/L)*L;
                z[i] = z[i] - floor(z[i]/L)*L;

                }
            break;
        /*** Segunda integracao ***/
        case 2:
            for(int i = 0 ; i < N ; i++){
                // Calculo das proximas velocidades
                vx[i] += fx[i]*dt;
                vy[i] += fy[i]*dt;
                vz[i] += fz[i]*dt;

                // Calculo do deslocamento
                xx = vx[i]*dt/2;
                yy = vy[i]*dt/2;
                zz = vz[i]*dt/2;

                // Calculo das proximas posicoes com contorno
                x[i] += xx;
                y[i] += yy;
                z[i] += zz;

                // Calculo das proximas posicoes sem contorno
                x_msd[i] += xx;
                y_msd[i] += yy;
                z_msd[i] += zz;

                sumvi += vx[i];
                sumvj += vy[i];
                sumvk += vz[i];
                sumv2 += (pow(vx[i], 2) + pow(vy[i], 2) + pow(vz[i], 2));
                }

            // O centro de massa nao pode se mover
            if((-1 > sumvi || sumvi > 1) || (-1 > sumvj || sumvj > 1) || (-1 > sumvk || sumvk > 1))
                printf("\nATENCAO: A velocidade do centro de massa e diferente de zero.\nVi = %f Vj = %f Vk = %f\n", sumvi, sumvj, sumvk);

            // Calculo da energia cinetica do sistema

            K = 0.5*sumv2;

            break;
    }
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
        nid = (4/3) * PI * vb * rho; // Número de partículas
        g[i] = g[i]/(ngr * N * nid); // Normalização da g(r)

        fprintf(arq_Gr, "%f %f\n", g[i], r[i]);
    }

    fclose(arq_Gr);
}

void msd(int ref, double *dr2, double *vac){

    /*
        Função que calcula o deslocamento quadrático médio das partículas
        Entrada:
            ref : tempo de referência para cada amostra
            *dr2 : array para armazenar o msd em cada instante de tempo
            xd, yd, zd : arrays com o deslocamento de cada particula em cada coordenada
            x_0, y_0, z_0 : arrays com as posições iniciais de cada particula em cada coordenada
    */

    // Se estiver em um tempo de referência, guarda as posições
    if(ref == 0){
        for(int part = 0 ; part < N ; part++){
            x_0[part] = x_msd[part];
            y_0[part] = y_msd[part];
            z_0[part] = z_msd[part];

            vx_0[part] = vx[part];}
    }
    // Caso contrário, calcula o MSD
    else if(ref > 0){
        for(int part = 0 ; part < N ; part++){
            // Aculumula o MSD de cada partícula
            dr2[ref] += pow((x_msd[part]-x_0[part]), 2) + pow((y_msd[part]-y_0[part]), 2) + pow((z_msd[part]-z_0[part]), 2);
            vac[ref] += vx[part]*vx_0[part];
        }

    // Normalização do MSD
    dr2[ref] /= N;
    vac[ref] /= N;
    }
}
