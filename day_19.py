#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum

if len(sys.argv) == 1:
    sys.argv += ["input_19"]

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def turn_left(self):
        return Direction((self.value - 1) % 4)
    def turn_right(self):
        return Direction((self.value + 1) % 4)
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

class Network(object):
    def __init__(self, lines):
        self.world = {}
        self.start_pos = None

        for y, line in enumerate(lines):
            line = line.rstrip()
            for x, c in enumerate(line):
                if c == ' ':
                    continue
                else:
                    self.world[x, y] = c

        # trouver la position de départ
        max_x = max(p[0] for p in self.world.keys())
        for x in range(max_x + 1):
            v = self.world.get((x, 0), None)
            if v == '|':
                self.start_pos = (x, 0)
                break

    def walk(self):
        letters = []
        p = self.start_pos
        direction = Direction.DOWN
        
        steps = 0
        while True:
            v = self.world.get(p, None)
            if v == None:
                break
            elif v in '|-':
                pass
            elif v == '+':
                for test_d in [direction.turn_left(), direction.turn_right()]:
                    test_v = self.world.get(test_d.next(p), None)
                    if test_v != None and test_v != '|' and test_d in [Direction.RIGHT, Direction.LEFT]:
                        direction = test_d
                        break
                    elif test_v != None and test_v != '-' and test_d in [Direction.UP, Direction.DOWN]:
                        direction = test_d
                        break
            else:
                letters.append(v)
            
            steps += 1
            p = direction.next(p)
        
        return ("".join(letters), steps)


def p12():
    net = Network(fileinput.input())
    print(net.walk())
p12()
