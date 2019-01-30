
# coding: utf-8

# In[1]:


class Particle:
   def __init__(self, x, y, ang_vel):
       self.x = x
       self.y = y
       self.ang_vel = ang_vel


# In[2]:


class ParticleSimulator:
   def __init__(self, particles):
       self.particles = particles
   def evolve(self, dt):
       timestep = 0.00001
       nsteps = int(dt/timestep)
       for i in range(nsteps):
           for p in self.particles:
               # 1. calculate the direction
               norm = (p.x**2 + p.y**2)**0.5
               v_x = -p.y/norm
               v_y = p.x/norm
               # 2. calculate the displacement
               d_x = timestep * p.ang_vel * v_x
               d_y = timestep * p.ang_vel * v_y
               p.x += d_x
               p.y += d_y
               # 3. repeat for all the time steps


# In[6]:


from random import uniform
def benchmark():
    particles = [Particle(uniform(-1.0, 1.0),
                            uniform(-1.0, 1.0),
                            uniform(-1.0, 1.0))
                for i in range(1000)]
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)
if __name__ == '__main__':
   benchmark()

