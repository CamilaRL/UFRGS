/*********************************************/ 

// Simulação de DM de um fluido de Lennard-Jones com termostato Nosé-Hoover Compile usando "gcc -o NVT_NH NVT_NH.c -lm -lgsl" //

/********************************************/  
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*********CONSTANTES GLOBAIS #1*****************/
#define rho 0.75 //Densidade 
#define V N*1./rho //Volume
#define N 256 //Numeros de particulas
#define T0 0.0
#define M 2 //Numero de correntes Nosé-Hoover
#define TEMPO_MAX 10000 //Tempo de simulação
/*********VARIAVEIS GLOBAIS******************/
double rx[N],ry[N],rz[N];
double vx[N],vy[N],vz[N];
double xi1[N],xi2[N],vxi1[N],vxi2[N];  
double fx[N],fy[N],fz[N];
double Q1[M],Q2[M];// "Massa" de resistencia do Termostato
double uk,pe; // Energia cinetica e potencial
double T;
double et, et0,r2;
/*********CONSTANTES GLOBAIS #2******************/
double l=3*N;// Variaveis reais - Frenkel --> L=3N 
double L = pow(V,1./3.);//Comprimento da aresta da caixa
double delt=0.0002, delt2, delt4, delt8;
double To = 1.0;//Temperatura de interesse
/********************FUNÇÕES*********************/
void init(void);
void force(void);
void chain(double T);
void aplica_PBC(void);
/********************************************/

