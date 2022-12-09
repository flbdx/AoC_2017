#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

class Component(object):
    def __init__(self, line):
        self.ports = list(map(int, line.strip().split("/")))
    
    def is_starting_compo(self):
        return 0 in self.ports
    
    def __repr__(self):
        return "/".join(repr(p) for p in self.ports)

class Bridge(object):
    def __init__(self):
        self.bridge = []
        self.free_port = 0
    
    def is_compat(self, compo):
        return self.free_port in compo.ports
    
    def add(self, compo):
        next_free_port = compo.ports[0] if compo.ports[0] != self.free_port else compo.ports[1]
        self.bridge.append(compo)
        self.free_port = next_free_port
    
    def strength(self):
        return sum(compo.ports[0] + compo.ports[1] for compo in self.bridge)

    def __len__(self):
        return len(self.bridge)
    
    def copy(self):
        b = Bridge.__new__(Bridge)
        b.bridge = [p for p in self.bridge]
        b.free_port = self.free_port
        return b

    def __repr__(self):
        return repr(self.bridge)

def work(lines):
    components = deque()
    for line in lines:
        components.append(Component(line))
    
    
    max_strength = 0
    max_length = 0
    strengths_max_length = []
    
    queue = [(Bridge(), components)]
    while len(queue) != 0:
        bridge, compos = queue.pop(0)
        
        s = bridge.strength()
        if s > max_strength:
            max_strength = s
        l = len(bridge)
        if l > max_length:
            max_length = l
            strengths_max_length = [s]
        elif l == max_length:
            strengths_max_length.append(s)
        
        for i in range(len(compos)):
            c = compos[0]
            if bridge.is_compat(c):
                bridge_ = bridge.copy()
                bridge_.add(c)
                compos_ = compos.copy()
                compos_.popleft()
                queue.append((bridge_, compos_))
            compos.rotate(1)
        
    return (max_strength, max(strengths_max_length))

def p1_2():
    print(work(fileinput.input()))
p1_2()
        
