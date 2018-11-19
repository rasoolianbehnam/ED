#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


void poisson_solve(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, int iterations, float* V, float* g, float *R, float w, float h) ;

void before_poisson(int imax, int jmax, int kmax, int tmax, float *ne, float *ni, float *difxne, float *difyne, float *difxni, float *difyni, float *difxyne, float *difxyni, float *Exy, float *fexy, float *fixy, float *g, float* g_temp, float *R, float *Ex, float *Ey, float *fex, float *fey, float *fix, float *fiy, float *V, float *L, float *difzne, float *difzni, float *Ez, float *fez, float *fiz, float qi, float qe, float kr, float ki, float si, float sf, float alpha, float q, float pie, float Ta , float w , float eps0 , float Te, float Ti, float B, float Kb, float me, float mi, float nue, float nui, float denominator_e, float denominator_i, float nn, float dt, float h, float wce, float wci, float mue, float mui, float dife, float difi) ;


void after_poisson(int imax, int jmax, int kmax, int tmax, float *ne, float *ni, float* ne_temp, float* ni_temp, float *difxne, float *difyne, float *difxni, float *difyni, float *difxyne, float *difxyni, float *Exy, float *fexy, float *fixy, float *g, float* g_temp, float *R, float *Ex, float *Ey, float *fex, float *fey, float *fix, float *fiy, float *V, float *L, float *difzne, float *difzni, float *Ez, float *fez, float *fiz, float qi, float qe, float kr, float ki, float si, float sf, float alpha, float q, float pie, float Ta , float w , float eps0 , float Te, float Ti, float B, float Kb, float me, float mi, float nue, float nui, float denominator_e, float denominator_i, float nn, float dt, float h, float wce, float wci, float mue, float mui, float dife, float difi) ;



void sum_ne(int imax, int jmax, int kmax, float* mat, float* res) ;


void update_ne(int imax, int jmax, int kmax, float* ne, float* ni, float *sf, float si);

