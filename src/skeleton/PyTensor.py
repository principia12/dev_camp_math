from PyFormula import *
from util import *

class PyVector:
    ''' Vector class. 
    '''
    def __init__(self, *data): # should be list-like data type
        # PyVector(1,2,3)
        # PyVector(PyFormula('x+y'), 1, 2)
        for elem in data:
            assert isinstance(elem, PyFormula) or isnumber(elem)
        self.data = data
        self.shape = (len(data), 1)
    
    # for vec[i] syntax
    def __iter__(self):
        # v = PyVector(1,2,3)
        # v[1] = 2
        yield from self.data
        
    # check if vector is numeric
    def is_numeric(self):
        res = True
        for elem in self.data:
            res = res and isnumber(elem)
        return res
        
        #return all(list(filter(lambda x:isnumber(x), self.data)))
        
    # implement vector as function 
    def __call__(self, *value_list, **value_dict):
        pass
        
    # basic opertions    
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        # return PyVector(*[x+y for zip(self.data, other.data)])
        res = []
        for i in range(self.size()):
            res.append(self.data[i] + other.data[i])
        return PyVector(*res)
        
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        res = []
        for i in range(self.size()):
            res.append(self.data[i] - other.data[i])
        return PyVector(*res)
        
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert self.size() == other.size()
            return PyVector.inner_product(self, other)
        elif isinstance(other, PyFormula) or isnumber(other):
            return PyVector(*[e*other for e in self.data])
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
        return sum([x*y for x,y in zip(l,r)])
        
    def norm(self):
        import math
        if self.is_numeric():
            import math
            return math.sqrt(PyVector.inner_product(self, self))
        else:
            return lambda *args, **kargs:math.sqrt(PyVector.inner_prodcut(self.self)(*args, **kargs)**2)
    @staticmethod    
    def is_orthogonal(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        return PyVector.inner_product(l,r) == 0
    
    @staticmethod    
    def cosine_similarity(l, r):
        assert isinstance(l, PyVector)
        assert isinstance(r, PyVector)
        assert l.size() == r.size()
        return PyVector.inner_product(l,r)/(l.norm()*r.norm())
    
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
    

