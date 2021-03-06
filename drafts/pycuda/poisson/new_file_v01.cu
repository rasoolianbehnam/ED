#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


__global__ void mardas(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, int iterations, float* V, float* g, float *R, float w, float h, int oddEven) {
    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
        for (int I = index_x; I < N; I +=stride_x) {
            V[I] = 1000;
        }
}

__global__ void poisson_solve_1it_cu(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, float* V, float* g, float *R, float w, float h, int oddEven) {
    int I = threadIdx.x + blockDim.x * blockIdx.x;
    //int stride_x = blockDim.x * gridDim.x;
        //for (int I = index_x; I < N; I +=stride_x) {
             int k = I % n3;
             int s1 = (I - k) / n3;
             int j = s1 % n2;
             int i = (s1 - j) / n2;
            if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) return;
            if ((i+j+k)%2==oddEven) return;
            R[k + n3 * (j + n2 * (i))]=
                (V[k + n3 * (j + n2 * (i+1))]+
                     V[k + n3 * (j + n2 * (i-1))]+
                     V[k + n3 * (j+1 + n2 * (i))]+
                     V[k + n3 * (j-1 + n2 * (i))]+
                     V[k+1 + n3 * (j + n2 * (i))]+
                     V[k-1 + n3 * (j + n2 * (i))]
                 ) / 6.0 - V[k + n3 * (j + n2 * (i))]- (h*h)*g[k + n3 * (j + n2 * (i))]/6.0;
            V[k + n3 * (j + n2 * (i))] += w*R[k + n3 * (j + n2 * (i))];
        //}
}
__global__ void before_poisson_cu(int imax, int jmax, int kmax, float* ne,float* ni, float *g, float* g_temp, float *values) {

    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1;
    N=n1*n2*n3;
    float qi = values[0];
    float qe = values[1];
    float w = values[10];
    float eps0 = values[11];
    float h = values[24];
    for (int I=index_x; I<N; I+=stride_x) g_temp[I] = w*h*h*g[I]/6.;
    for (int I=index_x; I<N; I+=stride_x) {
        int k = I % n3;
        int s1 = (I - k) / n3;
        int j = s1 % n2;
        int i = (s1 - j) / n2;
        if (i >= 1 && i < imax-1
                && j >= 1 && j < jmax-1
                && k >= 1 && k < kmax-1) {
            g_temp[I] += w/6.*(g_temp[I-1]+g_temp[I-n3]+g_temp[I-n3*n2]);
        }
        else {
            g_temp[I] = 0;
        }
    }

      for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        g[k + n3 * (j + n2 * (i))]=-(ne[k + n3 * (j + n2 * (i))]*qe+ni[k + n3 * (j + n2 * (i))]*qi)/eps0;
    }

}


