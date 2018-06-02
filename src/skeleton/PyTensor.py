from PyFormula import *
from util import *

class PyVector:
    ''' Vector class. 
    '''
    def __init__(self, *data): # should be list-like data type
        self.data = []
        self.shape = []
    
    # for vec[i] syntax
    def __iter__(self):
        pass
        
    # check if vector is numeric
    def is_numeric(self):
        pass
        
    # implement vector as function 
    def __call__(self, *value_list, **value_dict):
        pass
        
    # basic opertions    
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        pass
        
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        pass
        
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert self.size() == other.size()
            pass
        elif isinstance(other, PyFormula) or isnumber(other):
            pass
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
        pass
        
    def norm(self):
        import math
        if self.is_numeric():
            pass
        else:
            pass
    @staticmethod    
    def is_orthogonal(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        pass
    
    @staticmethod    
    def cosine_similarity(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        pass
    
    # cross product
    @staticmethod
    def cross_product(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size() == 3
        pass
   
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
    def __init__(self, *data, initialize_from_column = True):
        self.size = 0
        self.data = []
        
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
        
    def _minor(self, i, j):
        pass
        
    def determinant(self):
        pass
        
    def row_space(self):
        pass
        
    def column_space(self):
        pass
    

