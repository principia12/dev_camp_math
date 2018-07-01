import os
import sys
import math 
from util import binary2nary


MAXIMUM_ITERATION = 10000
DEBUG = False

OPERATIONS = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, 
    } 
              
OPERATION_WITH_FUNCTIONS = {\
    '+' : binary2nary(lambda x,y : x+y),
    '*' : binary2nary(lambda x,y : x*y), 
    '/' : binary2nary(lambda x,y : x/y), 
    '-' : binary2nary(lambda x,y : x-y),
    '^' : binary2nary(lambda x,y : x**y),
    }

PARA = ['(', ')', '[', ']', '{', '}',]

    
FUNCTION_DICT = {\
    'cos' : (math.cos, math.sin, 
                      '-1*sin(placeholder)'),
    'sin' : (math.sin, lambda x:math.cos(x), 
                       'cos(placeholder)',),
    'tan' : (math.tan, lambda x:1/(math.cos(x)**2), 
                       '1/cos(placeholder)^2'),
    'ln' : (math.log, lambda x:1/x, 
                      '1/placeholder'),
    # constants are also considered as functions! 
    'e' : (lambda : math.e, lambda : 0, '0'),
    'pi' : (lambda : math.pi, lambda : 0, '0'),
    
    # custom functions 
    }