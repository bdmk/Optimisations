#!/usr/bin/python
# coding: UTF-8
#
# Author: Dawid Laszuk
# Contact: laszukdawid@gmail.com
#          d.laszuk@pgr.reading.ac.uk
#
# Feel free to contact for any information.
#
# Last update: 10/03/2015
#
# You can cite this code by referencing:
#   D. Laszuk, "Python implementation of Particle 
#   Swarm Optimisation," 2015-,
#   [Online] Available: http://www.laszukdawid.com/codes
#
# LICENCE:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


from scipy.integrate import ode
import numpy as np
import pylab as py


class Particle:
    def __init__(self, dim=10):
        pass
        self.__dim = dim

class PSO:
    def __init__(self, func, bounds, initPos=None, nPart=10):
        
        # number of particles in swarm
        self.nPart = 100
        
        # Params
        self.epsError = 1.
        self.maxGen = 500
        
        self.w = 0.2
        self.phiP = 0.2
        self.phiG = 0.1
                        
        # Function to be minimised
        self.problem = func

        # Set up boundary values
        self.minBound = np.array(bounds[0])
        self.maxBound = np.array(bounds[1])

        self.dim = len(bounds[0])
        
        # Initial positions
        if initPos!=None:
            self.initPos = np.array(initPos).reshape((-1,self.dim))        
        else:
            self.initPos = initPos


    def __initPart(self):
        """Initiate particles.
        """
         
        # Create particles
        self.Particles = []
        for i in range(self.nPart):
            self.Particles.append( Particle(self.dim) )
        
        # Initiate pos and fit for particles
        for part in self.Particles:
            
            # Initial position
            if self.initPos == None:
                part.pos = np.random.random(self.dim)*self.maxBound - self.minBound
            else:
                part.pos = self.initPos[0,:]
                self.initPos = np.delete(self.initPos, 0,0)
                
                # If nothing left on initial pos
                if len(self.initPos) == 0: self.initPos = None
            
            # Initial velocity
            part.vel = np.random.random(self.dim)*(self.maxBound - self.minBound)
            part.vel *= [-1., 1.][np.random.random()>0.5]
            
            # Initial fitness
            part.fitness = self.problem(part.pos)
            part.bestFit = part.fitness
            part.bestPos = part.pos
        
        # Global best fitness
        self.globBestFit = self.Particles[0].fitness
        self.globBestPos = self.Particles[0].pos
        for part in self.Particles:
            if part.fitness < self.globBestFit:
                self.globBestFit = part.fitness
                self.globBestPos = part.pos
    
    def update(self):
        
        for part in self.Particles:
            
            # Gen param
            rP, rG = np.random.random(2)
            
            w, phiP, phiG = self.w, self.phiP, self.phiG
            
            # Update velocity
            v, pos = part.vel, part.pos
            part.vel = self.w*v + phiP*rP*(part.bestPos-pos) + phiG*rG*(self.globBestPos-pos)
            
            # New position
            part.pos += part.vel
            
            # If pos outside bounds
            if np.any(part.pos<self.minBound):
                idx = part.pos<self.minBound
                part.pos[idx] = self.minBound[idx]
            if np.any(part.pos>self.maxBound):
                idx = part.pos>self.maxBound
                part.pos[idx] = self.maxBound[idx]
            
            # New fitness
            part.fitness = self.problem(part.pos)
        
        # Global and local best fitness
        for part in self.Particles:
            
            # Comparing to local best
            if part.fitness < part.bestFit:
                part.bestFit = part.fitness
            
            # Comparing to global best
            if part.fitness < self.globBestFit:
                self.globBestFit = part.fitness
                self.globBestPos = part.pos
            
    def finished(self):
        """What is returned when searched is finished.
        """
        
        return self.globBestPos, self.globBestFit
    
    def optimize(self):
        """ Optimisation function.
            Before it is run, initial values should be set.
        """
        
        # Initiate particles
        self.__initPart()
        
        idx = 0
        while(idx < self.maxGen):
            print "Gen: {}/{}  -- best = {}".format(idx, self.maxGen, self.globBestFit)
            
            # Perform search
            self.update()
            
            # Acceptably close to solution
            if self.globBestFit < self.epsError:
                return self.finished()
            
            # next gen
            idx += 1
        
        # Search finished
        return self.finished()
        

#################################

if __name__ == "__main__":
    N = 1000
    t = np.linspace(-2, 2, N)

    S = 4*t*np.cos( 4*np.pi*t**2) * np.exp(-3*t**2)
    S+= (np.random.random(N)-0.5)*0.05

    rec = lambda a: a[0]*t*np.sin(a[1]*np.pi*t**2 +a[2])*np.exp(-a[3]*t**2)
    minProb = lambda a: np.sum(np.abs(S-rec(a)))

    numParam = 4
    bounds = ([0]*numParam, [10]*numParam)
    
    pso = PSO(minProb, bounds)
    bestPos, bestFit = pso.optimize()

    print 'bestFit: ', bestFit
    print 'bestPos: ', bestPos

    ############################
    # Visual results representation
    py.figure()
    py.plot(t, S, 'b')
    py.plot(t, rec(bestPos), 'r')
    py.xlabel("Time")
    py.ylabel("Amp")
    py.title("Input (blue) and reconstuction (red)")

    py.savefig('fit',dpi=120)
    py.show()
