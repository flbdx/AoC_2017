#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

class Danse(object):
    def __init__(self, line):
        self.programs = [chr(ord('a') + c) for c in range(16)]
        self.instructions = []
        
        for sequence in line.split(","):
            op = sequence[0]
            if op == 's':
                v1 = int(sequence[1:])
                self.instructions.append((self.do_spin, v1))
            elif op == 'x':
                v1, v2 = map(int, tuple(sequence[1:].split("/")))
                self.instructions.append((self.do_exchange, v1, v2))
            elif op == 'p':
                v1, v2 = tuple(sequence[1:].split("/"))
                self.instructions.append((self.do_partner, v1, v2))
            
    def do_spin(self, v):
        self.programs = self.programs[-v:] + self.programs[:-v]
    
    def do_exchange(self, v1, v2):
        self.programs[v1], self.programs[v2] = self.programs[v2], self.programs[v1]
    
    def do_partner(self, v1, v2):
        for idx1 in range(len(self.programs)):
            if self.programs[idx1] == v1:
                for idx2 in range(idx1 + 1, len(self.programs)):
                    if self.programs[idx2] == v2:
                        self.programs[idx1], self.programs[idx2] = self.programs[idx2], self.programs[idx1]
                        return
            elif self.programs[idx1] == v2:
                for idx2 in range(idx1 + 1, len(self.programs)):
                    if self.programs[idx2] == v1:
                        self.programs[idx1], self.programs[idx2] = self.programs[idx2], self.programs[idx1]
                        return
    
    def run(self):
        for inst in self.instructions:
            inst[0](*inst[1:])

def p1():
    for line in fileinput.input():
        d = Danse(line)
        d.run()
        print("".join(d.programs))
p1()

def p2():
    for line in fileinput.input():
        d = Danse(line)
        ref = d.programs.copy()
        l = 1
        max_l = 1000000000
        while l < max_l:
            d.run()
            if d.programs == ref:
                break
            l += 1
        rem = max_l % l
        for l in range(rem):
            d.run()
        print("".join(d.programs))
p2()
