#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from types import SimpleNamespace

class Particle(SimpleNamespace): pass

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

class Simu(object):
    def __init__(self, lines):
        self.particles = {}
        for n, line in enumerate(lines):
            #result = re.match("(\w+) \((\d+)\)", line)
            #p=<663,1944,-2188>, v=<94,281,-312>, a=<-5,-25,21>
            result = re.match("p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>", line)
            p=[int(result.group(v)) for v in range(1,4)]
            v=[int(result.group(v)) for v in range(4,7)]
            a=tuple(int(result.group(v)) for v in range(7,10))
            
            self.particles[n] = (Particle(n=n, p=p, v=v, a=a))

    def manhattan(p):
        return sum(map(abs, p.p))

    def run_p1(self):
        long_run_best_p = None
        long_run = 0
        
        while long_run != 500:
            best_d = None
            best_p = None
            for particle in self.particles.values():
                particle.v = tuple(particle.v[i] + particle.a[i] for i in range(3))
                particle.p = tuple(particle.p[i] + particle.v[i] for i in range(3))
                d = Simu.manhattan(particle)
                if best_d == None or d < best_d:
                    best_d = d
                    best_p = particle
            if long_run_best_p == best_p:
                long_run += 1
            else:
                long_run_best_p = best_p
                long_run = 0
        
        return long_run_best_p
    
    def run_p2(self):
        long_run_n_particles = None
        long_run = 0
        
        while long_run != 500:
            positions = {}
            
            for particle in self.particles.values():
                particle.v = tuple(particle.v[i] + particle.a[i] for i in range(3))
                particle.p = tuple(particle.p[i] + particle.v[i] for i in range(3))
                a = positions.get(particle.p, [])
                a.append(particle)
                positions[particle.p] = a
            
            for pos, a in positions.items():
                if len(a) > 1:
                    for p in a:
                        del(self.particles[p.n])

            if long_run_n_particles == None or len(self.particles) < long_run_n_particles:
                long_run_n_particles = len(self.particles)
                long_run = 0
            else:
                long_run += 1
        
        return len(self.particles)

def p1():
    s = Simu(fileinput.input())
    print(s.run_p1())
p1()

def p2():
    s = Simu(fileinput.input())
    print(s.run_p2())
p2()

