
# coding: utf-8

# In[2]:


from pycuda import gpuarray
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
import matplotlib.pyplot as plt
import time




with open("new_file.cu", 'r') as f:
    code = f.read()
index = code.find('int main')
code = code[:index]
ker = SourceModule(code)



before_poisson_cu    = ker.get_function('before_poisson_cu')
poisson_solve_1it_cu = ker.get_function('poisson_solve_1it_cu')
after_poisson_cu     = ker.get_function('after_poisson_cu')
sum_ne_cu            = ker.get_function('sum_ne_cu')
update_ne_cu         = ker.get_function('update_ne_cu')


##important note: make sure to convert EVERYTHING into numpy numbers otherwise you're screwed
imax = np.int32(61)
jmax = np.int32(61)
kmax = np.int32(61)
n1 = np.int32(imax+3)
n2 = np.int32(jmax+3)
n3 = np.int32(kmax+3)
qi = np.float32(1.6E-19)
qe = np.float32(-1.6E-19)
kr = np.float32(0)
ki = np.float32(0)
si = np.float32(0)
alpha = np.float32(0)
q     = np.float32(1.6E-19)
pie   = np.float32(3.14159)
tmax  = np.float32(200)


Kb    = np.float32(1.38E-23)
B     = np.float32(0.5)
Te    = np.float32(2.5*11604.5)
Ti    = np.float32(0.025*11604.5)
me    = np.float32(9.109E-31)
mi    = np.float32(6.633E-26)
ki    = np.float32(0.0)
dt    = np.float32(1.0E-14)
h     = np.float32(4.0E-4)
eps0  = np.float32(8.854E-12)
si    = np.float32(0.0)
sf    = np.float32(0.0)


N=np.int32(n1*n2*n3)
iterations = np.int32(40);
tmax = np.int32(1000)

original_ne = np.ones(N).astype(np.float32)*1e-9
original_ni = np.ones(N).astype(np.float32)*1e-9
original_difxne = np.ones(N).astype(np.float32)*1e-9
original_difyne = np.ones(N).astype(np.float32)*1e-9
original_difxni = np.ones(N).astype(np.float32)*1e-9
original_difyni = np.ones(N).astype(np.float32)*1e-9
original_difxyne = np.ones(N).astype(np.float32)*1e-9
original_difxyni = np.ones(N).astype(np.float32)*1e-9
original_Exy = np.ones(N).astype(np.float32)*1e-9
original_fexy = np.ones(N).astype(np.float32)*1e-9
original_fixy = np.ones(N).astype(np.float32)*1e-9
original_g = np.ones(N).astype(np.float32)*1e-9
original_R = np.ones(N).astype(np.float32)*1e-9
original_Ex = np.ones(N).astype(np.float32)*1e-9
original_Ey = np.ones(N).astype(np.float32)*1e-9
original_fex = np.ones(N).astype(np.float32)*1e-9
original_fey = np.ones(N).astype(np.float32)*1e-9
original_fix = np.ones(N).astype(np.float32)*1e-9
original_fiy = np.ones(N).astype(np.float32)*1e-9
original_V = np.ones(N).astype(np.float32)*1e-9
original_L = np.ones(N).astype(np.float32)*1e-9
original_difzne = np.ones(N).astype(np.float32)*1e-9
original_difzni = np.ones(N).astype(np.float32)*1e-9
original_Ez = np.ones(N).astype(np.float32)*1e-9
original_fez = np.ones(N).astype(np.float32)*1e-9
original_fiz = np.ones(N).astype(np.float32)*1e-9

   
nn  =np.float32(10.0/(Kb*Ti)) #neutral density=p/(Kb.T)
nue =np.float32(nn*1.1E-19*np.sqrt(2.55*Kb*Te/me)) # electron collision frequency= neutral density * sigma_e*Vth_e
nui =np.float32(nn*4.4E-19*np.sqrt(2.55*Kb*Ti/mi))
wce =np.float32(q*B/me)
wci =np.float32(q*B/mi)
mue =np.float32(q/(me*nue))
mui =np.float32(q/(mi*nui))
dife=np.float32(Kb*Te/(me*nue))
difi=np.float32(Kb*Ti/(mi*nui))
ki=np.float32(0.00002/(nn*dt))
denominator_e= np.float32((1+wce*wce/(nue*nue)))
denominator_i= np.float32(1+wci*wci/(nui*nui))
# Ta and W are just some constants needed for the iterative method that we have used to solve Poisson eq.
Ta=np.float32(np.arccos((np.cos(pie/imax)+np.cos(pie/jmax)+np.cos(pie/kmax))/3.0))# needs to be float checked
w=np.float32(2.0/(1.0+np.sin(Ta)))
# -----------------------------------------------------------------------------------------------
#Density initialization
# To add multiple Gaussian sources, just simply use the density_initialization function at the (x,y) points that you want
x_position = 15; y_position = 15; z_position = 15;


