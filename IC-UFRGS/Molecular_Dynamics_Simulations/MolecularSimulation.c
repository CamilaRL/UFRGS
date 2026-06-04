#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Dados do sistema
#define t0 0.728
#define N 108
#define rho 0.8442
// Passos de tempo, tempo máximo e tempo de equilibrio
#define dt 0.001
#define dtef 0.01 // passo utilizado para testes
#define tmax 1/dt
#define teq 800
// Estatistica g(r)
#define nhis 108
// Estatistica msd
#define nmsd 1000
// Constantes
#define PI 3.14159


void init(float *L, float *x, float *y, float *z,
            float *x_msd, float *y_msd, float *z_msd,
            float *v_x, float *v_y, float *v_z, float *delg);
void force(float *fx, float *fy, float *fz,
            double *U, float *x, float *y, float *z,
            float L, float *g, int *ngr, float delg, float t);
void integrate(int verlet, double U, float *temp, double *etot,
                double *k, float L,
                float *fx, float *fy, float *fz,
                float *x, float *y, float *z,
                float *x_msd, float *y_msd, float *z_msd,
                float *v_x, float *v_y, float *v_z);
void gr(float delg, float *g, float *r, int ngr);
void msd(int ref, double *dr2, double *vac,
            float *x, float *y, float *z,
            float *x0, float *y0, float *z0,
            float *v_x, float *v_y, float *v_z,
            float *v_x0, float *v_y0, float *v_z0);


