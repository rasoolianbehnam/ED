#include "utility.h"

int main()
{
    int imax = 32, jmax = 32, kmax = 64,i,j,k;
    int n1 = imax+3, n2 = jmax+3, n3 = kmax+3;
    float qi=1.6E-19,qe=-1.6E-19, kr = 0,ki = 0,si = 0,sf = 0,alpha = 0, q=1.6E-19,pie=3.14159,Ta,w,eps0,Te,Ti,B,Kb,me,mi,nue,nui,denominator_e,denominator_i,nn,dt,h,wce,wci,mue,mui,dife,difi;
    int tmax = 200;
    float *ne;
    float *ni;
    float *ne_temp;
    float *ni_temp;
    float *difxne;
    float *difyne;
    float *difxni;
    float *difyni;
    float *difxyne;
    float *difxyni;
    float *Exy;
    float *fexy;
    float *fixy;
    float *g;
    float *g_temp;
    float *R;
    float *Ex;
    float *Ey;
    float *fex;
    float *fey;
    float *fix;
    float *fiy;
    float *V;
    float *L;
    float *difzne;
    float *difzni;
    float *Ez;
    float *fez;
    float *fiz;
    ne  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    ni  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    ne_temp  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    ni_temp  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difxne  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difyne  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difxni  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difyni  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difxyne  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difxyni  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    Exy  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fexy  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fixy  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    g  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    g_temp  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    R  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    Ex  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    Ey  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fex  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fey  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fix  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fiy  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    V  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    L  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difzne  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    difzni  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    Ez  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fez  = (float*) malloc( n1 * n2 * n3 * sizeof(float));
    fiz  = (float*) malloc( n1 * n2 * n3 * sizeof(float));

    Kb    = 1.38E-23;
    B     = 0.0;
    Te    = 2.5*11604.5;
    Ti    = 0.025*11604.5;
    me    = 9.109E-31;
    mi    = 6.633E-26;
    ki    = 0.0;
    dt    = 1.0E-12;
    h     = 1.0E-3;
    eps0  = 8.854E-12;
    si    = 0.0;
    sf    =0.0;

    for ( i=0; i<imax+3;i++){
        for ( j=0; j<jmax+3; j++){
            for ( k=0; k<kmax+3;k++){
                ne[k + n3 * (j + n2 * (i))] = 1e-9;
                ni[k + n3 * (j + n2 * (i))] = 1e-9;
                difxne[k + n3 * (j + n2 * (i))] = 1e-9;
                difyne[k + n3 * (j + n2 * (i))] = 1e-9;
                difxni[k + n3 * (j + n2 * (i))] = 1e-9;
                difyni[k + n3 * (j + n2 * (i))] = 1e-9;
                difxyne[k + n3 * (j + n2 * (i))] = 1e-9;
                difxyni[k + n3 * (j + n2 * (i))] = 1e-9;
                Exy[k + n3 * (j + n2 * (i))] = 1e-9;
                fexy[k + n3 * (j + n2 * (i))] = 1e-9;
                fixy[k + n3 * (j + n2 * (i))] = 1e-9;
                g[k + n3 * (j + n2 * (i))] = 1e-9;
                R[k + n3 * (j + n2 * (i))] = 1e-9;
                Ex[k + n3 * (j + n2 * (i))] = 1e-9;
                Ey[k + n3 * (j + n2 * (i))] = 1e-9;
                fex[k + n3 * (j + n2 * (i))] = 1e-9;
                fey[k + n3 * (j + n2 * (i))] = 1e-9;
                fix[k + n3 * (j + n2 * (i))] = 1e-9;
                fiy[k + n3 * (j + n2 * (i))] = 1e-9;
                V[k + n3 * (j + n2 * (i))] = 1e-9;
                L[k + n3 * (j + n2 * (i))] = 1e-9;
                difzne[k + n3 * (j + n2 * (i))] = 1e-9;
                difzni[k + n3 * (j + n2 * (i))] = 1e-9;
                Ez[k + n3 * (j + n2 * (i))] = 1e-9;
                fez[k + n3 * (j + n2 * (i))] = 1e-9;
                fiz[k + n3 * (j + n2 * (i))] = 1e-9;
             }
        }
    }


    nn=1.33/(Kb*Ti); //neutral density=p/(Kb.T)
    nue=nn*1.1E-19*sqrt(Kb*Te/me); // electron collision frequency= neutral density * sigma_e*Vth_e
    nui=nn*4.4E-19*sqrt(Kb*Ti/mi);
    wce=q*B/me;
    wci=q*B/mi;
    mue=q/(me*nue);
    mui=q/(mi*nui);
    dife=Kb*Te/(me*nue);
    difi=Kb*Ti/(mi*nui);
    ki=0.00002/(nn*dt);
    denominator_e= (1+wce*wce/(nue*nue));
    denominator_i= (1+wci*wci/(nui*nui));
    // Ta and W are just some constants needed for the iterative method that we have used to solve Poisson eq.
    Ta=acos((cos(pie/imax)+cos(pie/jmax)+cos(pie/kmax))/3.0);// needs to be float checked
    w=2.0/(1.0+sin(Ta));
// -----------------------------------------------------------------------------------------------
    //Density initialization
    // To add multiple Gaussian sources, just simply use the density_initialization function at the (x,y) points that you want
    int x_position = 15, y_position = 15, z_position = 15;
    for ( i=1; i<imax-1;i++){
        for ( j=1; j<jmax-1;j++){
            for ( k=1; k<kmax-1;k++){
            ne[k + n3 * (j + n2 * (i))]= 2.0E13;/*
                1.0E14+1.0E14*exp(-(pow((i-x_position),2)+
                pow((j-y_position),2)+pow((k-z_position),2))/100.0);*/
            ni[k + n3 * (j + n2 * (i))]=2.0E13;/*
                1.0E14+1.0E14*exp(-(pow((i-x_position),2)+
                pow((j-y_position),2)+pow((k-z_position),2))/100.0);*/
            }
        }
    }



    for ( k=1; k<kmax+1; k++) {
        for ( j=1; j<jmax+1; j++) {
            for ( i=1; i<imax+1;i++) {
            si=si+ne[k + n3 * (j + n2 * (i))] ;
            }
        }
    }

    int myTime,kk,I,N,s1; 
    N=n1*n2*n3;
    int iterations = 40;

    float* sf_temp;
    sf_temp = (float*) malloc(sizeof(sf_temp));
    double begin = clock();
    for ( myTime=1; myTime<tmax; myTime++){  // This for loop takes care of myTime evolution
        printf("%d\n", myTime);
//################################################################################################################
        //UNCOMMENT THE FOLLOWING TO RUN THE CODE ON CPU
//################################################################################################################
        before_poisson(imax, jmax, kmax, tmax, ne, ni, difxne, difyne, difxni, difyni, difxyne, difxyni, Exy, fexy, fixy, g, g_temp, R, Ex, Ey, fex, fey, fix, fiy, V, L, difzne, difzni, Ez, fez, fiz, qi, qe, kr, ki, si, sf, alpha, q, pie,Ta ,w ,eps0 , Te, Ti, B, Kb, me, mi, nue, nui, denominator_e, denominator_i, nn, dt, h, wce, wci, mue, mui, dife, difi);

        poisson_solve(imax, jmax, kmax, n1, n2, n3, N, iterations, V, g, R, w, h);

        after_poisson(imax, jmax, kmax, tmax, ne, ni, ne_temp, ni_temp, difxne, difyne, difxni, difyni, difxyne, difxyni, Exy, fexy, fixy, g, g_temp, R, Ex, Ey, fex, fey, fix, fiy, V, L, difzne, difzni, Ez, fez, fiz, qi, qe, kr, ki, si, sf, alpha, q, pie,Ta ,w ,eps0 , Te, Ti, B, Kb, me, mi, nue, nui, denominator_e, denominator_i, nn, dt, h, wce, wci, mue, mui, dife, difi);
        sum_ne(imax, jmax, kmax, ne, sf_temp);
        //printf("sf = %f\n", *sf_temp);
        update_ne(imax, jmax, kmax, ne, ni, sf_temp, si);


     }

    double time_spent1 = (clock() - begin) / CLOCKS_PER_SEC;
    printf("Time spent without parallelization: %f\n", time_spent1);

    printf("%f\n", V[5 + (kmax+3) * (5 + (jmax+3) * 5)]);
}
