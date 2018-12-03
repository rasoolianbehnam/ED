import numpy as np

def check_connectivity(mat):
    n, m = mat.shape
    assert n == m
    mat = mat * 1
    diag = range(n)
    mat[diag, diag] = 1
    print(mat)
    mat = np.linalg.matrix_power(mat, n);
    print(np.sum((mat != 0).sum(axis=0) == m) > 0)

def check_no_cycle(mat):
    n, m = mat.shape
    assert n == m
    a = mat.sum(axis=0) == 1
    b = mat.sum(axis=1) == 1
    print((a.sum() == n) & (b.sum() == n))

if __name__=="__main__":
    a = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0]])
    b = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0]])
    c = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0]])

    check_connectivity(a)
    check_no_cycle(a)
    #check_connectivity(b)

