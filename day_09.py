#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from types import SimpleNamespace
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

class Node(SimpleNamespace): pass

def parse(line):
    root = Node(children=[], garbage=0)
    stack = deque([root])
    
    in_garbage = False
    cancel_next = False
    for c in line:
        if c == '\n':
            break
        if cancel_next:
            cancel_next = False
            continue
        if not in_garbage:
            if c == '{':
                n = Node(children=[], garbage=0)
                parent=stack[-1].children.append(n)
                stack.append(n)
            elif c == '}':
                stack.pop()
            elif c == '<':
                in_garbage = True
        else:
            if c == '!':
                cancel_next = True
            elif c == '>':
                in_garbage = False
            else:
                stack[-1].garbage += 1
    return root.children[0]

def score_p1(tree, depth=1):
    return depth + sum(score_p1(c, depth+1) for c in tree.children)

def score_p2(tree):
   return tree.garbage + sum(score_p2(c) for c in tree.children)

def test_p1():
    assert score_p1(parse("{{{},{},{{}}}}")) == 16
    assert score_p1(parse("{{<ab>},{<ab>},{<ab>},{<ab>}}")) == 9
    assert score_p1(parse("{{<!!>},{<!!>},{<!!>},{<!!>}}")) == 9
    assert score_p1(parse("{{<a!>},{<a!>},{<a!>},{<ab>}}")) == 3
test_p1()

def p1():
    for line in fileinput.input():
        print(score_p1(parse(line)))
p1()

def p2():
    for line in fileinput.input():
        print(score_p2(parse(line)))
p2()
