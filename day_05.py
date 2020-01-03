#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

def work_p1(lines):
    jumps = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        jumps.append(int(line))
    
    steps = 0
    ip = 0
    while True:
        v = jumps[ip]
        jumps[ip] += 1
        ip += v
        steps += 1
        if ip < 0 or ip >= len(jumps):
            break
    return steps

def work_p2(lines):
    jumps = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        jumps.append(int(line))
    
    steps = 0
    ip = 0
    while True:
        v = jumps[ip]
        jumps[ip] += -1 if v >= 3 else 1
        ip += v
        steps += 1
        if ip < 0 or ip >= len(jumps):
            break
    return steps

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
