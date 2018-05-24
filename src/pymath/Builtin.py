from PySet import *
from util import *


def integer_generator():
    i = 0
    while True:
        yield i
        i += 1
        yield -1*i
    
PyInt = PyOrderedSet(\
            integer_generator,
            lambda x,y:x-y)    
       
def rational_generator():
    # implementation of Calkin-Wilf Sequence
    from math import floor    
    i = 1
    yield 0
    while True:
        yield i
        i = 1/(2*floor(i)-i+1)

PyRational = PyOrderedSet(\
    rational_generator, 
    lambda x,y:x-y)

if __name__ == '__main__':
    print('--------------')
    PyInt.list_elements()
    print('--------------')
    PyInt.list_elements(return_sorted = False)
    print('--------------')
    PyRational.list_elements()
    
    