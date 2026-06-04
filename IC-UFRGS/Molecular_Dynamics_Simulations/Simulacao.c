#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define t0 0.728
#define N 108
#define rho 0.8442
#define dt 0.001
#define tmax 1/dt
#define nhis 108
#define PI 3.14159

void init(float *L, float *x, float *y, float *z,
            float *xm, float *ym, float *zm,
            float *v_x, float *v_y, float *v_z,
            int *g, float *delg);
void force(float *fx, float *fy, float *fz,
            double *U, float *x, float *y, float *z, 
            float L, float *g, int *ngr, float delg, int e);
void integrate(double U, float *temp, double *etot, double *k, float L,
                float *fx, float *fy, float *fz,
                float *x, float *y, float *z,
                float *xm, float *ym, float *zm);
void gr(float delg, float *g, double *r, int ngr);

int main(){

    // Declaracao de variaveis
    float x[N], y[N], z[N];
    float xm[N], ym[N], zm[N];
    float v_x[N], v_y[N], v_z[N];
    float fx[N], fy[N], fz[N];
    float L, temp;
    double U = 0, etot = 0, k = 0;
    int ngr = 0;
    float delg, g[nhis], r[nhis];

    FILE *arq_Energias;
    arq_Energias = fopen("energias.txt", "w");
    fprintf(arq_Energias, "# U K E\n");

    printf("\n\tCondicoes Iniciais\n");
    printf("\tt0: %f\n\tN: %d\n\trho: %fn\ttmax: %f\n\tdt: %f\n", t0, N, rho, tmax, dt);


    init(&L, x, y, z, xm, ym, zm, v_x, v_y, v_z, g, &delg);
    
    for(float i = 0 ; i < tmax ; i = i + 0.01)
    {
        force(fx, fy, fz, &U, x, y, z, L, g, &ngr, delg, i);
        integrate(U, &temp, &etot, &k , L, fx, fy, fz, x, y, z, xm, ym, zm);
        fprintf(arq_Energias, "%f %f %f\n", U, k, etot);
    }

    gr(delg, g, r, ngr);
    printf("ngr: %d\n", ngr);
    
    fclose(arq_Energias);    
/*
    for(int i = 0 ; i<N; i++){
        printf("\nParticula %d\n", i);
        printf(" x: %f y: %f z: %f\n", x[i], y[i], z[i]);
        printf(" vx: %f vy: %f vz: %f\n", v_x[i], v_y[i], v_z[i]);
        printf(" fx: %f fy: %f fz: %f\n", fx[i], fy[i], fz[i]);
    }
*/
    printf("\nEnergia Potencial: %f", U);
    printf("\nEnergia Total por Particula: %f", etot);
    printf("\nEnergia Cinetica: %f", k);
    printf("\nTemperatura: %f\n", temp);

    return 0;
}

void init(float *L, float *x, float *y, float *z,
            float *xm, float *ym, float *zm,
            float *v_x, float *v_y, float *v_z, int *g, float *delg){
    
    /*
        Funcao para posicionar as particulas em uma rede cristalina e
        designar a velocidade inicial de cada uma aleatoriamente.

        Entrada:
            L = tamanho da lateral da caixa
            x, y, z = arrays com as posicoes de cada particula em cada coordenada
            xm, ym, zm = arrays com as posicoes anteriores em cada coordenada
            v_x, v_y, vz = arrays com as velocidades em cada coordenada
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
    for(int n = 0 ; n < nhis ; n++)
    {
        g[n] = 0;
    }

    printf("\n\tCaracteristicas da caixa\n");
    printf("\tL: %f\n\tn3: %i\n\tespaco: %f\n", *L, n3, espaco);

    // Inicializacao de cada particula com posicoes e velocidades
    for(part = 0 ; part < N ; part++){

        x[part] = i * espaco;
        y[part] = j * espaco;
        z[part] = k * espaco;

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

        // Posicao anterior conforme a conservacao de momentum
        xm[i] = x[i] - (v_x[i] * dt);
        ym[i] = y[i] - (v_y[i] * dt);
        zm[i] = z[i] - (v_z[i] * dt);
    } 

}

void force(float *fx, float *fy, float *fz,
            double *U, float *x, float *y, float *z, 
            float L, float *g, int *ngr, float delg, int e){
    
    /*
        Funcao para calcular as forcas entre cada particula a partir do potencial de Lennard-Jones 
        e a energia potencial.

        Entrada:
            L = tamanho da lateral da caixa
            x, y, z = arrays com as posicoes de cada particula em cada coordenada
            fx, fy, fz = arrays com as forcas em cada coordenada
            U = energia potencial total
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
            if(e >= 800)
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
    if(e >= 800)
        *ngr = *ngr + 1;
}

void integrate(double U, float *temp, double *etot, double *k, float L,
                float *fx, float *fy, float *fz,
                float *x, float *y, float *z,
                float *xm, float *ym, float *zm){

    /*
        Funcao que computa as proximas posicoes e velocidades.

        Entrada:
            en = energia potencial total
            temp = temperatura do sistema
            etot = energia total do sistema (potencial + cinetica)
            fx, fy, fz = arrays com as forcas em cada coordenada
            x, y, z = arrays com as posicoes de cada particula em cada coordenada
            xm, ym, zm = arrays com as posicoes anteriores em cada coordenada
    */

    // Definicao de variaveis
    float sumvi = 0, sumvj = 0, sumvk = 0, sumv2 = 0;
    float xx = 0, yy = 0, zz = 0;
    float vi, vj, vk;

    for(int i = 0 ; i < N ; i++){

        // Calculo das proximas posicoes e velocidades
        xx = (2*x[i]) - xm[i] + (pow(dt, 2) * fx[i]);
        //printf("%f", xx);
        xx = xx - (L * round(xx/L));
        //printf("    %f\n", xx);
        vi = (xx - xm[i]) / (2*dt);
        
        yy = (2*y[i]) - ym[i] + (pow(dt, 2) * fy[i]);
        yy = yy - (L * round(yy/L));
        vj = (yy - ym[i]) / (2*dt);

        zz = (2*z[i]) - zm[i] + (pow(dt, 2) * fz[i]);
        zz = zz - (L * round(zz/L));
        vk = (zz - zm[i]) / (2*dt);

        sumvi += vi;
        sumvj += vj;
        sumvk += vk;
        sumv2 += pow(vi, 2) + pow(vj, 2) + pow(vk, 2);

        // Atualizacao das posicoes
        xm[i] = x[i];
        x[i] = xx;

        ym[i] = y[i];
        y[i] = yy;

        zm[i] = z[i];
        z[i] = zz;
    }

    // O centro de massa nao pode se mover
    //if((-0.5 < sumvi && sumvi < 0.5) || (-0.5 < sumvj && sumvj < 0.5) || (-0.5 < sumvk && sumvk < 0.5))
       //printf("\nATENCAO: A velocidade do centro de massa e diferente de zero.\nVi = %f Vj = %f Vk = %f\n", sumvi, sumvj, sumvk);

    // Calculo da temperatura e energia total do sistema
    *temp = sumv2/(3*N);
    *k = 0.5*sumv2/N;
    *etot = U + *k;
}

void gr(float delg, float *g, double *r, int ngr){

    /*
        Função que normaliza a distribuição radial, g(r).

        Entrada:
            delg = tamanho dos intervalos do histograma
            g* = distribuição radial
            *r = raio da região contabilizada
            *ngr = número de cálculos de g(r)
    */

    float vb, nid;

    FILE *arq_Gr;
    arq_Gr = fopen("g(r).txt", "w");

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