__global__ void after_poisson_cu(int imax, int jmax, int kmax, float *ne, float *ni , float *difxne, float *difyne, float *difxni , float *difyni, float *difxyne, float *difxyni, float *Exy, float *fexy , float *fixy, float *R, float *Ex, float *Ey , float *fex, float *fey, float *fix, float *fiy, float *V, float *difzne, float *difzni, float *Ez, float *fez, float *fiz , float *values, float *sf_temp) {
    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1;
    N=n1*n2*n3;
    float q = values[7];
    float me = values[16];
    float mi = values[17];
    float nue = values[18];
    float nui = values[19];
    float denominator_e = values[20];
    float denominator_i = values[21];
    float dt = values[23];
    float h = values[24];
    float wce = values[25];
    float wci = values[26];
    float mue = values[27];
    float mui = values[28];
    float dife = values[29];
    float difi = values[30];

  for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i >= imax-1 || j >= jmax || k >= kmax) continue;
        Ex[k + n3 * (j + n2 * (i))]= (V[k + n3 * (j + n2 * (i))]-V[k + n3 * (j + n2 * (i+1))])/h;
        difxne[k + n3 * (j + n2 * (i))]=(ne[k + n3 * (j + n2 * (i+1))]-ne[k + n3 * (j + n2 * (i))])/h;
        difxni[k + n3 * (j + n2 * (i))]=(ni[k + n3 * (j + n2 * (i+1))]-ni[k + n3 * (j + n2 * (i))])/h;
        }


    for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i >= imax || j >= jmax-1 || k >= kmax) continue;
        Ey[k + n3 * (j + n2 * (i))]= (V[k + n3 * (j + n2 * (i))]-V[k + n3 * (j+1 + n2 * (i))])/h;
        difyne[k + n3 * (j + n2 * (i))]=(ne[k + n3 * (j+1 + n2 * (i))]-ne[k + n3 * (j + n2 * (i))])/h;
        difyni[k + n3 * (j + n2 * (i))]=(ni[k + n3 * (j+1 + n2 * (i))]-ni[k + n3 * (j + n2 * (i))])/h;
        }


    for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i >= imax || j >= jmax || k >= kmax-1) continue;
       Ez[k + n3 * (j + n2 * (i))]= (V[k + n3 * (j + n2 * (i))]-V[k+1 + n3 * (j + n2 * (i))])/h;
       difzne[k + n3 * (j + n2 * (i))]=(ne[k+1 + n3 * (j + n2 * (i))]-ne[k + n3 * (j + n2 * (i))])/h;
       difzni[k + n3 * (j + n2 * (i))]=(ni[k+1 + n3 * (j + n2 * (i))]-ni[k + n3 * (j + n2 * (i))])/h;
     }

// -----------------------------------------------------------------------------------------------
       /* Since I am using mid points for Calculating electric field and density gradient,
        to calculate Ex at any point that I don't have it directly, the average over
        the neighboring points is used instead. these average variables are, exy, fexy, fixy, ...*/
        // Calculating the average values of Ex and gradiant_x
   for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;

        Exy[k + n3 * (j + n2 * (i))]= 0.0 ;
        difxyne[k + n3 * (j + n2 * (i))]=0.0;
        difxyni[k + n3 * (j + n2 * (i))]=0.0;
    }

    for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i * k == 0 ||  i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        Exy[k + n3 * (j + n2 * (i))]= 0.25*(Ex[k + n3 * (j + n2 * (i))]+Ex[k + n3 * (j+1 + n2 * (i))]+Ex[k + n3 * (j + n2 * (i-1))]+Ex[k + n3 * (j+1 + n2 * (i-1))]) ;
        difxyne[k + n3 * (j + n2 * (i))]=0.25*(difxne[k + n3 * (j + n2 * (i))]+difxne[k + n3 * (j+1 + n2 * (i))]+difxne[k + n3 * (j + n2 * (i-1))]+difxne[k + n3 * (j+1 + n2 * (i-1))]);
        difxyni[k + n3 * (j + n2 * (i))]=0.25*(difxni[k + n3 * (j + n2 * (i))]+difxni[k + n3 * (j+1 + n2 * (i))]+difxni[k + n3 * (j + n2 * (i-1))]+difxni[k + n3 * (j+1 + n2 * (i-1))]);
    }


