#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import namedtuple, Counter
import re

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

Program = namedtuple("Program", ["name", "weight", "parent", "children", "total_weight"])

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
        
        t = programs.get(name, None)
        if t != None:
            programs[name] = t._replace(weight=weight, children=children)
        else:
            programs[name] = Program(name, weight, None, children, 0)
        
        for c in children:
            t = programs.get(c, None)
            if t != None:
                programs[c] = t._replace(parent=name)
            else:
                programs[c] = Program(c, 0, name, [], 0)
    
    return programs

def rec_weight(programs, root_name):
    t = programs[root_name]
    w = t.weight
    for c in t.children:
        w += rec_weight(programs, c)
    programs[root_name] = t._replace(total_weight = w)
    return w

def work_p1(lines):
    programs = build_tree(lines)
    
    root = next(p for p in programs.values() if p.parent == None)
    return root

def work_p2(lines):
    programs = build_tree(lines)
    
    root = next(p for p in programs.values() if p.parent == None)
    rec_weight(programs, root.name)
    
    def check_weights(n):
        test_set = set()
        for c_name in n.children:
            test_set.add(programs[c_name].total_weight)
        if len(test_set) <= 1:
            return None
        else:
            return n
    
    def DFS(n):
        r = None
        for c_name in n.children:
            r = DFS(programs[c_name])
            if r:
                break
        if not r:
            r = check_weights(n)
        return r
    
    culprit_parent = DFS(root)
    
    candidate_weights = list(programs[c].total_weight for c in culprit_parent.children)
    candidate_weights_counted = Counter(candidate_weights).most_common()
    delta_weight = candidate_weights_counted[1][0] - candidate_weights_counted[0][0]
    return next(programs[c].weight - delta_weight for c in culprit_parent.children if programs[c].total_weight != candidate_weights_counted[0][0])
    

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
