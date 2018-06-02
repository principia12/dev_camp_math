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
    
def expr(operator, operand, tokens, idx):
    return idx
    
def find_match(tokens, t_idx):
    return t_idx 

    
def part(operator, operand, tokens, idx):
    return idx
    
def pop_operator(operator, operand):
    pass

def push_operator(operator, operand, op):
    pass
    
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
    
    
    