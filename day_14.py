#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

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
    
    def hash_bin(self, data):
        lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
        
        for r in range(64):
            self.round(lengths)
        
        h = []
        ite = iter(self.state)
        for blk in range(16):
            v = 0
            for i in range(16):
                v ^= next(ite)
            h.append(v)
        
        return h
    
hamming_weight = {v:bin(v).count("1") for v in range(256)}

def work_p1(keyword):
    global hamming_weight
    weight = 0
    
    for r in range(128):
        key = keyword + "-" + repr(r)
        h = Hash()
        h = h.hash_bin(key)
        for v in h:
            weight += hamming_weight[v]
    return weight

def work_p2(keyword):
    grid = {}
    
    for r in range(128):
        key = keyword + "-" + repr(r)
        h = Hash()
        h = h.hash(key)
        h = "{0:0128b}".format(int(h, 16))
        
        for c in range(128):
            grid[r, c] = 0 if h[c] == "1" else None
    
    label = 0
    queue = []
    for r in range(128):
        for c in range(128):
            cell = grid[r,c]
            if cell == None or cell > 0:
                continue
            label += 1
            queue.append((r, c))
            while len(queue) != 0:
                _r, _c = queue.pop()
                grid[_r, _c] = label
                if _r > 0:
                    if grid[_r - 1, _c] == 0:
                        queue.append((_r - 1, _c))
                if _r < 127:
                    if grid[_r + 1, _c] == 0:
                        queue.append((_r + 1, _c))
                if _c > 0:
                    if grid[_r, _c - 1] == 0:
                        queue.append((_r, _c - 1))
                if _c < 127:
                    if grid[_r, _c + 1] == 0:
                        queue.append((_r, _c + 1))
    
    return label

def p1():
    for line in fileinput.input():
        print(work_p1(line.strip()))
p1()

def p2():
    for line in fileinput.input():
        print(work_p2(line.strip()))
p2()
