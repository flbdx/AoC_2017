#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

class Cpu(object):
    def __init__(self):
        self.regs = {}
        self.operations = {
            "inc":  lambda x,y: x+y,
            "dec":  lambda x,y: x-y,
            ">":    lambda x,y: x>y,
            "<":    lambda x,y: x<y,
            ">=":   lambda x,y: x>=y,
            "<=":   lambda x,y: x<=y,
            "==":   lambda x,y: x==y,
            "!=":   lambda x,y: x!=y
        }
        self.max_v = None
    
    def run(self, lines):
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            
            tokens = line.split(" ")
            reg = tokens[0]
            op = self.operations[tokens[1]]
            value = int(tokens[2])
            cmp_reg = self.regs.get(tokens[4], 0)
            cmp_op = self.operations[tokens[5]]
            cmp_value = int(tokens[6])
            
            if cmp_op(cmp_reg, cmp_value):
                self.regs[reg] = op(self.regs.get(reg, 0), value)
            
            m = max(self.regs.values()) if len(self.regs) > 0 else 0
            if self.max_v is None or m > self.max_v:
                self.max_v = m
    
    def res_p1(self):
        return max(self.regs.values())
    
    def res_p2(self):
        return self.max_v

def test_p1():
    lines="""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".splitlines()
    cpu = Cpu()
    cpu.run(lines)
    assert cpu.res_p1() == 1
test_p1()

def p1():
    cpu = Cpu()
    cpu.run(fileinput.input())
    print(cpu.res_p1())
p1()

def p2():
    cpu = Cpu()
    cpu.run(fileinput.input())
    print(cpu.res_p2())
p2()
            
