#include <math.h>
#include <stdio.h>
void cython_sin(float* a, int n, int n_iter) {
    int i, t;
    for (t=0; t<n_iter; t++) {
        for (i=0; i<n; i++) {
            a[i] = sin(a[i]);
        }
    }
}

void main() {
    int i;
    int n = 64 * 128;
    int n_iters = 100000;
    float *a = (float*) malloc(n * sizeof(float));
    for (i=0; i<n; i++) a[i] = 1;
    printf("starting...\n");
    cython_sin(a, n, n_iters);
    printf("%f, %f, %f\n", a[0], a[1], a[2]);
}
