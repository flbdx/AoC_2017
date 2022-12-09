#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

def work_p1(s):
    r = 0
    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            r += int(s[i])
    if s[-1] == s[0]:
        r += int(s[0])
    return r

def work_p2(s):
    r = 0
    l = len(s)
    for i in range(l):
        if s[i] == s[(l//2 + i) % l]:
            r += int(s[i])
    return r

def test_p1():
    assert work_p1("1111") == 4
    assert work_p1("1234") == 0
    assert work_p1("1122") == 3
    assert work_p1("91212129") == 9
test_p1()

def p1():
    for line in fileinput.input():
        print(work_p1(line.strip()))
p1()

def test_p2():
    assert work_p2("1212") == 6
    assert work_p2("1221") == 0
    assert work_p2("123425") == 4
    assert work_p2("123123") == 12
    assert work_p2("12131415") == 4
test_p1()

def p2():
    for line in fileinput.input():
        print(work_p2(line.strip()))
p2()
