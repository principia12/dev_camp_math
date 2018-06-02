from PySet import PySet, PyFiniteSet
from util import *
from global_variables import *
from copy import deepcopy

import math
import re

#-------------------------------------              
# Formula Class
#-------------------------------------

class PyFormula: 
    def __init__(self, eq, ):
        pass
        
    def __add__(self, other): 
        pass
    
    def __sub__(self, other):
        pass
    
    def __mul__(self, other):
        pass

    def __div__(self, other):
        pass
        
    def __str__(self):
        pass
        
    def __call__(self, *value_list, **value_dict):
        pass
    @staticmethod    
    def _calculate(tree, value_dict):
        pass
    
'''
6/02 Coding Practice 
Parser Implementation

In this problem, you are given a grammar that expresses common mathematical expressions, but without (-) signed numbers. 

1. Grammar

IMPORTANT : IF YOU CAN UNDERSTAND THE GRAMMAR, DO NOT READ THIS PART.

Grammar is given as following; 

1) expr -> part (binary part)* ; 
2) part -> num | val | "(" expr ")" ; 
3) binary -> "+" | "-" | "*" | "/" | "^" ; 
4) num -> r"[1-9][0-9]*\.?[0-9]*|0" ; 
5) val -> r"[a-zA-Z]+"

Each line of grammar is called a rule. A rule can be seperated by '->', distinguishing left hand side and right hand side. Each rule means that the left hand side can be rewritten by one of the options - options are splited by | - on the left hand side. For example, binary can be replaced by "+". Input is always assumed to be the left hand side of the first rule, and parsed to the sequence of 'terminals', which are tokens that are wrapped by ". 

Your task is to write a parser that gets input string and return a tree-like structure expressing the meaning of this grammar. 

The grammar shown on the slide is NOT identical to the grammar you see in this text. However, it should not make a bit difference - unless you have passed all the tests till eq33. Even if so, it will not cause a significant error. 

On rule 1), '(binary part)*' means that 'binary part' will be finitely iterated. 0 iteration is also possible. So, 1) is just a shortened notation for  

1') expr -> part | part binary part | part binary part binary part | ... 

On rule 4 and 5, you might find the right hand side of the rule unfamiliar if you have not encounted a regular expression before. They imply as follows; 

4.r) r"[1-9][0-9]*\.?[0-9]*|0"

Firstly, [1-9] or [0-9] means from 1-9 or 0-9, respectively. * after the [] term means that token that is expressed in [] can be repeated zero or more times. Likewise, ? means it can be repeated zero or one times. \. represents dot itself. So, this regular expression means a string that starts with one of the numbers 1 to 9, and have few numbers afterward, allowing one dot in the middle; which is just a normal numbers, except 0. Since 0 is the only number that starts with 0, 0 is handled with care. 

5.r) r"[a-zA-Z]+"

Only new part is +. It means one or more iteration, not allowing zero iteration. 
 

2. Functions to implement and hints 

 
- tokenizer

When implementing tokenizer, go through a given equation by iteratively checking whether the first part of equation matches with one of the tokens. If so, erase matching part and repeat again. For this, use re.match() function. 

re.match(pattern, string) checks whether the pattern is matched with the 'first part' of the string. (This is difference between re.find(); it searches through all the string.) Since it will return a match object, you can use m.start() and m.end() to locate the longest matching part. So the pseudocode will be as following; 

while eq !=  '':
    for pattern in tokens:
        if re.match(pattern, eq):
            yield (pattern_type, pattern)
            eq = erase_eq(...) 

Note that not all tokens are regular expression; some are just strings. Handle them accordingly. 

- parser

Two methods can be considered for implementing the parser for the given grammar. 

- Recursive implementation 

In the recursive implementation, 'expr' and 'part' will be a function that parses to that specific matching part and return the index of the matching part. For example, consider following expression; 

1+1 -> tokenized to ('num', 1), ('op', +), ('num', 1)

When you first call expr, it should call part twice; first part should return 1 or 2, since it will only parse the first token. You can either increment token, or make part function returns to the next index that parsing need to be started. 

- Iterative implementation 

Consider the type of current token and next token. Handle it accoridngly; use stack for handling the operators. 

'''

precedence = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, }
    
def tokenizer(equation):
    tokens = {\
        'op' : ['^', '+', '-', '*', '+', '/'],
        'para' : ['(', ')'],
        'num' : [r"[1-9][0-9]*\.?[0-9]*|0",], # 0 is also a number! 
        'var' : [r"[a-zA-Z]+_?[0-9]*",], } # x_0 format also allowed
    tok_strings = tokens['op'] + \
        tokens['para'] + tokens['num'] + tokens['var']
    
    
def recursive_descent(tokens):
    operator = Stack()
    operand = Stack()
    idx = expr(operator, operand, tokens, 0)
    res = operand.pop()
    
    return res
    
    
def parse(eq):
    return recursive_descent(list(tokenizer(eq)))
        
if __name__ == '__main__':
    
    # tests, tests, more tests! 
    
    # simple numbers
    eq1 = '(1)'
    eq2 = '3'
    
    # +,- 
    eq4 = '1+1'
    
    # +,-,*,/ 
    eq7 = '1+2/3+2'
    eq8 = '3*4+2'
    eq9 = '4/2'
    eq10 = '3+4*2'
    eq11 = '3+4/2'
    eq12 = '3/4/2'
    eq13 = '(3/4)/2' # check
    eq14 = '3/(4/2)'
    eq15 = '1+2/3'
    
    # +,-,*,/,^ with (,)
    eq16 = '(1+2)/3'
    eq17 = '(1*2)/3'
    eq18 = '(1+2)*3'
    eq19 = '3*(1+2)'
    eq20 = '3*(2-1)'
    eq21 = '3*(1-2)'
    
    # +,-,*,/ with nested (,)
    eq29 = '3+(2^(2+2))'
    eq30 = '3*(2*2+1)'
    eq31 = '2-3*(2*2+1)'
    eq32 = '2-3*(2*(2+1))'
    eq33 = '((3+2)*4-(2*4+2^(2-5)))*(2+(3+2)*5^2)'
    
    eq36 = 'x'
    eq37 = 'x*z+y'
    eq40 = '1+3^3*c'
    eq45 = 'a+b+C+d+e+f+g+h'
    eq46 = '1'
    eq47 = '0'

    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        print(parse(eq))
        print('=============')
    eq = PyFormula(eq37)
    print(eq(1,2,3))
    print(eq(x_0 = 1, y = 2, z = 3)) 
    
    
    