import numpy as np
import matplotlib.pyplot as plt
import math

class RAY:
    def __init__(self,stop,angle):
        self.x = 0
        self.y = 0
        self.alpha = angle*math.pi/180
        self.xf = stop
 
#a class to which defines surface properties and parameters   
class surface:
    def __init__(self,r1,x,aperature):
        self.r1 = r1
        self.x = x
        self.aperature = aperature
        
    def s1(self):
        if self.r1>0:
            dtheta = 0.001
            C1 = self.x + self.r1
            theta = math.asin(self.aperature/self.r1)
            N = math.floor(2*theta/dtheta)
            theta_M = np.linspace(-theta,theta,N)
            x1 = C1 - self.r1*np.cos(theta_M)
            y1 = self.r1*np.sin(theta_M)   
            return x1,y1,theta_M 
        elif self.r1<0:
            dtheta = 0.001
            self.r1 *= -1
            C1 = self.x-self.r1
            theta = math.asin(self.aperature/self.r1)
            N = math.floor(2*theta/dtheta)
            theta_M = np.linspace(-theta,theta,N)
            x1 = C1 + self.r1*np.cos(theta_M)
            y1 = self.r1*np.sin(theta_M)
            return x1,y1,theta_M
        else:
            #todo
            return 
    
    def chk_proximity(self,x,y):
        x1,y1,theta_M = self.s1()
        for i in range(len(x1)):
            if x1[i]>x-0.005 and x1[i]<x+0.005:
                if y1[i] > y-0.005 and y1[i]<0.005+y:
                    return theta_M[i],True
        return 0,False

#performs refraction operation at a surface with snells law
def refraction(alpha,theta,surf,n,s):
    if alpha>0:
        #return math.asin(n[0]*math.sin(-theta+alpha)/n[1])-theta
        #plt.ylabel(f'{n[0]} {n[1]} {round(theta,3)} {round(alpha,3)}')
        #plt.xlabel(math.asin(n[0]*math.sin(-theta+alpha)/n[1])-theta)
        if s[surf].r1>0 and n[surf]<n[surf+1]:
            plt.xlabel(theta)
            return (math.asin(n[surf]*math.sin(-theta+alpha)/n[surf+1])-theta)
        ##########todo
        #plt.ylabel(theta)
        #return -1*alpha
    else:
        return -math.asin(n[surf]*math.sin(theta-alpha)/n[surf+1])+theta

#performs ray-tracing and calls a function chk_proximity() to detect surfaces        
def ray_tracing(ray,n,s):
    X = [ray.x]
    Y = [ray.y]
    is_call = True
    surf = 0
    while ray.x<ray.xf:
        if is_call:
            theta,is_there = s[surf].chk_proximity(ray.x,ray.y)
        else:
            is_there = False
        if is_there:
            X.append(ray.x)
            Y.append(ray.y)
            ray.alpha = refraction(ray.alpha,theta,surf,n,s)
            surf += 1
            if surf>len(s)-1:
                is_call = False
        ray.x += 0.01
        ray.y += 0.01*math.tan(ray.alpha)
    X.append(ray.x)
    Y.append(ray.y)   
    return X,Y     
  
#perform main operations of ray tracing in order      
if __name__ == '__main__':
    #define the refractive index of the system sequentially
    n = [1,2.1,1]
    #a ray object with specifed parameters (final imaging plane position, initial angle)
    ray = RAY(30,1)
    # second ray object for ray 2
    ray1 = RAY(30,9)
    #s = [surface(10,2,4,5),surface(-10,3,7,5)]
    # an array of surfaces
    s = [surface(10,15,5),surface(-10,18,5)] #radii,position,aperature
    #s2 = surface(10,3,7,5)
    for i in range(len(s)):
        x1,y1,theta_M = s[i].s1()
        plt.plot(x1,y1)
    #x2,y2,theta_M2 = s[1].s1()
    #plot surface 1
    X,Y = ray_tracing(ray,n,s)
    #plot surface 2
    X1,Y1 = ray_tracing(ray1,n,s)
    plt.plot(X,Y)
    plt.plot(X1,Y1)
    #plt.plot(x2,y2)
    plt.plot([0,ray.xf],[0,0])
    plt.show()
    
        
        
    
