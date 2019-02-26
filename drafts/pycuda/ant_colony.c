#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 5
#define M 50
#define T 100

float tau[N][N];
float tau_tmp[N][N];
float eta[N][N];
float alpha, beta;
float p[N][N];

float dist[N][N] = {{0, 10, 5, 2, 8}, {10, 0, 6, 5, 4}, {5, 6, 0, 9, 2}, {2, 5, 9, 0, 7}, {8, 4, 2, 7, 0}};

float uni_rand() {
    return ((float) rand()) / RAND_MAX;
}

void initiate() {
    int i, j, k;
    alpha = beta = .5;
    for (i=0; i<N; i++) {
        for (j=0; j<N; j++) {
            tau[i][j] = uni_rand();
            p[i][j] = ((tau[i][j], alpha) * pow(dist[i][j], beta));
        }
    }
}

void update_probs() {
    int i,j;
    for (i=0; i<N; i++) {
        for (j=0; j<N; j++) {
            printf("p[%d][%d] = %4.2f\n", i, j, p[i][j]);
        }
    }
}
int check_if_sum_is_one(int length, float probs[length]) {
    int i;
    float sum;
    for (i=0; i<length; i++) {
        sum+=probs[i];
    }
    if (sum - 1 < 1e5 | sum -1 > -1e5) return 1;
    return 0;
}



int pick_randomly(int length, float probs[length]) {
    int i;
    float accumulated[length];
    accumulated[0] = 0;
    int indices[length];
    float probs_copy[length];
    copy_from_array(length, probs, probs_copy);
    insertion_sort(length, probs_copy, indices);
    for (i=1; i<length; i++) {
        accumulated[i] = accumulated[i-1] + probs_copy[i];
    }
    for (i=1; i<length; i++) {
        accumulated[i] /= accumulated[length-1];
        printf("%4.2f ", accumulated[i]);
    }
    printf("\n");
    float r = uni_rand();
    i = 0;
    while (i < length && r > accumulated[i]) {
        i++;
    }
    printf("picked %d for random number %4.2f\n", i-1, r);
    printf("************\n");
    return indices[i-1];
}

void copy_from_array(int length, float array_from[length], float array_to[length]) {
    int i;
    for (i=0; i<length; i++) {
        array_to[i] = array_from[i];
    }
}

void insertion_sort(int length, float A[length], int indices[length]) {
    int i, j;
    float tmp;
    int tmpi;
    for (i=0; i<length; i++) {
        indices[i] = i;
    }
    for (i = 1; i < length; i++) {
        j = i-1;
        while (j >= 0 && A[j+1] < A[j]) {
            tmp = A[j];
            A[j] = A[j+1];
            A[j+1] = tmp;

            tmpi = indices[j];
            indices[j] = indices[j+1];
            indices[j+1] = tmpi;

            j--;
        }
    }
}

pick_path_for_ant(int k) {
    printf("choosing path for ant %d\n", k);
    float probs_copy[N];
    copy_from_array(N, p[k], probs_copy);
    int next;
    int i = 0;
    while (i++ < N-1) {
        next = pick_randomly(N, probs_copy);
        printf("%d, ", next);
        probs_copy[next] = 0;
    }
    printf("\n");
}

/*refer to
 * https://stackoverflow.com/questions/3911400/how-to-pass-2d-array-matrix-in-a-function-in-c
 * for a list of methods to pass 2D or 3D arrays */
print_matrix(int n, int m, float p[n][m]) {
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            printf("%4.2f ", p[i][j]);
        }
        printf("\n");
    }
}

print_matrix2(float* p, int n, int m) {
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            printf("%4.2f ", p[i*m + j]);
        }
        printf("\n");
    }
}

print_matrix_int(int* p, int n, int m) {
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            printf("%d ", p[i*m + j]);
        }
        printf("\n");
    }
}

int main() {
    srand(time(NULL));
    initiate();
    int t, k;
    printf("TAU:\n");
    print_matrix2(tau, N, N);

    printf("P:\n");
    print_matrix(N, N, p);

    update_probs();
    printf("P:\n");
    print_matrix(N, N, p);

    pick_path_for_ant(1);
    //for (t=0; t<T; t++) {
    //    //for (k=0; k<M; k++) {
    //    //    pick_path_for_ant(k);
    //    //}
    //}
    //float mardas[] = {3, 1, 3, 5, 10, 6, 7, 8, 15, 100, 134, 123, 131};
    //int indices[13];
    //print_matrix2(mardas, 1, 13);
    //insertion_sort(13, mardas, indices);
    //print_matrix2(mardas, 1, 13);
    //print_matrix_int(indices, 1, 13);
}
