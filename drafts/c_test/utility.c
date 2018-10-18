#include "utility.h"


void poisson_solve(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, int iterations, float* V, float* g, float *R, float w, float h) {
      for (int kk=0; kk<iterations; kk++) {
        for (int I = 0; I < N; I ++) {
             int k = I % n3;
             int s1 = (I - k) / n3;
             int j = s1 % n2;
             int i = (s1 - j) / n2;
            if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
            R[k + n3 * (j + n2 * (i))]=
                (V[k + n3 * (j + n2 * (i+1))]+
                     V[k + n3 * (j + n2 * (i-1))]+
                     V[k + n3 * (j+1 + n2 * (i))]+
                     V[k + n3 * (j-1 + n2 * (i))]+
                     V[k+1 + n3 * (j + n2 * (i))]+
                     V[k-1 + n3 * (j + n2 * (i))]
                 ) / 6.0 - V[k + n3 * (j + n2 * (i))]- (h*h)*g[k + n3 * (j + n2 * (i))]/6.0;
            V[k + n3 * (j + n2 * (i))] += w*R[k + n3 * (j + n2 * (i))];
        }
    }
}



void before_poisson(int imax, int jmax, int kmax, int tmax, float *ne, float *ni, float *difxne, float *difyne, float *difxni, float *difyni, float *difxyne, float *difxyni, float *Exy, float *fexy, float *fixy, float *g, float* g_temp, float *R, float *Ex, float *Ey, float *fex, float *fey, float *fix, float *fiy, float *V, float *L, float *difzne, float *difzni, float *Ez, float *fez, float *fiz, float qi, float qe, float kr, float ki, float si, float sf, float alpha, float q, float pie, float Ta , float w , float eps0 , float Te, float Ti, float B, float Kb, float me, float mi, float nue, float nui, float denominator_e, float denominator_i, float nn, float dt, float h, float wce, float wci, float mue, float mui, float dife, float difi) {
    int index_x = 0;
    int stride_x = 1;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1; 
    N=n1*n2*n3;
        for (int I=0; I<N; I++) g_temp[I] = w*h*h*g[I]/6.;
        for (int I=0; I<N; I++) {
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


void after_poisson(int imax, int jmax, int kmax, int tmax, float *ne, float *ni, float* ne_temp, float* ni_temp, float *difxne, float *difyne, float *difxni, float *difyni, float *difxyne, float *difxyni, float *Exy, float *fexy, float *fixy, float *g, float* g_temp, float *R, float *Ex, float *Ey, float *fex, float *fey, float *fix, float *fiy, float *V, float *L, float *difzne, float *difzni, float *Ez, float *fez, float *fiz, float qi, float qe, float kr, float ki, float si, float sf, float alpha, float q, float pie, float Ta , float w , float eps0 , float Te, float Ti, float B, float Kb, float me, float mi, float nue, float nui, float denominator_e, float denominator_i, float nn, float dt, float h, float wce, float wci, float mue, float mui, float dife, float difi) {
    int index_x = 0;
    int stride_x = 1;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1; 
    N=n1*n2*n3;
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



        // calculating the loss
//         sf=0.0;
//       for ( I = index_x; I < N; I += stride_x) {
//         k = I % n3;
//         s1 = (I - k) / n3;
//         j = s1 % n2;
//         i = (s1 - j) / n2;
//         if (i * j * k == 0 || i >= imax || j >= jmax || k >= kmax) continue;
//        sf=sf+ne[k + n3 * (j + n2 * (i))] ;
//    }
//       printf("sf = %f\n", sf);
//
//        alpha=(si-sf)/sf;
//
//    for ( I = index_x; I < N; I += stride_x) {
//         k = I % n3;
//         s1 = (I - k) / n3;
//         j = s1 % n2;
//         i = (s1 - j) / n2;
//        if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
//        ne_temp[k + n3 * (j + n2 * (i))]=ne[k + n3 * (j + n2 * (i))]+alpha*ne[k + n3 * (j + n2 * (i))] ;
//        ni_temp[k + n3 * (j + n2 * (i))]=ni[k + n3 * (j + n2 * (i))]+alpha*ne[k + n3 * (j + n2 * (i))] ;
//    }
//    for ( I = index_x; I < N; I += stride_x) {
//        ne[I] = ne_temp[I];
//        ni[I] = ni_temp[I];
//    }
      // if (myTime%100==0.0){
     //  }

}



void sum_ne(int imax, int jmax, int kmax, float* mat, float* res) {
    *res = 0;
    int index_x = 0;
    int stride_x = 1;
    int  n1=imax+3, n2 = jmax+3, n3 = kmax+3,i,j,k,myTime,kk,I,N,s1; 
    N=n1*n2*n3;
    for (int I = index_x; I < N; I += stride_x) {
        int k = I % n3;
        int s1 = (I - k) / n3;
        int j = s1 % n2;
        int i = (s1 - j) / n2;
       if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
        *res += mat[I];
    }

}


void update_ne(int imax, int jmax, int kmax, float* ne, float* ni, float *sf, float si) {
    int index_x = 0;
    int stride_x = 1;
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

