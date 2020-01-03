#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from math import sqrt
from collections import defaultdict

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

def work_p1(v):
    def coordinates(v):
        # numéro de la couche dans laquelle se trouve v
        n = (sqrt(v - 1)-1) // 2 + 1
        # largeur couche
        w = 2*n + 1
        # demi largeur
        h = (w - 1) // 2
        
        # coins
        corners = [w * w - n * (w - 1) for n in range(0, 5)]
        
        x, y = None, None
        if v >= corners[1]:
            y = h
            x = v - corners[1] - h
        elif v >= corners[2]:
            x = -h
            y = v - corners[2] - h
        elif v >= corners[3]:
            y = -h
            x = -(v - corners[3] - h)
        else:
            x = h
            y = -(v - corners[4] - h)
        
        
        return (x, y)
        
    x, y = coordinates(v)
    return int(abs(x) + abs(y))

def work_p2(target):
    grid = defaultdict(lambda: 0)
    
    grid[(0,0)] = 1
    
    n = 1
    while True:
        w = 2*n + 1
        h = (w - 1) // 2
        corners = [w * w - n * (w - 1) for n in range(0, 5)]
        
        x, y = h, h - 1
        for v in range(corners[4] + 1, corners[0] + 1):
            grid[(x, y)] = \
                grid[(x - 1, y - 1)] + grid[(x, y - 1)] + grid[(x + 1, y - 1)] + \
                grid[(x - 1, y)]                        + grid[(x + 1, y)] + \
                grid[(x - 1, y + 1)] + grid[(x, y + 1)] + grid[(x + 1, y + 1)]
            
            if grid[(x, y)] > target:
                return grid[(x, y)]
            
            if v >= corners[1]:
                x += 1
            elif v >= corners[2]:
                y += 1
            elif v >= corners[3]:
                x -= 1
            else:
                y -= 1
        
        n += 1
    

def test_p1():
    assert work_p1(1) == 0
    assert work_p1(12) == 3
    assert work_p1(23) == 2
    assert work_p1(1024) == 31
test_p1()

def p1():
    for line in fileinput.input():
        print(work_p1(int(line)))
p1()

def p2():
    for line in fileinput.input():
        print(work_p2(int(line)))
p2()