# In[5]:


for i in range(1, imax-1):
    for j in range(1, jmax-1):
        for k in range(1, kmax-1):
            original_ne[k + n3 * (j + n2 * (i))]= 5.0E14
            original_ni[k + n3 * (j + n2 * (i))]=5.0E14
            
for i in range(18, 22):
    for j in range(18, 22):
        for k in range(20, 40):
            original_ne[k + n3 * (j + n2 * (i))]=5.0E15;
            original_ni[k + n3 * (j + n2 * (i))]=5.0E15;

for i in range(38, 42):
    for j in range(18, 22):
        for k in range(20, 40):
            original_ne[k + n3 * (j + n2 * (i))]=5.0E15;
            original_ni[k + n3 * (j + n2 * (i))]=5.0E15;

for i in range(18, 22):
    for j in range(38, 42):
        for k in range(20, 40):
            original_ne[k + n3 * (j + n2 * (i))]=5.0E15;
            original_ni[k + n3 * (j + n2 * (i))]=5.0E15;

for i in range(38, 42):
    for j in range(38, 42):
        for k in range(20, 40):
            original_ne[k + n3 * (j + n2 * (i))]=5.0E15;
            original_ni[k + n3 * (j + n2 * (i))]=5.0E15;

for k in range(1, kmax+1):
    for j in range(1, jmax+1):
        for i in range(1, imax+1):
            si=si+original_ne[k + n3 * (j + n2 * (i))] ;
si = np.float32(si)


# In[6]:


ne = gpuarray.to_gpu(original_ne)
ni = gpuarray.to_gpu(original_ni)
difxne = gpuarray.to_gpu(original_difxne)
difyne = gpuarray.to_gpu(original_difyne)
difxni = gpuarray.to_gpu(original_difxni)
difyni = gpuarray.to_gpu(original_difyni)
difxyne = gpuarray.to_gpu(original_difxyne)
difxyni = gpuarray.to_gpu(original_difxyni)
Exy = gpuarray.to_gpu(original_Exy)
fexy = gpuarray.to_gpu(original_fexy)
fixy = gpuarray.to_gpu(original_fixy)
g = gpuarray.to_gpu(original_g)
R = gpuarray.to_gpu(original_R)
Ex = gpuarray.to_gpu(original_Ex)
Ey = gpuarray.to_gpu(original_Ey)
fex = gpuarray.to_gpu(original_fex)
fey = gpuarray.to_gpu(original_fey)
fix = gpuarray.to_gpu(original_fix)
fiy = gpuarray.to_gpu(original_fiy)
V = gpuarray.to_gpu(original_V)
L = gpuarray.to_gpu(original_L)
difzne = gpuarray.to_gpu(original_difzne)
difzni = gpuarray.to_gpu(original_difzni)
Ez = gpuarray.to_gpu(original_Ez)
fez = gpuarray.to_gpu(original_fez)
fiz = gpuarray.to_gpu(original_fiz)

g_temp =  gpuarray.to_gpu(g)
ne_temp = gpuarray.to_gpu(ne)
ni_temp = gpuarray.to_gpu(ni)

original_values = np.array([qi,qe,kr,ki,si,sf,alpha,q,pie,Ta,w,eps0,Te,Ti,B,Kb,me,mi,nue,nui,denominator_e,denominator_i,nn,dt,h,wce,wci,mue,mui,dife,difi]).astype(np.float32)
values = gpuarray.to_gpu(original_values)

sf_temp = gpuarray.zeros(1, dtype='float32')


# In[7]:


def test(p = None):
    if p is None:
        p = [V, g, ne]
    p  = [a.get()[5 + (kmax+3) * (5 + (jmax+3) * 5)] for a in p]
    p.append(sf_temp.get()[0])
    return p

