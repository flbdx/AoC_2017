#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

def checksum_p1(lines):
    r = 0
    for line in lines:
        numbers = [int(word) for word in line.split("\t")]
        r += max(numbers)
        r -= min(numbers)
    return r

def checksum_p2(lines):
    r = 0
    for line in lines:
        numbers = [int(word) for word in line.split("\t")]
        for n1, n2 in itertools.combinations(numbers, 2):
            if n1 > n2 and (n1 % n2) == 0:
                r += n1 // n2
            elif n1 < n2 and (n2 % n1) == 0:
                r += n2 // n1
    return r

def p1():
    print(checksum_p1(fileinput.input()))
p1()

def p2():
    print(checksum_p2(fileinput.input()))
p2()
