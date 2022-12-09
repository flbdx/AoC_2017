#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import defaultdict
import queue
import threading

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

class Copro(object):
    def __init__(self, lines):
        self.instructions = []
        self.regs = defaultdict(lambda: 0)
        self.ip = 0
        
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            
            words = line.split(" ")
            
            if words[0] == "set":
                self.instructions.append((self.do_set, words[1:]))
            elif words[0] == "sub":
                self.instructions.append((self.do_sub, words[1:]))
            elif words[0] == "mul":
                self.instructions.append((self.do_mul, words[1:]))
            elif words[0] == "jnz":
                self.instructions.append((self.do_jnz, words[1:]))
    
    def op_value(self, op):
        v = None
        try:
            v = int(op)
        except:
            v = self.regs[op]
        return v
    
    #set X Y sets register X to the value of Y.
    def do_set(self, op1, op2):
        self.regs[op1] = self.op_value(op2)
        self.ip += 1
    
    #sub X Y decreases register X by the value of Y.
    def do_sub(self, op1, op2):
        self.regs[op1] -= self.op_value(op2)
        self.ip += 1
        
    #mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    def do_mul(self, op1, op2):
        self.regs[op1] *= self.op_value(op2)
        self.ip += 1
    
    #jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
    def do_jnz(self, op1, op2):
        if self.op_value(op1) != 0:
            self.ip += self.op_value(op2)
        else:
            self.ip += 1
    
    def run(self, debug=False, max_instructions=-1):
        total_instruction = 0
        while max_instructions == -1 or total_instruction < max_instructions:
            instruction = self.instructions[self.ip]
            if debug:
                print("{0}\t{1}\t{2}\t{3}".format(self.ip, instruction[0].__name__, repr(instruction[1]), repr(self.regs.items())))
            instruction[0](*instruction[1])
            total_instruction += 1
            if self.ip < 0 or self.ip >= len(self.instructions):
                break

def p1():
    class CoproP1(Copro):
        def __init__(self, lines):
            super(CoproP1, self).__init__(lines)
            self.n_muls = 0
        def do_mul(self, op1, op2):
            self.n_muls += 1
            return super(CoproP1, self).do_mul(op1, op2)
    d = CoproP1(fileinput.input())
    d.run()
    print(d.n_muls)
p1()

#0    set b 81
#1    set c b
#2    jnz a 2
#3    jnz 1 5
#4    mul b 100
#5    sub b -100000
#6    set c b
#7    sub c -17000
#8    set f 1
#9    set d 2
#10   set e 2
#11   set g d
#12   mul g e
#13   sub g b
#14   jnz g 2
#15   set f 0
#16   sub e -1
#17   set g e
#18   sub g b
#19   jnz g -8
#20   sub d -1
#21   set g d
#22   sub g b
#23   jnz g -13
#24   jnz f 2
#25   sub h -1
#26   set g b
#27   sub g c
#28   jnz g 2
#29   jnz 1 3
#30   sub b -17
#31   jnz 1 -23

# so it's actualy counting the number of non prime numbers between b and c
import math
def p2():
    a, b, c, d, e, f, g, h = 1, 0, 0, 0, 0, 0, 0, 0
    
    b = 81
    c = b
    if a != 0:
        b *= 100
        b += 100000 # b = 108100
        c = b
        c += 17000 # c = 125100

    for b in range(b, c + 1, 17):
        for d in range(2, int(math.sqrt(b + 1))):
            if (b % d) == 0:
                h += 1
                break
    print(h)
p2()
