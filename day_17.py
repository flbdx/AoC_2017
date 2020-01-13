#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

class Spin(object):
    def __init__(self, step):
        self.step = step
        self.mem = deque([0])
        self.pos = 0
        self.v = 1
    
    def spin(self, steps=1):
        for v in range(self.v, self.v + steps):
            self.mem.rotate(-self.step)
            self.mem.append(v)
        self.v += steps
    
def test_p1():
    steps = 2017
    s = Spin(3)
    s.spin(steps)
    idx = s.mem.index(steps)
    assert s.mem[(idx + 1) % (steps + 1)] == 638
test_p1()

def p1():
    with fileinput.input() as inp:
        steps = 2017
        s = Spin(int(inp.readline()))
        s.spin(steps)
        idx = s.mem.index(steps)
        print(s.mem[(idx + 1) % (steps + 1)])
p1()

def fastSpin_p2(step, n_spins):
    pos = 0
    res = 0
    for i in range(1, n_spins + 1):
        pos = ((pos + step) % i) + 1
        if pos == 1:
            res = i
    return res

def p2():
    with fileinput.input() as inp:
        print(fastSpin_p2(int(inp.readline()), 50000000))
p2()