int main(){

    //Número de passos analisados
    int nsteps = (int) tmax/dtef;

    //Definição dos vetores de posições, velocidades e forças
    float x[N], y[N], z[N];
    float x_msd[N], y_msd[N], z_msd[N];
    float x0[N], y0[N], z0[N];
    float v_x[N], v_y[N], v_z[N];
    float v_x0[N], v_y0[N], v_z0[N];
    float fx[N], fy[N], fz[N];

    //Definição de variáveis
    float L, temp, delg, t = 0;
    int ngr = 0, ref = 0;
    double U = 0, etot = 0, k = 0;
    double dr2[nmsd] = {0}, vac[nmsd] = {0};
    float g[nhis] = {0}, r[nhis], time[nsteps];

    //Criação de arquivo para salvar energias
    FILE *arq_Energias;
    arq_Energias = fopen("energias.txt", "w");
    fprintf(arq_Energias, "# T U K E\n");

    //Criação de arquivo para salvar deslocamento quadrático médio
    FILE *arq_MSD;
    arq_MSD = fopen("msd.txt", "w");
    fprintf(arq_MSD, "# T dr\n");

    // Criação de arquivo para salvar a autocorrelação das velocidades
    FILE *arq_VAC;
    arq_VAC = fopen("vac.txt", "w");
    fprintf(arq_VAC, "# T vac\n");

    //Criação de arquivo para salvar as posições
    FILE *arq_pos;

    //Impressão do cabeçalho do programa
    printf("\nThis is a Molecular Dynamic Simulation with Verlet Algorithm.\n");
    printf("It positions a determined number of particles in a box, calculates the forces between them and integrate these forces.\n");
    printf("It also computes the g(r) function, saving r and g(r) in a file.\n");
    printf("Energy for each step is also saved in a file.\n");
    printf("This program uses Verlet algorithm and Lennard-Jones potential.\n");
    printf("Authors: Camila Raupp and Vitoria Henkes, from Federal University of Rio Grande do Sul.\n\n");
    printf("\t|Initial Conditions|\n");
    printf("\tTemperature: %.3f\n\tNumber of particles: %d\n\tDensity: %.4f\n\tMaximum time: %.0f\n\tTime variation: %.3f\n\tEffective time variation: %.3f\n", t0, N, rho, tmax, dt, dtef);

    //Inicialização da caixa
    init(&L, x, y, z, x_msd, y_msd, z_msd, v_x, v_y, v_z,  &delg);
    force(fx, fy, fz, &U, x, y, z, L, g, &ngr, delg, t);

    //Loop sobre tempo
    for(int step = 0 ; step < nsteps ; step++)
    {
	//Instantes de tempo analisdos
        time[step] = t;

        // Arquivo para salvar as posições a cada 100 passos
        if(step % 1000 == 0)
        {
            char filename[30] = {0};
            sprintf(filename, "%s//pos%d.txt", "./posicoes", (int)(step*dtef));
            arq_pos = fopen(filename, "w");
            fprintf(arq_pos, "108\n");
            fprintf(arq_pos, "Caixa no tempo %d\n", (int)t);
            //Salvamento das posições iniciais em um arquivo
            for(int part = 0; part < N ; part++)
            {
                fprintf(arq_pos, "W %f %f %f\n", x[part], y[part], z[part]);
            }
        }

   	    //Cálculo e integração das forças
        integrate(1, U, &temp, &etot, &k , L, fx, fy, fz, x, y, z, x_msd, y_msd, z_msd, v_x, v_y, v_z);
        force(fx, fy, fz, &U, x, y, z, L, g, &ngr, delg, t);
        integrate(2, U, &temp, &etot, &k , L, fx, fy, fz, x, y, z, x_msd, y_msd, z_msd, v_x, v_y, v_z);

        //Deslocamento quadrado médio (Mean Square Displacement, MSD)
        if(step >= teq/dtef){
            msd(step % nmsd, dr2, vac, x_msd, y_msd, z_msd, x0, y0, z0, v_x, v_y, v_z, v_x0, v_y0, v_z0);
            ref++;
        }

        //Impressão dos resultados em arquivos
        fprintf(arq_Energias, "%f %f %f %f\n", time[step], U, k, etot);

        //Impressão do tempo em execução
        if(step % (int)(100/dtef) == 0)
	      printf("\nArrived on time %.0f", t);

        //Contabilização de passos percorridos
        t += dtef;
    }

    //Normalização de g(r), calculada em force
    gr(delg, g, r, ngr);

    //Impressão do MSD e da VAC em arquivo + normalizaçaõ
    ref = ref/nmsd;
    printf("\nref: %i\n", ref);
    for(int i = 0 ; i < nmsd ; i++)
    {
        fprintf(arq_MSD, "%f %f\n", i*dtef, dr2[i]/ref);
        fprintf(arq_VAC, "%f %f\n", i*dtef, vac[i]/ref);
    }

    //Fechamento dos arquivos
    fclose(arq_Energias);
    fclose(arq_MSD);
    fclose(arq_pos);
    fclose(arq_VAC);

    //Impressão das condições de equílibrio (final)
    printf("\n\n|Final Conditions|");
    printf("\nPotential Energy: %.4f", U);
    printf("\nTotal Energy per Particle: %.4f", etot);
    printf("\nKinetic Energy: %.4f", k);
    printf("\nTemperature: %.4f\n", temp);

    return 0;
}

