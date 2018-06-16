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
        
    def is_zero(self):
        pass
    
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
        
    # return zero vector
    @staticmethod
    def zero(size):
        return PyVector(*[0 for i in range(size)])
    
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
            
    def __div__(self, other):
        if isnumber(other):
            return PyVector(*[d/other for d in self.data])
        
    def __rdiv__(self, other):
        if isnumber(other):
            return PyVector(*[d/other for d in self.data])
            
            
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
            return math.sqrt(PyVector.inner_product(self, self))
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
   
    def unit(self):
        '''
        return unit vector that have same direction with self 
        '''
        pass
        
    def proj(self, vec):
        '''
        Projection from self to vec. Thus, resulting vector have directon to vec
        '''
        pass
        
    
    # span 
    @staticmethod
    def span(*vecs):
        pass
        
    # lineraly independent
    @staticmethod
    def linearly_independent(*vecs):
        pass
        
    @staticmethod
    def linearly_dependent(*vecs):
        return not PyVector.linearly_independent(*vecs)
        
    @staticmethod
    def resolve_dependency(*vecs):
        ''' return one of the biggest subset of vecs that is linearly independent. 
        '''
        pass
    
    @staticmethod
    def gram_schmidt(*vecs):
        pass
        
class PySubspace(PySet):
    def __init__(self, *basis):
        self.basis = basis
        PySet.__init__(self, PyVector.span(*basis).membership)

    
