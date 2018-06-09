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
        
    def size(self):
        return (len(self.data), 1)
    
    def __index__(self, idx):
        return self.data[idx]
    # for vec[i] syntax    
    def __getitem__(self, idx, j=None):
        if j is None:
            return self.data[idx]
        else:
            assert j==1
            return self.data[idx]
    
    def __str__(self):
        res = ''
        for elem in self.data:
            res += ' %s '%str(elem)
        return res
    
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
            return PyVector(*[d*other for d in self.data])
        elif isinstance(other, Matrix):
            pass
        else:
            assert False, 'TypeError : multiplication with type %s not defined.'%str(type(other))
    
    def __rmul__(self, other):
        if isnumber(other):
            return PyVector(*[d*other for d in self.data])
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
            return lambda *args : math.sqrt(PyVector.inner_product(self)(*args))
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
    def __init__(self, *data, initialize_from_column = True):
        self.data = None
        self.cols = None
        self.rows = None
        self.is_column = None
        
        
    def __str__(self):
        res = ''
        for row in self.data:
            for elem in row:
                res += '%s\t'%str(round(elem, 3))
            res += '\n'
        return res
    
    def size(self):
        return (len(self.data), len(self.data[0]))
        
    def __getitem__(self, i, j=None):
        if j is None:
            return self.data[i]
        else:
            return self.data[i][j]
        
    # matrix arithematic operations     
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        # matrix-matrix
        if isinstance(other, self.__class__):
            pass
        elif isinstance(other, PyVector):
            pass
        elif isnumber(other):
            pass
            
    def __rmul__(self, other):
        if isnumber(other):
            pass
        
    # trace and transpose    
    def trace(self):
        pass
        
    def transpose(self):
        pass
    
    def _minor(self, i, j):
        pass
        
    def determinant(self):
        pass
            
    # some constants
    @staticmethod
    def identity(size):
        pass
        
    @staticmethod
    def zero(size):
        pass
        
    # elementary operations     
    def change_row(self, i, j):
        pass
    def multiply_row(self, i, factor):
        pass
    def add_row(self, i, j):
        pass
    
    @staticmethod
    def elementary_matrix(**kargs):
        assert 'option' in kargs.keys()
        assert 'size' in kargs.keys()
        
        if kargs['option'] == 'add':
            assert 'i' in kargs.keys()
            assert 'j' in kargs.keys()
            return PyMatrix.identity(kargs['size']).add_row(kargs['i'], kargs['j'])
        elif kargs['option'] == 'change':
            assert 'i' in kargs.keys()
            assert 'j' in kargs.keys()
            return PyMatrix.identity(kargs['size']).change_row(kargs['i'], kargs['j'])
        elif kargs['option'] == 'multiply':
            assert 'i' in kargs.keys()
            assert 'factor' in kargs.keys()
            
            return PyMatrix.identity(kargs['size']).multiply_row(kargs['i'], kargs['factor'])
        else:
            assert False, 'Not a valid option : %s'%kargs['option']
    
   
    def _find_leading_row(self, col_idx, highest_row):
        ''' Given a matrix and highest row, find the row with the leftmost element. 
        example) 
        
        0 1 2 1 0 
        2 1 2 0 0 
        3 3 1 1 1 
        highest_row : 0 / col_idx = 0
        >> 1
        
        0 0 0 0 2 
        0 1 0 1 1 
        0 0 1 0 0
        0 0 0 0 1
        highest_row : 2 / col_idx = 0
        >> 2
        '''
        pass        
    
    def gaussian_elimination(self):
        '''Return list of elementary operations and result matrix. 
        - list of matrices corresponding with necessary elementary operaitons
        - result matrix 
       
        '''
        pass            
                
            
    def diagonalize(self):
        pass
        
    # check if there is a inverse    
    def invertible(self):
        pass
        
    # get inverse if it exists. else return None 
    def inverse(self):
        pass
    