/****INCIAR AS POSIÇÕES E VELOCIDADES********/
void init ( void) 
/*******************************************/
{
int i;
double cmvx=0.0,cmvy=0.0,cmvz=0.0;
double fac;
double dx,dy,dz;
int M1,n1;

uk=0; 
n1=ceil(pow(N,1./3.));
M1=pow(n1,3);

dx=pow(V/M1,(1./3.));
dy=pow(V/M1,(1./3.));
dz=pow(V/M1,(1./3.));
  
for (i=0;i<N;i++)
 {
rx[i] = (i%n1)*dx;
ry[i] = ((i/n1)%n1)*dy;
rz[i] = ((i/(n1*n1))%n1)*dz;
// Velocidade aleatoria de distribuição normal 

vx[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
vy[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;
vz[i] = ((float)rand()/(float)(RAND_MAX) * 1) - 0.5;

cmvx+=vx[i];
cmvy+=vy[i];
cmvz+=vz[i];

vx[i]-=cmvx/N;
vy[i]-=cmvy/N;
vz[i]-=cmvz/N;
   
uk+=(vx[i]*vx[i]+vy[i]*vy[i]+vz[i]*vz[i])/2;// Energia cinética média
 }
/********************************************/
if (T0>0.0)
 {

T = (2/3)*(uk/N);// Temperatura do sistema
fac=sqrt(T0/T);
    
for (i=0;i<N;i++)
  {
  
vx[i]*=fac;
vy[i]*=fac;
vz[i]*=fac;
      
uk+= (vx[i]*vx[i]+vy[i]*vy[i]+vz[i]*vz[i])/2;
  }
 
 }    

return;  
}
/*********CALCULAR FORÇAS******************/
void force(void)
/*******************************************/ 
{
int i,j;
double dx, dy, dz,r2i, r6i;
double ff,rc,rc2;
double ecut;

pe = 0.0;
rc = L/2;
rc2 = rc*rc;
ecut = 4*(pow(rc2,-6)-pow(rc2,-3));

for (i=0;i<N;i++)
  {
  
fx[i]=0.0;
fy[i]=0.0;
fz[i]=0.0;
  }
   

for (i=0;i<(N-1);i++)
{
for (j=i+1;j<N;j++)
 {
 
dx  = (rx[i]-rx[j]);
dy  = (ry[i]-ry[j]);
dz  = (rz[i]-rz[j]);
	
dx=dx-rint(dx/L)*L;
dy=dy-rint(dy/L)*L;
dz=dz-rint(dz/L)*L;
	
r2 = dx*dx + dy*dy + dz*dz;
	
if (r2<rc2) 
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
	   
pe+= 4.0*r6i*(r6i - 1.0) - ecut;//Energia potencial
	   
}
   }
      }
      
 return;
}
/*******************************************/
void chain ( double T) 
/*******************************************/
{

double G1, G2, s;
int i;

Q1[0] = 10;//1.0//0.1
Q2[1] = 10;//1.0//0.1

delt2 = delt/2;
delt4 = delt/4;
delt8 = delt/8;

G2= (Q1[0]*vxi1[0]*vxi1[0]-T);
vxi2[1]= vxi2[1] + G2*delt4;
vxi1[0]=vxi1[0]*exp(-vxi2[1]*delt8);

G1=(2*uk-l*T)/Q1[0];
vxi1[0]=vxi1[0] + G1*delt4;
vxi1[0]=vxi1[0]*exp(-vxi2[1]*delt8); 
 
xi1[0]=xi2[0] + vxi1[0]*delt2;
xi2[1]=xi2[1] + vxi2[1]*delt2;

s=exp(-vxi1[0]*delt2);

for (i=0;i<N;i++)
 {
vx[i]=s*vx[i]; 
vy[i]=s*vy[i]; 
vz[i]=s*vz[i]; 

 }
uk = uk*s*s;

vxi1[0]=vxi1[0]*exp(-vxi2[1]*delt8);
G1=(2*uk-l*T)/Q1[0];
vxi1[0]=vxi1[0] + G1*delt4;

vxi1[0]=vxi1[0]*exp(-vxi2[1]*delt8);
G2=(Q1[0]*vxi1[0]*vxi1[0]-T)/Q2[1];
vxi2[1]=vxi2[1] + G2*delt4;



return;
}
void aplica_PBC(void)
 {

  int i;
  
for(i=0;i<N;i++)
 {
    rx[i] = rx[i] - floor(rx[i]/L)*L;
    ry[i] = ry[i] - floor(ry[i]/L)*L;
    rz[i] = rz[i] - floor(rz[i]/L)*L;
    /*if(rx[i]>L) 
    {
      rx[i] = rx[i] - 1.0*L;
    }
    else if (rx[i]<0) {
      rx[i] = rx[i] + 1.0*L;
    }
    if(ry[i]>L) 
    {
      ry[i] = ry[i] - 1.0*L;
    }
    else if (ry[i]<0) {
      ry[i] = ry[i] + 1.0*L;
    }
    if(rz[i]>L) 
    {
      rz[i] = rz[i] - 1.0*L;
    }
    else if (ry[i]<0) 
    {
      rz[i] = rz[i] + 1.0*L;
    }
  */  
  }
 
  return;
 
}
/*******************************************/
/*******************************************/
int main ( void ) 
/*******************************************/
{
int i;
double t;

init();
/*******************************************/
for (t=0;t<TEMPO_MAX;t++)
   {

chain(To);
/******************************************/
uk = 0.0;
    
for (i=0;i<N;i++)
   {
rx[i]+=vx[i]*delt2;
ry[i]+=vy[i]*delt2;
rz[i]+=vz[i]*delt2;
  
   }
aplica_PBC(); 
/************Calculo das Forças**************/
force();
      
/********************************************/
for (i=0;i<N;i++)
  {
  
vx[i]+=delt*fx[i];
vy[i]+=delt*fy[i];
vz[i]+=delt*fz[i];
      
rx[i]+=vx[i]*delt2;
ry[i]+=vy[i]*delt2;
rz[i]+=vz[i]*delt2;
      
uk+=(vx[i]*vx[i]+vy[i]*vy[i]+vz[i]*vz[i])/2;

  }

chain(To);

T = (2/3.)*(uk/N);
et = pe + uk;

/*Tempo,ENERGIA(Potencial,Cinetica,Total) e Temperatura*/    
printf("%lf\t%lf\t%lf\t%lf\t%lf\n", t,pe,uk,et,T);
/********************************************/
  }
  
return 0;  
}