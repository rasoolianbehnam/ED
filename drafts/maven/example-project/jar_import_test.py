import sys
import os
import time
print sys.version

root = "./target/dependency"
for folder, subfolders, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.jar'):
            full_path = "%s/%s/%s"%(os.getcwd(), root, filename)
            #print full_path
            sys.path.append(full_path)
from org.nd4j.linalg.factory import Nd4j


N = 10000
a = Nd4j.rand(N, N)
b = Nd4j.rand(N, N)
now = time.time()
a.mmul(b)
print "time taken: ", time.time() - now
