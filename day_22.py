#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def turn_left(self):
        return Direction((self.value - 1) % 4)
    def turn_right(self):
        return Direction((self.value + 1) % 4)
    def turn_back(self):
        return Direction((self.value + 2) % 4)
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3
    
    def evolve(self):
        return State((self.value + 1) % 4)

class Grid(object):
    def __init__(self, lines):
        self.grid = {}
        
        max_y = 0
        max_x = 0
        for y, line in enumerate(lines):
            max_y = max(max_y, y)
            for x, c in enumerate(line):
                max_x = max(max_x, x)
                if c == "#":
                    self.grid[x, y] = State.INFECTED
                    
        
        self.virus_p = (max_x // 2, max_y // 2)
        self.virus_d = Direction.UP
    
    def virus_step_p1(self):
        state = self.grid.get(self.virus_p, State.CLEAN)
        if state == State.INFECTED:
            self.virus_d = self.virus_d.turn_right()
            state = State.CLEAN
        else:
            self.virus_d = self.virus_d.turn_left()
            state = State.INFECTED
        self.grid[self.virus_p] = state
        self.virus_p = self.virus_d.next(self.virus_p)
        return state

    def virus_step_p2(self):
        state = self.grid.get(self.virus_p, State.CLEAN)
        if state == State.CLEAN:
            self.virus_d = self.virus_d.turn_left()
        elif state == State.WEAKENED:
            pass
        elif state == State.INFECTED:
            self.virus_d = self.virus_d.turn_right()
        else:
            self.virus_d = self.virus_d.turn_back()
        state = state.evolve()
        self.grid[self.virus_p] = state
        self.virus_p = self.virus_d.next(self.virus_p)
        return state

def p1():
    grid = Grid(fileinput.input())
    r = sum(grid.virus_step_p1() == State.INFECTED for n in range(10000))
    print(r)
p1()

def p2():
    grid = Grid(fileinput.input())
    r = sum(grid.virus_step_p2() == State.INFECTED for n in range(10000000))
    print(r)
p2()
    
