#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

def work_p1(lines):
    c = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        words = line.split(" ")
        words_set = set(words)
        c += len(words) == len(words_set)
    return c

def work_p2(lines):
    c = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        words = line.split(" ")
        words_set = set(words)
        if len(words) != len(words_set):
            continue
        
        # trier les caractères des string par ordre alphabétique et placer dans un set
        words_set = set("".join(sorted(s)) for s in words)
        
        if len(words) != len(words_set):
            continue
        
        c += 1
    return c

def p1():
    print(work_p1(fileinput.input()))
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