// -----------------------------------------------------------------------------------------------
        // Here we calculate the fluxes in y direction

       for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i * k == 0 ||  i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        fey[k + n3 * (j + n2 * (i))]= (-0.5*(ne[k + n3 * (j+1 + n2 * (i))]+ne[k + n3 * (j + n2 * (i))])*mue*Ey[k + n3 * (j + n2 * (i))]-dife*difyne[k + n3 * (j + n2 * (i))]
        -wce*q*0.5*(ne[k + n3 * (j+1 + n2 * (i))]+ne[k + n3 * (j + n2 * (i))])*Exy[k + n3 * (j + n2 * (i))]/(me*nue*nue)-wce*dife*difxyne[k + n3 * (j + n2 * (i))]/nue)/denominator_e;
        fiy[k + n3 * (j + n2 * (i))]= (0.5*(ni[k + n3 * (j+1 + n2 * (i))]+ni[k + n3 * (j + n2 * (i))])*mui*Ey[k + n3 * (j + n2 * (i))]-difi*difyni[k + n3 * (j + n2 * (i))]
        -wci*q*0.5*(ni[k + n3 * (j+1 + n2 * (i))]+ni[k + n3 * (j + n2 * (i))])*Exy[k + n3 * (j + n2 * (i))]/(mi*nui*nui)+wci*difi*difxyni[k + n3 * (j + n2 * (i))]/nui)/denominator_i;
    }


    for ( I =index_x; I < n1 * n3; I += stride_x) {
         k = I % n3;
         i = (I - k) / n3;

        if (i * k == 0 ||  i >= imax-1 || k >= kmax-1) continue;

        if (fey[k + n3 * (0 + n2 * (i))] > 0.0){
                fey[k + n3 * (0 + n2 * (i))] = 0.0;
                }

        if (fiy[k + n3 * (0 + n2 * (i))] > 0.0){
                fiy[k + n3 * (0 + n2 * (i))] = 0.0;
                }

        if (fey[k + n3 * (jmax-2 + n2 * (i))] < 0.0){
                fey[k + n3 * (jmax-2 + n2 * (i))] = 0.0;
                }

        if (fiy[k + n3 * (jmax-2 + n2 * (i))] < 0.0){
                fiy[k + n3 * (jmax-2 + n2 * (i))] = 0.0;
                }

    }

// -----------------------------------------------------------------------------------------------
        // Calculating the average Exy and difxy to be used in x direction fluxes
       // Calculating the average values of Ey and gradiant_y


      for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;

        Exy[k + n3 * (j + n2 * (i))]= 0.0 ;
        difxyne[k + n3 * (j + n2 * (i))]=0.0;
        difxyni[k + n3 * (j + n2 * (i))]=0.0;
    }


      for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        Exy[k + n3 * (j + n2 * (i))]= 0.25*(Ey[k + n3 * (j + n2 * (i))]+Ey[k + n3 * (j-1 + n2 * (i))]+Ey[k + n3 * (j + n2 * (i+1))]+Ey[k + n3 * (j-1 + n2 * (i+1))]);
        difxyne[k + n3 * (j + n2 * (i))]= 0.25*(difyne[k + n3 * (j + n2 * (i))]+difyne[k + n3 * (j-1 + n2 * (i))]+difyne[k + n3 * (j + n2 * (i+1))]+difyne[k + n3 * (j-1 + n2 * (i+1))]);
        difxyni[k + n3 * (j + n2 * (i))]= 0.25*(difyni[k + n3 * (j + n2 * (i))]+difyni[k + n3 * (j-1 + n2 * (i))]+difyni[k + n3 * (j + n2 * (i+1))]+difyni[k + n3 * (j-1 + n2 * (i+1))]);

    }

