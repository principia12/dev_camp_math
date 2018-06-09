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
        for elem in data:
            assert isinstance(elem, PyVector)
            assert elem.shape == data[0].shape
        
        if initialize_from_column:
            tmp = []
            for j in range(data[0].shape[0]):
                tmp.append([])
                for i in range(len(data)):
                    tmp[-1].append(data[i][j])
            self.data = tmp
            self.cols = data
            self.rows = [PyVector(*r) for r in tmp]
        else:
            tmp = []
            for r in data:
                tmp.append([e for e in r])
            self.data = tmp
                
            self.rows = data
            cols = []
            for idx in range(len(tmp[0])):
                cols.append(PyVector(*[e[idx] for e in tmp]))
            self.cols = cols
            
        self.is_column = initialize_from_column
        
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
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        
        cols = [x+y for x,y in zip(self.cols, other.cols)]
        return PyMatrix(cols)
        
        
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        assert self.size() == other.size()
        
        cols = [x-y for x,y in zip(self.cols, other.cols)]
        return PyMatrix(cols)
        
    def __mul__(self, other):
        # matrix-matrix
        if isinstance(other, self.__class__):
            assert self.size()[1] == other.size()[0]
            tmp = []
            for i in range(self.size()[0]):
                tmp.append([])
                for j in range(other.size()[1]):
                    sum = 0
                    for k in range(self.size()[1]):
                        sum += self.data[i][k]*other.data[k][j]
                    tmp[-1].append(sum)
            return PyMatrix(*[PyVector(*r) for r in tmp], 
                                initialize_from_column = False)
        elif isinstance(other, PyVector):
            assert self.size()[1] == other.size()[0]
            tmp = []
            for i in range(self.size()[0]):
                tmp.append([])
                for j in range(other.size()[1]):
                    sum = 0
                    for k in range(self.size()[1]):
                        sum += self.data[i][k]*other.data[k]
                    tmp[-1].append(sum)
            return PyMatrix(*[PyVector(*r) for r in tmp])
    
    def __rmul__(self, other):
        if isnumber(other):
            return PyMatrix(*[other*r for r in self.cols])
    # trace and transpose    
    def trace(self):
        sum = 0
        assert self.size()[0] == self.size()[1]
        for i in range(self.size()[0]):
            sum += self.data[i][i]
        return sum 
        
    def transpose(self):
        return PyMatrix(*self.rows)
    
    @staticmethod
    def _remove_idx(lst, remove_idx):   
        tmp = []
        for idx, elem in enumerate(lst):
            if idx != remove_idx:
                tmp.append(elem)
        return tmp 
    def _minor(self, i, j):
        cols = []
        for idx, c in enumerate(self.cols):
            if idx != i:
                cols.append(\
                    PyVector(*PyMatrix._remove_idx(c.data, j)))
        return PyMatrix(*cols)
            
        
    def determinant(self):
        assert self.size()[0] == self.size()[1]
        if self.size() == (2,2):
            return self.data[0][0]*self.data[1][1] - self.data[1][0]*self.data[0][1]
        else:
            sum = 0
            for idx, elem in enumerate(self.rows[0]):
                sum += (-1)**idx * self._minor(0,idx).determinant()
            return sum 
            
    # some constants
    @staticmethod
    def identity(size):
        cols = [[0]*i + [1] + [0]*(size-i-1) for i in range(size)]
        return PyMatrix(*[PyVector(*c) for c in cols])
    
    @staticmethod
    def zero(size):
        cols = [[0]*size for i in range(size)]
        return PyMatrix(*[PyVector(*c) for c in cols])
        
    # elementary operations     
    def change_row(self, i, j):
        rows = []
        for idx, elem in enumerate(self.rows): 
            if idx == i:
                rows.append(self.rows[j])
            elif idx == j:
                rows.append(self.rows[i])
            else:
                rows.append(self.rows[idx])
        return PyMatrix(*rows, initialize_from_column = False)
        
    def multiply_row(self, i, factor):
        rows = []
        for idx, elem in enumerate(self.rows): 
            if idx == i:
                rows.append(factor*self.rows[i])
            else:
                rows.append(self.rows[idx])
        return PyMatrix(*rows, initialize_from_column = False)
        
    def add_row(self, i, j):
        rows = []
        for idx, elem in enumerate(self.rows): 
            if idx == i:
                rows.append(self.rows[i] + self.rows[j])
            else:
                rows.append(self.rows[idx])
        
        return PyMatrix(*rows, initialize_from_column = False)
    
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
        for idx, elem in enumerate(self.cols[col_idx][highest_row:]):
            if elem == 0:
                pass
            else:
                return idx + highest_row
                
    def gaussian_elimination(self):
        '''Return list of elementary operations and result matrix. 
        - list of matrices corresponding with necessary elementary operaitons
        - result matrix 
       
        '''
        from copy import deepcopy
        
        col_idx = 0 
        
        tmp = deepcopy(self)
        lst = []
        s = len(tmp.rows)
        
        while(col_idx != self.size()[1]):
            idx = tmp._find_leading_row(col_idx, col_idx)
            if idx is None:
                col_idx += 1
                continue
            assert idx >= col_idx, (idx, col_idx)
            if idx != col_idx:
                m = PyMatrix.elementary_matrix(option = 'chanage', 
                                      i = col_idx,
                                      j = idx,
                                      size = s)
                lst.append(m)
                
                tmp = m * tmp
            leading_elem = tmp.data[col_idx][col_idx]
            # make all column elements below col_idx 0 
            for idx, elem in enumerate(tmp.cols[col_idx]):
                if idx > col_idx and elem != 0:
                    m = PyMatrix.elementary_matrix(option = 'multiply', 
                                          i = idx, 
                                          factor = -leading_elem/elem, 
                                          size = s)
                    lst.append(m)
                    tmp = m * tmp
                    m = PyMatrix.elementary_matrix(option = 'add', 
                                          i = idx, 
                                          j = col_idx,
                                          size = s,)
                    lst.append(m)
                    tmp = m * tmp
            col_idx += 1
            
        return lst, tmp 
                
                
            
    def diagonalize(self):
        assert self.size()[0] == self.size()[1]
        assert self.invertible()
        
        lst, tmp = self.gaussian_elimination()
        s = len(tmp.rows)
        
        for col_idx in range(s): 
            for row_idx in range(col_idx):
                i = col_idx
                j = row_idx 
                
                if tmp.data[j][i] != 0:
                    m = PyMatrix.elementary_matrix(option = 'multiply', 
                                    i = j, 
                                    factor = -tmp.data[i][i]/tmp.data[j][i], 
                                    size = s)
                    lst.append(m)
                    tmp = m * tmp 
                    m = PyMatrix.elementary_matrix(option = 'add', 
                                                i = j, 
                                                j = i, 
                                                size = s)
                    lst.append(m)
                    tmp = m * tmp
        return lst, tmp
        
    # check if there is a inverse    
    def invertible(self):
        assert self.size()[0] == self.size()[1]
        res = True
        lst, tmp = self.gaussian_elimination()
        for idx in range(self.size()[1]):
            res = res and tmp.data[idx][idx] != 0
            
        return res
        # lst, tmp = self.gaussian_elimination()
        # return all([tmp.data[i][i] for i in range(self.size()[0])])
        
    # get inverse if it exists. else return None 
    def inverse(self):
        assert self.size()[0] == self.size()[1]
        assert self.invertible()
        
        lst, tmp = self.diagonalize()
        s = len(tmp.cols)
        for idx in range(s):
            m = PyMatrix.elementary_matrix(option = 'multiply', 
                                    i = idx, 
                                    factor = 1/tmp.data[idx][idx], 
                                    size = s)
            lst.append(m)
            tmp = m * tmp 
        print(tmp)
            
        
        res = PyMatrix.identity(s)
        for elem in lst:
            res = elem * res
            
        return res
    
    