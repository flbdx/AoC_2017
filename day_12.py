#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def parse(lines):
    data = {}
    
    for line in lines:
        v, rem = line.strip().split(" <-> ")
        data[int(v)] = set(int(i) for i in rem.split(", "))
    
    groups = []
    while len(data) != 0:
        group = set()
        v, queue = data.popitem()
        group.add(v)
        while len(queue) != 0:
            v2 = queue.pop()
            if v2 in data.keys():
                queue.update(data[v2])
                group.add(v2)
                del data[v2]
        groups.append(group)
    
    return groups

def test_p1():
    lines="""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""".splitlines()
    groups = parse(lines)
    assert len(next(g for g in groups if 0 in g)) == 6
test_p1()

def p1():
    groups = parse(fileinput.input())
    print(len(next(g for g in groups if 0 in g)))
p1()

def p2():
    groups = parse(fileinput.input())
    print(len(groups))
p2()