// -----------------------------------------------------------------------------------------------
        // Now ready to calculate the fluxes in x direction

    for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        fex[k + n3 * (j + n2 * (i))]=(-0.5*(ne[k + n3 * (j + n2 * (i))]+ne[k + n3 * (j + n2 * (i+1))])*mue*Ex[k + n3 * (j + n2 * (i))]-dife*difxne[k + n3 * (j + n2 * (i))]
        +wce*dife*difxyne[k + n3 * (j + n2 * (i))]/nue+wce*q*0.5*(ne[k + n3 * (j + n2 * (i))]+ne[k + n3 * (j + n2 * (i+1))])/(me*nue*nue)*Exy[k + n3 * (j + n2 * (i))])/denominator_e;
        fix[k + n3 * (j + n2 * (i))]=(0.5*(ni[k + n3 * (j + n2 * (i))]+ni[k + n3 * (j + n2 * (i+1))])*mui*Ex[k + n3 * (j + n2 * (i))]-difi*difxni[k + n3 * (j + n2 * (i))]
        -wci*difi*difxyni[k + n3 * (j + n2 * (i))]/nui+wci*q*0.5*(ni[k + n3 * (j + n2 * (i))]+ni[k + n3 * (j + n2 * (i+1))])*Exy[k + n3 * (j + n2 * (i))]/(mi*nui*nui))/denominator_i;
    }


    for ( I = index_x; I < n2 * n3; I += stride_x) {
         k = I % n3;
         j = (I - k) / n3;

        if (j * k == 0 ||  j >= jmax-1 || k >= kmax-1) continue;

        if (fex[k + n3 * (j + n2 * (0))] > 0.0){
                fex[k + n3 * (j + n2 * (0))] = 0.0;
                }

        if (fix[k + n3 * (j + n2 * (0))] > 0.0){
                fix[k + n3 * (j + n2 * (0))] = 0.0;
                }

        if (fex[k + n3 * (j + n2 * (imax-2))] < 0.0){
                fex[k + n3 * (j + n2 * (imax-2))] = 0.0;
                }

        if (fix[k + n3 * (j + n2 * (imax-2))] < 0.0){
                fix[k + n3 * (j + n2 * (imax-2))] = 0.0;
                }

    }

// -----------------------------------------------------------------------------------------------

        // Now we calculate the fluxes in z direction
      for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i * j == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        fez[k + n3 * (j + n2 * (i))]=-0.5*(ne[k + n3 * (j + n2 * (i))]+ne[k+1 + n3 * (j + n2 * (i))])*mue*Ez[k + n3 * (j + n2 * (i))]-dife*difzne[k + n3 * (j + n2 * (i))];
        fiz[k + n3 * (j + n2 * (i))]=0.5*(ni[k + n3 * (j + n2 * (i))]+ni[k+1 + n3 * (j + n2 * (i))])*mui*Ez[k + n3 * (j + n2 * (i))]-difi*difzni[k + n3 * (j + n2 * (i))];

    }
       // BC on fluxes

    for ( I = index_x; I < n1 * n2; I += stride_x) {
         j = I % n2;
         i = (I - j) / n2;
        if (i * j == 0 || i >= imax-1 || j >= jmax-1) continue;
        if (fez[0 + n3 * (j + n2 * (i))]>0.0){
            fez[0 + n3 * (j + n2 * (i))]=0.0;
        }
        if (fiz[0 + n3 * (j + n2 * (i))]>0.0){
            fiz[0 + n3 * (j + n2 * (i))]=0.0;
        }
        if (fez[kmax-2 + n3 * (j + n2 * (i))]<0.0){
            fez[kmax-2 + n3 * (j + n2 * (i))]=0.0;
        }
        if (fiz[kmax-2 + n3 * (j + n2 * (i))]<0.0){
            fiz[kmax-2 + n3 * (j + n2 * (i))]=0.0;
        }
    }
