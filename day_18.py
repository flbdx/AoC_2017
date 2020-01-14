#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import defaultdict
import queue
import threading

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

class Break(Exception):
    pass

class Solo(object):
    def __init__(self, lines):
        self.instructions = []
        self.regs = defaultdict(lambda: 0)
        self.ip = 0
        
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            
            words = line.split(" ")
            
            if words[0] == "snd":
                self.instructions.append((self.do_snd, words[1:]))
            elif words[0] == "set":
                self.instructions.append((self.do_set, words[1:]))
            elif words[0] == "add":
                self.instructions.append((self.do_add, words[1:]))
            elif words[0] == "mul":
                self.instructions.append((self.do_mul, words[1:]))
            elif words[0] == "mod":
                self.instructions.append((self.do_mod, words[1:]))
            elif words[0] == "rcv":
                self.instructions.append((self.do_rcv, words[1:]))
            elif words[0] == "jgz":
                self.instructions.append((self.do_jgz, words[1:]))
    
    def op_value(self, op):
        v = None
        try:
            v = int(op)
        except:
            v = self.regs[op]
        return v
    
    #snd X plays a sound with a frequency equal to the value of X.
    def do_snd(self, op1):
        self.regs["SOUND"] = self.op_value(op1)
        self.ip += 1
    
    #set X Y sets register X to the value of Y.
    def do_set(self, op1, op2):
        self.regs[op1] = self.op_value(op2)
        self.ip += 1
    
    #add X Y increases register X by the value of Y.
    def do_add(self, op1, op2):
        self.regs[op1] += self.op_value(op2)
        self.ip += 1
        
    #mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    def do_mul(self, op1, op2):
        self.regs[op1] *= self.op_value(op2)
        self.ip += 1
    
    #mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    def do_mod(self, op1, op2):
        self.regs[op1] %= self.op_value(op2)
        self.ip += 1
    
    #rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    def do_rcv(self, op1):
        if self.op_value(op1) != 0:
            self.regs[op1] = self.regs["SOUND"]
            print(self.regs["SOUND"])
            raise Break()
        self.ip += 1
    
    #jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
    def do_jgz(self, op1, op2):
        if self.op_value(op1) > 0:
            self.ip += self.op_value(op2)
        else:
            self.ip += 1
    
    def run(self):
        while True:
            instruction = self.instructions[self.ip]
            try:
                instruction[0](*instruction[1])
            except Break:
                break
            if self.ip < 0 or self.ip >= len(self.instructions):
                break

def p1():
    d = Solo(fileinput.input())
    d.run()
p1()

class Duet(Solo):
    def __init__(self, lines, program_id, s_queue, r_queue):
        super(Duet, self).__init__(lines)
        self.s_queue = s_queue
        self.r_queue = r_queue
        self.regs["p"] = program_id
        self.n_sends = 0
    
    def do_snd(self, op1):
        self.s_queue.put(self.op_value(op1))
        self.n_sends += 1
        self.ip += 1
    
    def do_rcv(self, op1):
        try:
            self.regs[op1] = self.r_queue.get(timeout=0.5)
        except queue.Empty:
            raise Break()
        self.ip += 1

def work_p2(lines):
    queue_0_1 = queue.Queue()
    queue_1_0 = queue.Queue()
    
    d0 = Duet(lines, 0, queue_0_1, queue_1_0)
    d1 = Duet(lines, 1, queue_1_0, queue_0_1)
    
    thread_0 = threading.Thread(target=Duet.run, args=(d0,))
    thread_1 = threading.Thread(target=Duet.run, args=(d1,))
    
    thread_0.start()
    thread_1.start()
    thread_0.join()
    thread_1.join()

    return d1.n_sends

def p2():
    lines = list(fileinput.input())
    print(work_p2(lines))
p2()
