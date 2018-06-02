from PyFormula import *
from util import *

class PyVector:
    ''' Vector class. 
    '''
    def __init__(self, *data): # should be list-like data type

        # assert shape 
        for elem in data:
            assert isinstance(elem, PyFormula) or isnumber(elem)
        self.data = data
        self.shape = (len(self.data), 1) # for consistency with matrix
    
    # for vec[i] syntax
    def __iter__(self):
        yield from self.data
        
    # check if vector is numeric
    def is_numeric(self):
        '''
        # equivalent to code below
        res = True
        for elem in self.data:
            res = res and isnumber(elem)
        return res
        '''
        return all(map(lambda x:isnumber(x), self.data))
        
    # implement vector as function 
    def __call__(self, *value_list, **value_dict):
        pass
        
    # basic opertions    
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        return PyVector(*[x+y for x,y in zip(self.data, other.data)])
        
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        return PyVector(*[x-y for x,y in zip(self.data, other.data)])
        
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert self.size() == other.size()
            return PyVector.inner_product(self, other)
        elif isinstance(other, PyFormula) or isnumber(other):
            return 
        elif isinstance(other, Matrix):
            pass
        else:
            assert False, 'TypeError : multiplication with type %s not defined.'%str(type(other))
        
    # inner-product related operations
    @staticmethod
    def inner_product(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        return sum([x*y for x,y in zip(l.data, r.data)])
        
    def norm(self):
        import math
        if self.is_numeric():
            return math.sqrt(PyVector.inner_product(self))
        else:
            '''
            def sqrt_result(*args):
                return math.sqrt(PyVector.inner_product(self)(*args))
            return sqrt_result
            '''
            return lambda *args : math.sqrt(PyVector.inner)product(self)(*args)
    @staticmethod    
    def is_orthogonal(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        return PyVector.inner_product(self, other) == 0
    
    @staticmethod    
    def cosine_similarity(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        dot = PyVector.inner_product(self, other)
        return dot/(self.norm()*other.norm())
    
    # cross product
    @staticmethod
    def cross_product(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size() == 3
        r1 = []
        r2 = []
        r3 = []
        return PyVector(r1, r2, r3)
   
    # span 
    @staticmethod
    def span(*vecs):
        pass
        
    # lineraly independent
    @staticmethod
    def lineraly_independent(*vecs):
        pass
        
    @staticmethod
    def linearly_dependent(*vecs):
        pass
        
    @staticmethod
    def resolve_dependency(*vecs):
        ''' return one of the biggest subset of vecs that is linearly independent. 
        '''
        pass
    
        
class PySubspace(PySet):
    def __init__(self, *basis):
        self.basis = basis
        PySet.__init__(self, PyVector.span(*basis).membership)

    
class PyMatrix:
    def __init__(self, data):
        self.data = data
        
    def __add__(self, other):
        pass
        
    def __sub__(self, other):
        pass
        
    def __mul__(self, other):
        pass
        
    def trace(self):
        pass
        
    def transpose(self):
        pass
        
    def determinant(self):
        pass
        
    def row_space(self):
        pass
        
    def column_space(self):
        pass    
    

