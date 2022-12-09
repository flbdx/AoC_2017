#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import Counter
from types import SimpleNamespace
import re

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

class Program(SimpleNamespace): pass

def build_tree(lines):
    programs = {}
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        result = re.match("(\w+) \((\d+)\)", line)
        name = result.group(1)
        weight = int(result.group(2))
        children = []
        children_idx = line.find(" -> ")
        if children_idx > 0:
            children = line[children_idx + 4:].split(", ")
        
        children = [programs.get(c, Program(name=c,parent=None)) for c in children]
        
        p = programs.get(name, Program(name=name,parent=None))
        p.weight = weight
        p.children = children
        
        for c in children:
            c.parent = p
            if not c.name in programs:
                programs[c.name] = c
        
        programs[name] = p
    
    root = p
    while root.parent != None:
        root = root.parent
    
    return root

def rec_weight(root):
    p = root
    w = p.weight
    for c in p.children:
        w += rec_weight(c)
    p.total_weight = w
    return w

def work_p1(lines):
    root = build_tree(lines)

    return root

def work_p2(lines):
    root = build_tree(lines)
    rec_weight(root)
    
    def check_weights(n):
        test_set = set(c.total_weight for c in n.children)
        if len(test_set) <= 1:
            return None
        else:
            return n
    
    def DFS(n):
        r = None
        for c in n.children:
            r = DFS(c)
            if r:
                break
        if not r:
            r = check_weights(n)
        return r

    culprit_parent = DFS(root)
    
    candidate_weights = [c.total_weight for c in culprit_parent.children]
    candidate_weights_counted = Counter(candidate_weights).most_common()
    delta_weight = candidate_weights_counted[1][0] - candidate_weights_counted[0][0]
    return next(c.weight - delta_weight for c in culprit_parent.children if c.total_weight != candidate_weights_counted[0][0])
    

def test_p1():
    lines="""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".splitlines()
    assert work_p1(lines).name == "tknk"
test_p1()

def test_p2():
    lines="""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".splitlines()
    assert work_p2(lines) == 60
test_p2()

def p1():
    print(work_p1(fileinput.input()).name)
p1()

def p2():
    print(work_p2(fileinput.input()))
p2()
