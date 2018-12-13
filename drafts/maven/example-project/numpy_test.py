import numpy as np
import time

N = 10000
a = np.ones((N, N))
b = np.ones((N, N))

now = time.time()
a.dot(b)
print("time taken: ", time.time()-now)
