#include <pthread.h>

#define N 4
int total_sum = 0;
int A[N][N];
struct semaphore *s;

void* sum_row(void* arg) {
    int sum = 0;
    int j, row;
    row = (int) arg;
    pthread_t me = pthread_self();
    for (j=0; j<N; j++) {
        sum += A[row][j];
    }
    sem_wait(s);
        total_sum += sum;
    sem_post(s);
    printf("Thread %d [%lu] done: sum = %d\n",
            row, me, sum);
}

int main() {
    sem_init(s, 1);
    pthread_t threads[N];
    int i,j;
    void* status;
    for (i=0; i<N; i++) {
        for (j=0;j<N;j++) {
            A[i][j] = i*N+j+1;
            printf("%4d ", A[i][j]);
        }
        printf("\n");
    }
    printf("[MAIN] Creating %d threads...\n", N);
    for (i=0; i<N; i++) {
        pthread_create(&(threads[i]), NULL, sum_row, i/***/);
        /**cannot use pointer to i (*i) since all threads
         * will share the same pointer*/
    }
    printf("[MAIN] Try to join threads\n");
    for (i=0; i<N;i++) {
        pthread_join(A[i], &status);
        printf("[Main] joined with %d [%lu]: status: %d\n",
                i, threads[i], (int) status);
    }
    printf("Total sum = %d\n", total_sum);
}
