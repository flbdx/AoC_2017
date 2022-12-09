#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from types import SimpleNamespace

class Rule(SimpleNamespace): pass

if len(sys.argv) == 1:
    sys.argv += ["input_25"]


class TuringMachine(object):
    def __init__(self, lines):
        re_init_state = re.compile("\s*Begin in state ([a-zA-Z]+)")
        re_steps = re.compile("\s*Perform a diagnostic checksum after ([0-9]+) steps")
        re_in_state = re.compile("\s*In state ([a-zA-Z]+):")
        re_if_value = re.compile("\s*If the current value is ([01]):")
        re_write_value = re.compile("\s*- Write the value ([01])")
        re_move = re.compile("\s*- Move one slot to the ([a-zA-Z]+)")
        re_continue_state = re.compile("\s*- Continue with state ([a-zA-Z]+)")
    
        self.rules = {}
        current_state = None
        current_rule = None
        for line in lines:
            result = re_init_state.match(line)
            if result:
                self.state = result.group(1)
                continue
            
            result = re_steps.match(line)
            if result:
                self.check_steps = int(result.group(1))
                continue
            
            result = re_in_state.match(line)
            if result:
                current_state = result.group(1)
                self.rules[current_state] = {}
                continue
            
            result = re_if_value.match(line)
            if result:
                current_rule = Rule(if_value = int(result.group(1)))
                self.rules[current_state][current_rule.if_value] = current_rule
                continue
            
            result = re_write_value.match(line)
            if result:
                current_rule.write = int(result.group(1))
            
            result = re_move.match(line)
            if result:
                current_rule.move = result.group(1)
            
            result = re_continue_state.match(line)
            if result:
                current_rule.next_state = result.group(1)
        
        self.rules[current_state][current_rule.if_value] = current_rule
        
        self.tape = set()
        self.position = 0
        
    
    def run_p1(self):
        steps = 0
        while steps < self.check_steps:
            v = 1 if self.position in self.tape else 0
            rule = self.rules[self.state][v]
            if rule.write == 1:
                self.tape.add(self.position)
            else:
                self.tape.discard(self.position)
            self.position += 1 if rule.move == "right" else -1
            self.state = rule.next_state
            
            steps += 1

def p1():
    tm = TuringMachine(fileinput.input())
    tm.run_p1()
    print(len(tm.tape))
p1()