// -----------------------------------------------------------------------------------------------


       for ( I = index_x; I < N; I += stride_x) {
         k = I % n3;
         s1 = (I - k) / n3;
         j = s1 % n2;
         i = (s1 - j) / n2;
        if (i * j * k == 0 || i >= imax || j >= jmax || k >= kmax) continue;
        ne[k + n3 * (j + n2 * (i))]=ne[k + n3 * (j + n2 * (i))]-dt*(fex[k + n3 * (j + n2 * (i))]-fex[k + n3 * (j + n2 * (i-1))]+fey[k + n3 * (j + n2 * (i))]-fey[k + n3 * (j-1 + n2 * (i))]+fez[k + n3 * (j + n2 * (i))]-fez[k-1 + n3 * (j + n2 * (i))])/h ;
        ni[k + n3 * (j + n2 * (i))]=ni[k + n3 * (j + n2 * (i))]-dt*(fix[k + n3 * (j + n2 * (i))]-fix[k + n3 * (j + n2 * (i-1))]+fiy[k + n3 * (j + n2 * (i))]-fiy[k + n3 * (j-1 + n2 * (i))]+fiz[k + n3 * (j + n2 * (i))]-fiz[k-1 + n3 * (j + n2 * (i))])/h ;
    }





        for ( I = index_x; I < n1 * n2; I += stride_x) {
         j = I % n2;
         i = (I - j) / n2;
        if (i * j == 0 || i >= imax || j >= jmax ) continue;

        ne[0 + n3 * (j + n2 * (i))] = -dt*fez[0 + n3 * (j + n2 * (i))]/h ;
        ni[0 + n3 * (j + n2 * (i))] = -dt*fiz[0 + n3 * (j + n2 * (i))]/h ;

    }

     for ( I = index_x; I < n1 * n3; I += stride_x) {
         k = I % n3;
         i = (I - k) / n3;

        if (i * k == 0 ||  i >= imax || k >= kmax) continue;

        ne[k + n3 * (0 + n2 * (i))] = -dt*fey[k + n3 * (0 + n2 * (i))]/h ;
        ni[k + n3 * (0 + n2 * (i))] = -dt*fiy[k + n3 * (0 + n2 * (i))]/h ;

    }




      for ( I = index_x; I < n2 * n3; I += stride_x) {
         k = I % n3;
         j = (I - k) / n3;
        if (j * k == 0 ||  j >= jmax || k >= kmax) continue;

       ne[k + n3 * (j + n2 * (0))]= -dt*fex[k + n3 * (j + n2 * (0))]/h ;
       ni[k + n3 * (j + n2 * (0))]= -dt*fix[k + n3 * (j + n2 * (0))]/h ;


    }




        // BC on densities

     for ( I = index_x; I < n1 * n3; I += stride_x) {
         k = I % n3;
         i = (I - k) / n3;

        if (i * k == 0 ||  i >= imax || k >= kmax) continue;

        ne[k + n3 * (0 + n2 * (i))] = 0.0 ;
        ni[k + n3 * (0 + n2 * (i))] = 0.0 ;

        ne[k + n3 * (jmax-1 + n2 * (i))] = 0.0 ;
        ni[k + n3 * (jmax-1 + n2 * (i))] = 0.0 ;

    }




      for ( I = index_x; I < n2 * n3; I += stride_x) {
         k = I % n3;
         j = (I - k) / n3;
        if (j * k == 0 ||  j >= jmax || k >= kmax) continue;

       ne[k + n3 * (j + n2 * (0))]= 0.0 ;
       ni[k + n3 * (j + n2 * (0))]= 0.0 ;

       ne[k + n3 * (j + n2 * (imax-1))]= 0.0 ;
       ni[k + n3 * (j + n2 * (imax-1))]= 0.0 ;


    }



    for ( I = index_x; I < n1*n2; I += stride_x) {
         j = I % n2;
         i = (I - j) / n2;
        if (i * j == 0 || i >= imax+1 || j >= jmax+1) continue;
        ne[kmax-1 + n3 * (j + n2 * (i))]=0.0;
        ne[0 + n3 * (j + n2 * (i))]=0.0;
        ni[kmax-1 + n3 * (j + n2 * (i))]=0.0;
        ni[0 + n3 * (j + n2 * (i))]=0.0;

    }



    sf_temp[0] = 0;
}



__global__ void sum_ne_cu(int imax, int jmax, int kmax, float* mat, float* res) {
    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1;
    N=n1*n2*n3;
    for (int I = index_x; I < N; I += stride_x) {
        int k = I % n3;
        int s1 = (I - k) / n3;
        int j = s1 % n2;
        int i = (s1 - j) / n2;
       if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
       atomicAdd(res, mat[I]);
    }
}



