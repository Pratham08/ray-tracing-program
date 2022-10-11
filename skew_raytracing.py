from fnmatch import translate
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

#define properties and parameters of the ray
class RAY:
    def __init__(self,x0,y0,z0,k0,l0,m0,zf):
        self.x = x0
        self.y = y0
        self.z = z0
        self.k = k0
        self.l = l0
        self.m = m0
        self.zf = zf
        
#a class to which defines surface properties and parameters
class Surface:
    def __init__(self,zs,R):
        self.z = zs
        self.r = R
    
    def lens_surface(self):
        #todo: plot the surface of the lens in 3d
        return

#tranlation from current position to vertex plane of the lens surface  
def translate1(ray,surf,n,i):
    t = surf.z - ray.z
    if t>0:
        D = (surf.z-ray.z)/ray.m
        ray.x = ray.x + D*ray.k
        ray.y = ray.y + D*ray.l
        ray.z = surf.z
    else:
        raise Exception("Check the coordinates!")

#translation from the end surface to imaging plane
def translate2(ray,n,i):
    t = ray.zf - ray.z
    if t>0:
        D = (ray.zf-ray.z)/ray.m
        ray.x = ray.x + D*ray.k
        ray.y = ray.y + D*ray.l
        ray.z = ray.zf
    else:
        raise Exception("Check the coordinates!")

#translation from vertex plane to lens surface 
# and refraction atlens surface
def translate_refract(ray,surf,n,i):
    H = (ray.x**2 + ray.y**2)/surf.r
    B = ray.m - (ray.y*ray.l + ray.x*ray.k)
    n_cosI = n[i]*(((B/n[i])**2 - H/surf.r)**0.5)
    A_n = H/(B - n_cosI)
    #translation
    ray.x = ray.x + A_n*ray.k
    ray.y = ray.y + A_n*ray.l
    ray.z = ray.z + A_n*ray.m
    n1_cosR = n[i+1]*((n_cosI/n[i+1])**2 - (n[i]/n[i+1])**2 + 1)**0.5
    zeta = n1_cosR - n_cosI
    #refraction
    ray.k = ray.k - ray.x*zeta/surf.r
    ray.l = ray.l - ray.y*zeta/surf.r
    ray.m = ray.m - ((ray.z/surf.r)-1)*zeta

#if the current file is executed following will be executed
if __name__ == '__main__':
    #refractive index of the region
    n = [1,1.5,1]
    #define surface array
    s = [Surface(10,20),Surface(15,44)]
    #ray initiation
    ray = RAY(0,0,0,0,1/2,(3**0.5)/2,50)
    i = 0
    x = [ray.x]
    y = [ray.y]
    z = [ray.z]
    #mapping process
    while ray.z < ray.zf:
        if (i<(len(n)-1)):
            translate1(ray,s[i],n,i)
            translate_refract(ray,s[i],n,i)
            i+=1
            x.append(ray.x)
            y.append(ray.y)
            z.append(ray.z)
        else:
            translate2(ray,n,i)
            x.append(ray.x)
            y.append(ray.y)
            z.append(ray.z)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, projection='3d')
    #plot the ray path
    ax.plot(x,y,z)
    #plt.show()
    print(x,y,z)
    
            
