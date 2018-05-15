from PySet import PySet, PyCountableSet
from util import *
from math import floor

def integer_generator():
    i = 0
    while True:
        yield i
        i += 1
        yield -1*i
    
PyInt = PyCountableSet(integer_generator)

def rational_generator():
    # implementation of Calkin-Wilf Sequence
    i = 1
    yield 0
    while True:
        yield i
        i = 1/(2*floor(i)-i+1)

PyRational = PyCountableSet(rational_generator)

if __name__ == '__main__':
    PyInt.list_elements()
    PyRational.list_elements()