__global__ void update_ne_cu(int imax, int jmax, int kmax, float* ne, float* ni, float *sf, float si) {
    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1;
    N=n1*n2*n3;
    float alpha=(si-sf[0])/(sf[0]);
   for ( int I = index_x; I < N; I += stride_x) {
        int k = I % n3;
        int s1 = (I - k) / n3;
        int j = s1 % n2;
        int i = (s1 - j) / n2;
       if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
       ne[k + n3 * (j + n2 * (i))]=ne[k + n3 * (j + n2 * (i))]+alpha*ne[k + n3 * (j + n2 * (i))] ;
       ni[k + n3 * (j + n2 * (i))]=ni[k + n3 * (j + n2 * (i))]+alpha*ne[k + n3 * (j + n2 * (i))] ;
   }

}
int main()
{
    int deviceIndex = 0;
    cudaSetDevice(deviceIndex);
    printf("Using device %d\n", deviceIndex);
    int imax = 64, jmax = 64, kmax = 64,i,j,k;
    int n1 = imax+3, n2 = jmax+3, n3 = kmax+3;
    float qi=1.6E-19,qe=-1.6E-19, kr = 0,ki = 0,si = 0,sf = 0,alpha = 0, q=1.6E-19,pie=3.14159,Ta,w,eps0,Te,Ti,B,Kb,me,mi,nue,nui,denominator_e,denominator_i,nn,dt,h,wce,wci,mue,mui,dife,difi;
    int tmax = 100;
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
    float *values;
    cudaMallocManaged(&(values ), 32 * sizeof(float));
    cudaMallocManaged(&(ne ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(ni ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(ne_temp ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(ni_temp ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difxne ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difyne ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difxni ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difyni ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difxyne ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difxyni ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(Exy ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fexy ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fixy ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(g ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(g_temp ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(R ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(Ex ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(Ey ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fex ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fey ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fix ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fiy ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(V ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(L ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difzne ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(difzni ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(Ez ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fez ), n1 * n2 * n3 * sizeof(float));
    cudaMallocManaged(&(fiz ), n1 * n2 * n3 * sizeof(float));

    Kb    = 1.38E-23;
    B     = 0.5;
    Te    = 2.5*11604.5;
    Ti    = 0.025*11604.5;
    me    = 9.109E-31;
    mi    = 6.633E-26;
    ki    = 0.0;
    dt    = 1.0E-14;
    h     = 4.0E-4;
    eps0  = 8.854E-12;
    si    = 0.0;
    sf    =0.0;



    FILE*fp1;
    FILE*fp2;
    FILE*fp3;


    fp1=fopen("V_0.5B_20m.txt","w");
    fp2=fopen("ne_0.5B_20m.txt","w");
    fp3=fopen("ni_0.5B_20m.txt","w");





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

    nn=10.0/(Kb*Ti); //neutral density=p/(Kb.T)
    nue=nn*1.1E-19*sqrt(2.55*Kb*Te/me); // electron collision frequency= neutral density * sigma_e*Vth_e
    nui=nn*4.4E-19*sqrt(2.55*Kb*Ti/mi);
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
            ne[k + n3 * (j + n2 * (i))]= 5.0E14;/*
                1.0E14+1.0E14*exp(-(pow((i-x_position),2)+
                pow((j-y_position),2)+pow((k-z_position),2))/100.0);*/
            ni[k + n3 * (j + n2 * (i))]=5.0E14;/*
                1.0E14+1.0E14*exp(-(pow((i-x_position),2)+
                pow((j-y_position),2)+pow((k-z_position),2))/100.0);*/
            }
        }
    }


    for ( i=18; i<22;i++){
        for ( j=18; j<22;j++){
         for ( k=20; k<40;k++){

        ne[k + n3 * (j + n2 * (i))]=5.0E15;
        ni[k + n3 * (j + n2 * (i))]=5.0E15;
         }
        }
    }

   for ( i=38; i<42;i++){
        for ( j=18; j<22;j++){
         for ( k=20; k<40;k++){

        ne[k + n3 * (j + n2 * (i))]=5.0E15;
        ni[k + n3 * (j + n2 * (i))]=5.0E15;
         }
        }
    }


    for ( i=18; i<22;i++){
        for ( j=38; j<42;j++){
         for ( k=20; k<40;k++){

        ne[k + n3 * (j + n2 * (i))]=5.0E15;
        ni[k + n3 * (j + n2 * (i))]=5.0E15;
         }
        }
    }


    for ( i=38; i<42;i++){
        for ( j=38; j<42;j++){
         for ( k=20; k<40;k++){

        ne[k + n3 * (j + n2 * (i))]=5.0E15;
        ni[k + n3 * (j + n2 * (i))]=5.0E15;
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
    cudaMallocManaged(&sf_temp, sizeof(sf_temp));
    for (i=0; i<31; i++) {
        values[0] = qi;
        values[1] = qe;
        values[2] = kr;
        values[3] = ki;
        values[4] = si;
        values[5] = sf;
        values[6] = alpha;
        values[7] = q;
        values[8] = pie;
        values[9] = Ta;
        values[10] = w;
        values[11] = eps0;
        values[12] = Te;
        values[13] = Ti;
        values[14] = B;
        values[15] = Kb;
        values[16] = me;
        values[17] = mi;
        values[18] = nue;
        values[19] = nui;
        values[20] = denominator_e;
        values[21] = denominator_i;
        values[22] = nn;
        values[23] = dt;
        values[24] = h;
        values[25] = wce;
        values[26] = wci;
        values[27] = mue;
        values[28] = mui;
        values[29] = dife;
        values[30] = difi;
    }
    double begin = clock();
    for ( myTime=1; myTime<tmax; myTime++){  // This for loop takes care of myTime evolution
        //if (myTime % 1000 == 0)
        //    printf("%d\n", myTime);



        before_poisson_cu<<<512, N/512>>>(imax, jmax, kmax, ne, ni, g, g_temp, values);



        for (kk=0; kk<iterations; kk++) {
            poisson_solve_1it_cu<<<512, N/512>>>(imax, jmax, kmax, n1, n2, n3, N, V, g, R, w, h, 1);
            poisson_solve_1it_cu<<<512, N/512>>>(imax, jmax, kmax, n1, n2, n3, N, V, g, R, w, h, 0);
        }


        after_poisson_cu<<<512, N/512>>>( imax,  jmax,  kmax,  ne, ni , difxne, difyne, difxni , difyni, difxyne, difxyni, Exy, fexy, fixy, R, Ex, Ey , fex, fey, fix, fiy, V, difzne, difzni, Ez, fez, fiz , values, sf_temp);


        sum_ne_cu<<<512, N/512>>>(imax, jmax, kmax, ne, sf_temp);


        update_ne_cu<<<512, N/512>>>(imax, jmax, kmax, ne, ni, sf_temp, si);
	//printf("%d\n", myTime);

     }

    double time_spent1 = (clock() - begin) / CLOCKS_PER_SEC;
    printf("Time spent without parallelization: %f\n", time_spent1);

    cudaDeviceSynchronize();
    printf("%f\n", V[5 + (kmax+3) * (5 + (jmax+3) * 5)]);
    printf("%f\n", g[5 + (kmax+3) * (5 + (jmax+3) * 5)]);




   for ( i=0; i<imax+1;i++){
        for ( j=0; j<jmax+1; j++){
         fprintf(fp1,"%d %d %f \n", i,j,V[31 + n3 * (j + n2 * (i))]);
         fprintf(fp2,"%d %d %f \n", i,j,ne[31 + n3 * (j + n2 * (i))]);
         fprintf(fp3,"%d %d %f \n", i,j,ni[31 + n3 * (j + n2 * (i))]);
        }
    }
}
