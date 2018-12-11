import numpy as np
import time

N = 10000
a = np.random.rand(N, N)
b = np.random.rand(N, N)

now = time.time()
a.dot(b)
print("time taken: ", time.time()-now)
