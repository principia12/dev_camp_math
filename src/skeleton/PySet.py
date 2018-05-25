from global_variables import *

class PySet:
    def __init__(self, 
                    membership,): # membership checking 
        self.membership = membership
        
    def __contains__(self, elem):
        pass
        
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def intersection(self, other):
        pass
    @staticmethod
    def cup(*sets):
        pass                            
    @staticmethod
    def cap(*sets):
        pass
    @staticmethod
    def product(*sets):
        pass
        
class PyCountableSet(PySet):
    def __init__(self, generator, given_membership = None):
        if given_membership is None:
            membership = generator2membership(generator)
            PySet.__init__(self, membership)
        else:
            PySet.__init__(self, given_membership)
        self.generator = generator
        
    def list_elements(self, limit = 5,):
        i = 0
        g = self.generator()
        history = []
        while i<limit:
            try:
                a = next(g)
                if a not in history:
                    print(a)
                    history.append(a)
                    i += 1
                
            except StopIteration:
                break
                
    def __iter__(self):
        yield from self.generator()
                
                
class PyFiniteSet(PySet):
    def __init__(self,*elements):
        for elem in elements:
            assert elements.count(elem) == 1 # every element is unique
        PySet.__init__(self, lambda x:x in elements)
        self.elements = elements
        
    def __str__(self):
        res = '{'
        for elem in self.elements:
            res += '%s, '%str(elem)
        res = res.strip(', ')
        res += '}'
        return res
        
    def __iter__(self):
        for elem in self.elements:
            yield elem 
    
    def __contains__(self, item):
        return item in self.elements
        
    def __add__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        res = []
        for elem in self.elements:
            res.append(elem)
            
        for elem in other.elements:
            if elem not in res:
                res.append(elem)
        return PyFiniteSet(*res)
        
    def __sub__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        res = []
        for elem in self.elements:
            if elem not in other.elements:
                res.append(elem)
                
        return PyFiniteSet(*res)
        
    def intersection(self, other):
        assert isinstance(other, PyFiniteSet)
        
        res = []
        for elem in self.elements:
            if elem in other.elements:
                res.append(elem)
        
        return PyFiniteSet(*res)
    
    @staticmethod
    def _subsets(lst):
        pass     
    def subsets(self):
        pass
    def size(self):
        pass
       
    # test for equality and inclusion 
    def __gt__(self, other):
        pass    
    def __ge__(self, other): 
        pass
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        pass
    def __lt__(self, other):
        pass
    def __le__(self, other):
        pass
        
class PyOrderedSet(PyCountableSet):
    def __init__(self, generator, cmp):
        PyCountableSet.__init__(self, generator)
        self.cmp = cmp

    def __iter__(self):
        yield from self.generator()
        
class PyPartiallyOrderedSet(PyCountableSet):
    def __init__(self, generator, cmp):
        PyCountableSet.__init__(self, generator)
        # cmp will get two inputs, and return True, False, or None. 
        self.cmp = cmp

    def __iter__(self):
        yield from self.generator()
        
    def topological_sort(self):
        V = [v for v in self.generator()]
        E = []
        for u in V:
            for v in V:
                if self.cmp(u, v): 
                    E.append((u, v))
        return Graph(V,E).topological_sort()
            
    
if __name__ == '__main__':
    a = PySet(lambda x:x%2==0)  # {x|x is even}
    b = PySet(lambda x:x in [1,2,3]) # {1,2,3}
    f = PyFiniteSet([1,2,3])

    c = a+b
    d = a.intersection(b)
    e = PySet.product(a,b,c,d)
    print(e.membership((2, 1, 3, 2)))
    print(e.membership((2, 1, 3, 100)))
    print(c.membership(2))
    print(d.membership(1))
    
    def even_number_generator():
        i = 0
        while True:
            yield 2*i
            i += 1
    
    f = PyCountableSet(even_number_generator)
    print(f.membership(200))
    
    print(isinstance(f, PySet))
    