#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import math

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

def read_pattern(pattern):
    lines = pattern.strip().split("/")
    width = len(lines)
    art = [None] * (width * width)
    
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            art[y * width + x] = c
    return tuple(art), width

def expand_pattern(pattern):
    output = set()
    art, width = read_pattern(pattern)
    
    for rotation in range(4):
        output.add(tuple(art))
        
        # vertical flip
        new_art = [None] * (width * width)
        for y in range(width):
            for x in range(width):
                new_art[y * width + x] = art[y * width + (width - x - 1)]
        output.add(tuple(new_art))
        
        # horizontal flip
        for y in range(width):
            for x in range(width):
                new_art[y * width + x] = art[(width - y - 1) * width + x]
        output.add(tuple(new_art))
        
        # left rotation
        if rotation != 3:
            for y in range(width):
                for x in range(width):
                    new_art[(width - x - 1) * width + y] = art[y * width + x]
        art = new_art
    return output

def build_rules(lines):
    rules = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        pattern, replacement = line.split(" => ")
        patterns = expand_pattern(pattern)
        replacement, _w = read_pattern(replacement)
        for pattern in patterns:
            if not pattern in rules:
                rules[pattern] = replacement
            else:
                print("got one rule collision")
    return rules

def apply_rules(art, rules):
    width = int(math.sqrt(len(art)))
    div_width = 2 if (width % 2) == 0 else 3
    r_width = (width // div_width) * (div_width + 1)
    new_art = [None] * (r_width * r_width)
    for Y in range(0, width, div_width):
        for X in range(0, width, div_width):
            subart = tuple()
            for y in range(div_width):
                subart += art[(Y + y) * width + X: (Y + y) * width + X + div_width]
            
            replacement = rules[subart]
            r_Y = (Y // div_width) * (div_width + 1)
            r_X = (X // div_width) * (div_width + 1)
            
            for y in range(div_width + 1):
                new_art[(r_Y + y) * r_width + r_X : (r_Y + y) * r_width + r_X + (div_width + 1)] = replacement[y * (div_width + 1) : y * (div_width + 1) + (div_width + 1)]
    
    return tuple(new_art)
    
def p1():
    rules = build_rules(fileinput.input())
    art, w = read_pattern(".#./..#/###")
    for step in range(5):
        art = apply_rules(art, rules)
    print(sum((c == '#') for c in art))
p1()

def p2():
    rules = build_rules(fileinput.input())
    art, w = read_pattern(".#./..#/###")
    for step in range(18):
        art = apply_rules(art, rules)
    print(sum((c == '#') for c in art))
p2()
