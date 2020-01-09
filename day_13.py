#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

def build_firewall(lines):
    firewall = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            break
        depth, _range = map(int, line.split(": "))
        
        while len(firewall) < depth:
            firewall.append((0, 0))
        firewall.append((_range, 2 * (_range - 1)))
    
    return firewall

def caught(firewall, layer, step):
    _range, rtt = firewall[layer]
    if _range == 0:
        return False
    
    return (step % rtt) == 0

def traverse(firewall):
    return sum(caught(firewall, l, l) * l * firewall[l][0] for l in range(len(firewall)))

def traverse_p2(firewall, delay):
    for l in range(len(firewall)):
        if caught(firewall, l, l + delay):
            return False
    return True

def p1():
    fw = build_firewall(fileinput.input())
    print(traverse(fw))
p1()

def p2():
    fw = build_firewall(fileinput.input())
    delay = 0
    while not traverse_p2(fw, delay):
        delay += 1
    print(delay)
p2()
