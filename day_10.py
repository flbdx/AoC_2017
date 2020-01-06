#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

class Hash(object):
    def __init__(self, size=256):
        self.state = deque(range(size))
        self.pos = 0
        self.skip = 0
    
    def round(self, lengths):
        for l in lengths:
            self.state.rotate(-self.pos)
            rev = deque()
            for i in range(l):
                rev.appendleft(self.state.popleft())
            rev.extend(self.state)
            self.state = rev
            self.state.rotate(self.pos)
            self.pos += l + self.skip
            self.skip += 1
    
    def hash(self, data):
        lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
        
        for r in range(64):
            self.round(lengths)
        
        h = ""
        ite = iter(self.state)
        for blk in range(16):
            v = 0
            for i in range(16):
                v ^= next(ite)
            h += "%0.2x" % v
        
        return h
        
            
def test_p1():
    h = Hash(5)
    h.round([3, 4, 1, 5])
    assert h.state[0] * h.state[1] == 12
test_p1()

def p1():
    for line in fileinput.input():
        h = Hash()
        h.round([int(w) for w in line.split(",")])
        print(h.state[0] * h.state[1])
p1()

def test_p2():
    h = Hash()
    assert h.hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
    h = Hash()
    assert h.hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
test_p2()

def p2():
    for line in fileinput.input():
        h = Hash()
        print(h.hash(line.strip()))
p2()
