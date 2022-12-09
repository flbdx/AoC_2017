#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import operator

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

def distance(x, y):
    def sign(n):
        return 1 if n >= 0 else -1
    # déplacements en diagonale
    d = min(abs(x), abs(y))
    x -= sign(x) * d
    y -= sign(y) * d
    # déplacements verticaux restants
    d += max(abs(x), abs(y))//2
    return d

dir_offset = {"n": (0,2),
              "s": (0, -2),
              "ne": (1,1),
              "nw": (-1,1),
              "se": (1,-1),
              "sw": (-1,-1)}

def walk(line):
    pos = (0,0)
    
    for direction in line.strip().split(","):
        pos = map(operator.add, pos, dir_offset[direction])
    
    
    pos = tuple(pos)
    return distance(*pos)

def walk_p2(line):    
    pos = (0,0)
    max_d = 0
    
    for direction in line.strip().split(","):
        pos = tuple(map(operator.add, pos, dir_offset[direction]))
        d = distance(*pos)
        if d > max_d:
            max_d = d
    
    return max_d

def p1():
    for line in fileinput.input():
        pos = walk(line)
        print(pos)
p1()

def p2():
    for line in fileinput.input():
        d = walk_p2(line)
        print(d)
p2()