class PyMatrix:
    def __init__(self, *data, initialize_from_column = True):
        assert data!=(), data
        for elem in data:
            assert isinstance(elem, PyVector)
            assert data[0].size() == elem.size()
            
        '''
        1 2 3 4 
        2 3 1 7
        2 1 4 1
        -> data : [[1,2,3,4], [2,3,1,7,], [2,1,4,1]]
        -> rows : [1,2,3,4], [2,3,1,7], [2,1,4,1],
        -> cols : [1,2,2,], [2,3,1,], [3,1,4,], [4,7,1],
        '''
        if initialize_from_column:
            self.cols = data
            tmp = [] 
            for i in range(data[0].size()[0]):
                tmp.append([])
                for j in range(len(data)):
                    # i : 0~2, j : 0~2
                    tmp[-1].append(data[j][i]) # [[1,2,3], 
            self.data = tmp
            self.rows = [PyVector(*r) for r in tmp]
        else:
            self.rows = data
            tmp = []
            for r in data:
                tmp.append(r.data)
            self.data = tmp 
            col = []
            '''
            [1,2,3], [4,5,6], [7,8,9]
            '''
            for i in range(data[0].size()[0]):
                col.append(PyVector(*[r[i] for r in data]))
                # col = [[1,4,7], [2,5,8],...]
            self.cols = col 
        
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
        assert isinstance(other, PyMatrix)
        assert self.size() == other.size()
        
        return PyMatrix(*[x+y for x,y in zip(self.cols, other.cols)])
        
    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        assert isinstance(other, PyMatrix)
        assert self.size() == other.size()
        
        return PyMatrix(*[x-y for x,y in zip(self.cols, other.cols)])
    
    
    def __mul__(self, other):
        # matrix-matrix
        if isinstance(other, self.__class__):
            assert self.size()[1] == other.size()[0]
            rows = []
            # a_ik b_kj 
            
            for i in range(self.size()[0]): # i 
                rows.append([])
                for j in range(other.size()[1]): # j 
                    sum = 0
                    for k in range(self.size()[1]):
                        sum += self.data[i][k] * other.data[k][j]
                    rows[-1].append(sum)
            
            return PyMatrix(*[PyVector(*r) for r in rows], initialize_from_column = False)
        elif isinstance(other, PyVector):
            return self*PyMatrix(*[other])
        elif isnumber(other):
            return PyMatrix(*[other*c for c in self.cols])
            
            
    def __rmul__(self, other):
        if isnumber(other):
            return PyMatrix(*[other*c for c in self.cols])
        
    # trace and transpose    
    def trace(self):
        sum = 0
        for i in range(min(self.size())):
            sum += self.data[i][i]
        return sum 
        
    def transpose(self):
        return PyMatrix(*self.rows)
    
    def _minor(self, i, j):
        # ith row, jth col
        rows = []
        for idx, elem in enumerate(self.rows):
            if idx != i:
                tmp = []
                for jdx, c in enumerate(elem.data):
                    if jdx != j:
                        tmp.append(c)
                rows.append(PyVector(*tmp))
        return PyMatrix(*rows, initialize_from_column = False)
        
    def determinant(self):
        assert self.size()[0] == self.size()[1], self.size()
        if self.size()[0] == 1 and self.size()[1] == 1:
            return self.data[0][0]
        else:
            sum = 0
            for idx, elem in enumerate(self.rows[0]):
                sum += (-1)**(idx) * self._minor(0, idx).determinant()
            return sum 
            
    # some constants
    @staticmethod
    def identity(size):
        rows = []
        for i in range(size):
            rows.append([])
            for j in range(size):
                if i==j:
                    rows[-1].append(1)
                else:
                    rows[-1].append(0)
        
        return PyMatrix(*[PyVector(*r) for r in rows], initialize_from_column = False)
    
    @staticmethod
    def zero(size):
        pass
        
    # elementary operations     
    def change_row(self, i, j):
        row = []
        for idx, elem in enumerate(self.rows):
            if idx == i:
                row.append(self.rows[j])
            elif idx == j:
                row.append(self.rows[i])
            else:
                row.append(elem)
                
        return PyMatrix(*row, initialize_from_column = False)
    
    def multiply_row(self, i, factor):
        assert isnumber(factor)
        row = []
        for idx, elem in enumerate(self.rows):
            if idx == i:
                row.append(factor * self.rows[i])
            else:
                row.append(elem)
                
        return PyMatrix(*row, initialize_from_column = False)
    
    def add_row(self, i, j):
        # ith row -> ith row + jth row
        row = []
        for idx, elem in enumerate(self.rows):
            if idx == i:
                row.append(self.rows[i] + self.rows[j])
            else:
                row.append(elem)
                
        return PyMatrix(*row, initialize_from_column = False)
    
    @staticmethod
    def elementary_matrix(**kargs):
        assert 'option' in kargs.keys()
        assert 'size' in kargs.keys()
        '''
        kargs = {'option' : ..., 
                 'size' : ..., 
                 'i' : ...,
                 'j' : .., 
                 'factor' : ...,
        '''
        
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
        highest_row : 2 / col_idx = 2
        >> 2
        '''
        
        for idx, elem in enumerate(self.cols[col_idx].data[highest_row:]):
            if elem != 0:
                return idx + highest_row
                
    
    def gaussian_elimination(self):
        '''Return list of elementary operations and result matrix. 
        - list of matrices corresponding with necessary elementary operaitons
        - result matrix 
       
        '''
        from copy import deepcopy

        tmp = deepcopy(self)
        col_idx = 0 
        lst = []
        s = self.size()[0]
        
        while col_idx != self.size()[1]:
            
            row_idx = tmp._find_leading_row(col_idx, col_idx)
            if row_idx is None:
                col_idx += 1
                continue
            elif row_idx != col_idx:
                # change col_idx th row and row_idx th row 
                '''
                0 1 1 
                2 1 0
                2 2 2 
                row_idx = 1 
                col_idx = 0
                '''
                m = PyMatrix.elementary_matrix(\
                option = 'change', 
                i = col_idx, 
                j = row_idx,
                size = s)
                tmp = m * tmp
                lst.append(m)
            '''
            2 1 0 
            0 1 1 
            2 2 2 
            '''
            t_elem = tmp.data[col_idx][col_idx]
            
            
            for idx, elem in enumerate(tmp.cols[col_idx].data[col_idx+1:]):
                
                if elem != 0:
                    # elem -> -t_elem/elem 
                    m = PyMatrix.elementary_matrix(\
                    option = 'multiply', 
                    i = col_idx+idx+1,
                    factor = -t_elem/elem,
                    size = s)
                    lst.append(m)
                    tmp = m * tmp 
                    '''
                    2 1 0 
                    0 1 1 
                    -2 -2 -2 ( -1* (2 2 2))
                    '''
                    # sum col_idx th row col_idx + idx th row 
                    m = PyMatrix.elementary_matrix(\
                    option = 'add', 
                    i = col_idx + idx + 1, 
                    j = col_idx, 
                    size = s)
                    lst.append(m)
                    tmp = m * tmp
            col_idx += 1
        
                
        return lst, tmp
        
    def diagonalize(self):
        col_idx = 0
        lst, tmp = self.gaussian_elimination()
        s = self.size()[0]
        while col_idx != self.size()[1]:   
            t_elem = tmp.data[col_idx][col_idx]
            for idx, elem in enumerate(tmp.cols[col_idx].data[:col_idx]):
                if elem != 0:
                    # elem -> -t_elem/elem 
                    m = PyMatrix.elementary_matrix(\
                        option = 'multiply', 
                        i = idx,
                        factor = -t_elem/elem,
                        size = s)
                    lst.append(m)
                    tmp = m * tmp 
                    
                    # sum col_idx th row col_idx + idx th row 
                    m = PyMatrix.elementary_matrix(\
                        option = 'add', 
                        i = idx, 
                        j = col_idx, 
                        size = s)
                    lst.append(m)
                    tmp = m * tmp
            col_idx += 1
        return lst, tmp
        
    # check if there is a inverse    
    def invertible(self):
        return self.determinant() != 0
        
    # get inverse if it exists. else return None 
    def inverse(self):
        s = self.size()[0]
        lst, tmp = self.diagonalize()
        for i in range(tmp.size()[0]):
            m = PyMatrix.elementary_matrix(\
                option = 'multiply', 
                i = i, 
                factor = 1/tmp.data[i][i],
                size = s,)
            lst.append(m)
        
        m = PyMatrix.identity(s)
        
        for elem in lst:
            m = elem * m
            
        return m
        
    # rank of a matrix 
    def rank(self):
        pass
    
    # QR decomposition
    def QR(self):
        pass
        
    def psuedo_inverse(self):
        return self.transpose()*self
    
    @staticmethod    
    def solve(A, b):
        pass
        
    @staticmethod
    def LLS(A, b):
        pass
    
            
    

