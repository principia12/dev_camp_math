import os
import sys
import math 
from util import *

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
    'cos' : math.cos, 
    'sin' : math.sin, 
    'tan' : math.tan, 
    'cosh' : math.cosh,
    'sinh' : math.sinh,
    'tanh' : math.tanh,    
    'ln' : math.log,
    'log' : math.log10,
    
    # constants are also considered as functions! 
    'e' : lambda : math.e, 
    'pi' : lambda : math.pi, 
    }