grid  = (int(N)//512, 1, 1)
block = (512, 1, 1)

new_ker = SourceModule("""
__global__ void poisson_solve_1it_cu(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, float* V, float* g, float *R, float w, float h, int oddEven) {
    int index_x = threadIdx.x + blockDim.x * blockIdx.x;
    int stride_x = blockDim.x * gridDim.x;
        for (int I = index_x; I < N; I +=stride_x) {
            int k = I % n3;
            int s1 = (I - k) / n3;
            int j = s1 % n2;
            int i = (s1 - j) / n2;
            if (i * j * k == 0 || i >= imax-1 || j >= jmax-1 || k >= kmax-1) continue;
            float r =
                (V[k + n3 * (j + n2 * (i+1))]+
                     V[k + n3 * (j + n2 * (i-1))]+
                     V[k + n3 * (j+1 + n2 * (i))]+
                     V[k + n3 * (j-1 + n2 * (i))]+
                     V[k+1 + n3 * (j + n2 * (i))]+
                     V[k-1 + n3 * (j + n2 * (i))]
                 ) / 6.0 - V[k + n3 * (j + n2 * (i))]- (h*h)*g[k + n3 * (j + n2 * (i))]/6.0;
            R[k + n3 * (j + n2 * (i))] = V[k + n3 * (j + n2 * (i))] + w*r;
        }
}
""")


# In[9]:


new_ker = SourceModule("""
#define _x  ( threadIdx.x + blockIdx.x * blockDim.x )
#define _y  ( threadIdx.y + blockIdx.y * blockDim.y )
#define _z  ( threadIdx.z + blockIdx.z * blockDim.z )
#define _width  ( blockDim.x * gridDim.x )
#define _height ( blockDim.y * gridDim.y  )
#define _depth  ( blockDim.z * gridDim.z  )
#define _xm(x)  ( (x + _width) % _width )
#define _ym(y)  ( (y + _height) % _height )
#define _zm(z)  ( (z + _depth) % _depth )
#define _index(x,y,z)  ( _zm(z)  + _depth * (_ym(y) + _xm(x) * _height) )

__global__ void poisson_out_of_place(int imax, int jmax, int kmax, int n1, int n2, int n3, int N, float* V, float* g, float *R, float w, float h, int oddEven) {
    int x = _x, y = _y, z = _z;
    if (x >= 1  && y >= 1 && z >= 1 && x < imax+1 && y < jmax+1 && z < kmax-1) {
        float r = V[_index(x+1,y,z)]
                 +V[_index(x-1,y,z)]
                 +V[_index(x,y+1,z)]
                 +V[_index(x,y-1,z)]
                 +V[_index(x,y,z+1)]
                 +V[_index(x,y,z-1)];
        r = r/6.0-V[_index(x,y,z)]/6.0 ;//- V[_index(x, y, z)]- (h*h)*g[_index(x,y,z)]/6.0;
        R[_index(x,y,z)]=r;                   
    }
}

""")
poisson_out_of_place = new_ker.get_function("poisson_out_of_place")


# In[11]:


print("starting process...")
grid  = (int(N)//8, int(N)//8, int(N)//8)
block = (8, 8, 8)
s = time.time()
for i in range(10):
    print(i, test([V, R]))
    before_poisson_cu(imax, jmax, kmax, ne, ni, g, g_temp, values, grid=grid, block=block)
    for kk in range(1):#(kk=0; kk<iterations; kk++) {
        poisson_out_of_place(imax, jmax, kmax, n1, n2, n3, N, V, g, R, w, h, np.int32(0), grid=grid, block=block);
        #tmp = V
        #V = R
        #R = tmp
        V[:] = R[:]
    
    after_poisson_cu( imax,  jmax,  kmax,  ne, ni , difxne, difyne, difxni , difyni, difxyne, difxyni, Exy, fexy, fixy, R, Ex, Ey , fex, fey, fix, fiy, V, difzne, difzni, Ez, fez, fiz , values, sf_temp
                     , grid=grid, block=block)
    sum_ne_cu(imax, jmax, kmax, ne, sf_temp, grid=grid, block=block);
    ##sf_temp = gpuarray.sum(ne)
    update_ne_cu(imax, jmax, kmax, ne, ni, sf_temp, si, grid=grid, block=block);
f = time.time()
print("took ", f-s)


# In[69]:


def test():
    p = [V, g, ne]
    p  = [a.get()[5 + (kmax+3) * (5 + (jmax+3) * 5)] for a in p]
    p.append(sf_temp.get())
    return p
test()