void init(float *L, float *x, float *y, float *z,
            float *x_msd, float *y_msd, float *z_msd,
            float *v_x, float *v_y, float *v_z, float *delg){

    /*
        Funcao para posicionar as particulas em uma rede cristalina e
        designar a velocidade inicial de cada uma aleatoriamente.

        Entrada:
            *L : tamanho da lateral da caixa
            *x, *y, *z : arrays com as posicoes de cada particula em cada coordenada
            *xm, *ym, *zm : arrays com as posicoes anteriores em cada coordenada
            *v_x, *v_y, *vz : arrays com as velocidades em cada coordenada
            *g : array da distribuição radial
            *delg : tamanho dos intervalos do histograma
    */

    // Definicao de variáveis
    float espaco;
    int n3, part, i = 0, j = 0, k = 0;
    float sumv_x = 0, sumv_y = 0, sumv_z = 0;
    float sumv2_x = 0, sumv2_y = 0, sumv2_z = 0;
    float sumv2 = 0, fs;

    // Tamanho da caixa e espacamento entre as particulas
    *L = cbrt((float)N/rho);
    n3 = ceil(cbrt(N));
    espaco = (float) *L/n3;

    // Distribuicao Radial da Inicializacao
    *delg = *L/(2*nhis);

    printf("\n\t|Box Characteristics|\n");
    printf("\tSide: %.4f\n\tParticles per dimension: %i\n\tSpace between sequential particles: %.4f\n", *L, n3, espaco);

    // Inicializacao de cada particula com posicoes e velocidades
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
        v_x[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        v_y[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
        v_z[part] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;

        sumv_x += v_x[part];
        sumv_y += v_y[part];
        sumv_z += v_z[part];

        sumv2_x += pow(v_x[part], 2);
        sumv2_y += pow(v_y[part], 2);
        sumv2_z += pow(v_z[part], 2);
    }

    // Media das velocidades
    sumv_x /= N;
    sumv_y /= N;
    sumv_z /= N;

    // Media das velocidades quadradas
    sumv2 = (sumv2_x + sumv2_y + sumv2_z)/ N;

    // Fator de escala das velocidades
    fs = sqrt(3 * t0 / sumv2);

    // Correcao das velocidades
    for(i = 0 ; i < N ; i++){

        v_x[i] = (v_x[i] - sumv_x) * fs;
        v_y[i] = (v_y[i] - sumv_y) * fs;
        v_z[i] = (v_z[i] - sumv_z) * fs;
    }
}

void force(float *fx, float *fy, float *fz, double *U,
            float *x, float *y, float *z, float L,
            float *g, int *ngr, float delg, float t){

    /*
        Funcao para calcular as forcas entre cada particula a partir do potencial de Lennard-Jones
        e a energia potencial.

        Entrada:

            *fx, *fy, *fz : arrays com as forcas em cada coordenada
            *U : energia potencial total por partícula
            *x, *y, *z : arrays com as posicoes de cada particula em cada coordenada
            L : tamanho da lateral da caixa
            *g : array da distribuição radial
            *ngr = número de cálculos de g(r)
            delg : tamanho dos intervalos do histograma
            e : instante de iteração do loop externo
    */

    // Definição de variaveis
    float xr, yr, zr;
    float rc2, ecut;
    float r2, r2i, r6i, ff;
    float r;
    int ig;

    // Forcas e energias nulas
    double en = 0;

    for(int i = 0 ; i < N ; i++)
    {
        fx[i] = fy[i] = fz[i] = 0;
    }

    // Distância máxima de interação e potencial de Lennard-Jones
    rc2 = pow(L/2, 2);
    ecut = 4 * ((1/pow(rc2, 6)) - (1/pow(rc2, 3)));

    // Calculo das forcas para cada par de particulas
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
            if((int) t >= teq) // Iteração a partir da qual o sistema já estabilizou
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
    // Energia potencial por partícula
    *U = en/N;

    // Contagem de cálculos de g(r)
    if((int) t >= teq)
        *ngr = *ngr + 1;
}

void integrate(int verlet, double U, float *temp, double *etot,
                double *k, float L,
                float *fx, float *fy, float *fz,
                float *x, float *y, float *z,
                float *x_msd, float *y_msd, float *z_msd,
                float *v_x, float *v_y, float *v_z){

    /*
        Funcao que computa as proximas posicoes e velocidades.

        Entrada:
            U : energia potencial por partícula
            *temp : temperatura do sistema
            *etot : energia total do sistema (potencial + cinetica)
            *k : energia cinética por partícula
            L : tamamnho da caixa
            *fx, *fy, *fz : arrays com as forcas em cada coordenada
            *x, *y, *z : arrays com as posicoes de cada particula em cada coordenada
            *xd, *yd, *zd : arrays com o deslocamento real de cada particula em cada coordenada
            *xm, *ym, *zm : arrays com as posicoes anteriores em cada coordenada
    */

    // Definicao de variaveis
    float sumvi = 0, sumvj = 0, sumvk = 0, sumv2 = 0;
    float xx, yy, zz;

    switch (verlet)
    {
        // Pimeira integracao
        case 1:
            for(int i = 0 ; i < N ; i++){
                // Calculo do deslocamento
                xx = v_x[i]*dt + 0.5*fx[i]*pow(dt, 2);
                yy = v_y[i]*dt + 0.5*fy[i]*pow(dt, 2);
                zz = v_z[i]*dt + 0.5*fz[i]*pow(dt, 2);

                // Calculo das proximas posicoes com contorno
                x[i] += xx;
                y[i] += yy;
                z[i] += zz;

                // Calculo das proximas posicoes sem contorno
                x_msd[i] += xx;
                y_msd[i] += yy;
                z_msd[i] += zz;

                // Calculo das velocidades no meio do intervalo
                v_x[i] += 0.5*fx[i]*dt;
                v_y[i] += 0.5*fy[i]*dt;
                v_z[i] += 0.5*fz[i]*dt;

                // Condicao de contorno
                x[i] = x[i] - floor(x[i]/L)*L;
                y[i] = y[i] - floor(y[i]/L)*L;
                z[i] = z[i] - floor(z[i]/L)*L;}
            break;
        // Segunda integracao
        case 2:
            for(int i = 0 ; i < N ; i++){
                // Calculo das velocidades no fim do intervalo
                v_x[i] += 0.5*fx[i]*dt;
                v_y[i] += 0.5*fy[i]*dt;
                v_z[i] += 0.5*fz[i]*dt;

                sumvi += v_x[i];
                sumvj += v_y[i];
                sumvk += v_z[i];
                sumv2 += pow(v_x[i], 2) + pow(v_y[i], 2) + pow(v_z[i], 2);}

            // O centro de massa nao pode se mover
            if((-1 > sumvi || sumvi > 1) || (-1 > sumvj || sumvj > 1) || (-1 > sumvk || sumvk > 1))
            printf("\nATENCAO: A velocidade do centro de massa e diferente de zero.\nVi = %f Vj = %f Vk = %f\n", sumvi, sumvj, sumvk);

            // Calculo da temperatura e energia total do sistema
            *temp = sumv2/(3*N);
            *k = 0.5*sumv2/N;
            *etot = U + *k;
            break;
    }
}

void gr(float delg, float *g, float *r, int ngr){

    /*
        Função que normaliza a distribuição radial, g(r).

        Entrada:
            delg : tamanho dos intervalos do histograma
            *g : array distribuição radial
            *r : raio da região contabilizada
            *ngr : número de cálculos de g(r)
    */

    float vb, nid;

    FILE *arq_Gr;
    arq_Gr = fopen("g_r.txt", "w");

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

void msd(int ref, double *dr2, double *vac,
            float *x, float *y, float *z,
            float *x0, float *y0, float *z0,
            float *v_x, float *v_y, float *v_z,
            float *v_x0, float *v_y0, float *v_z0){

    /*
        Função que calcula o deslocamento quadrático médio das partículas

        Entrada:
            ref : tempo de referência para cada amostra
            *dr2 : array para armazenar o msd em cada instante de tempo
            *xd, *yd, *zd : arrays com o deslocamento de cada particula em cada coordenada
            *x0, *y0, *z0 : arrays com as posições iniciais de cada particula em cada coordenada
    */

    // Se estiver em um tempo de referência, guarda as posições
    if(ref == 0){
        for(int part = 0 ; part < N ; part++){
            x0[part] = x[part];
            y0[part] = y[part];
            z0[part] = z[part];

            v_x0[part] = v_x[part];
            v_y0[part] = v_y[part];
            v_z0[part] = v_z[part];}
    }
    // Caso contrário, calcula o MSD
    else if(ref > 0){
        for(int part = 0 ; part < N ; part++){
            // Aculumula o MSD de cada partícula
            dr2[ref] += pow((x[part]-x0[part]), 2) + pow((y[part]-y0[part]), 2) + pow((z[part]-z0[part]), 2);
            vac[ref] += v_x[part]*v_x0[part];
        }

    // Normalização do MSD
    dr2[ref] /= N;
    vac[ref] /= N;
    }
}
