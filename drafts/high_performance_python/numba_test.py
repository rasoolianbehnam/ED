import numba as nb

import math

@nb.vectorize(target='cpu')
def expon_cpu(x, y):
	return math.exp(x) + math.exp(y)

@nb.vectorize(['float32(float32, float32)'], target='cuda')
def expon_gpu(x, y):
	return math.exp(x) + math.exp(y)


import numpy as np

import time

N = 1000000

niter = 100

a = np.random.rand(N).astype('float32')

b = np.random.rand(N).astype('float32')

# Trigger compilation

expon_cpu(a, b)
expon_gpu(a, b)

# Timing

start = time.time()
for i in range(niter):
    expon_cpu(a, b)
print("CPU:", time.time() - start)

start = time.time()
for i in range(niter):
    expon_gpu(a, b)
print("GPU:", time.time() - start)

# Output:
