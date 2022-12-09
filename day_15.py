#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

class Generator(object):
    def __init__(self, state, factor, max_it=40000000):
        self.state = state
        self.factor = factor
        self.max_it = max_it
        self.n = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.n < self.max_it:
            self.state = (self.state * self.factor) % 2147483647
            self.n += 1
            return self.state
        raise StopIteration()

class Generator2(object):
    def __init__(self, state, factor, mask, max_it=5000000):
        self.state = state
        self.factor = factor
        self.mask = mask
        self.max_it = max_it
        self.n = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.n < self.max_it:
            while True:
                self.state = (self.state * self.factor) % 2147483647
                if (self.state & self.mask) == 0:
                    break
            self.n += 1
            return self.state
        raise StopIteration()

def work_p1(state_A, state_B):
    gen_A = Generator(state_A, 16807)
    gen_B = Generator(state_B, 48271)
    
    count = 0
    for va, vb in zip(gen_A, gen_B):
        if ((va ^ vb) & 0xFFFF) == 0:
            count += 1
    return count

def work_p2(state_A, state_B):
    gen_A = Generator2(state_A, 16807, 0b11)
    gen_B = Generator2(state_B, 48271, 0b111)
    
    count = 0
    for va, vb in zip(gen_A, gen_B):
        if ((va ^ vb) & 0xFFFF) == 0:
            count += 1
    return count

def p1():
    with fileinput.input() as inp:
        state_A = int(inp.readline().split(" ")[-1])
        state_B = int(inp.readline().split(" ")[-1])
        print(work_p1(state_A, state_B))
p1()

def p2():
    with fileinput.input() as inp:
        state_A = int(inp.readline().split(" ")[-1])
        state_B = int(inp.readline().split(" ")[-1])
        print(work_p2(state_A, state_B))
p2()
