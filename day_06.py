#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]


def balance(banks):
    l = len(banks)
    index_max = max(range(l), key=banks.__getitem__)
    v = banks[index_max]
    
    banks[index_max] = 0
    q, r = divmod(v, l)
    for i in range(l):
        banks[(index_max + 1 + i) % l] += q + (1 if i < r else 0)
    
    return banks

def work_p1(line):
    banks = [int(w) for w in line.strip().split("\t")]
    configs = set(tuple(banks))
    steps = 0
    while True:
        balance(banks)
        t = tuple(banks)
        steps += 1
        if t in configs:
            return steps
        configs.add(tuple(banks))
    
def work_p2(line):
    banks = [int(w) for w in line.strip().split("\t")]
    configs = {tuple(banks) : 0}
    steps = 0
    while True:
        balance(banks)
        t = tuple(banks)
        steps += 1
        if t in configs.keys():
            return steps - configs[t]
        configs[t] = steps

def p1():
    for line in fileinput.input():
        print(work_p1(line))
p1()

def p2():
    for line in fileinput.input():
        print(work_p2(line))
p2()
