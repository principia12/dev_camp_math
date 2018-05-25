from global_variables import *

class PySet:
    def __init__(self, 
                    membership,): # membership checking 
        self.membership = membership
        
    def __contains__(self, elem):
        return self.membership(elem)
        
    def __add__(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) or g(args), )
        
    def __sub__(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) and not g(args),)
        
    def __mul__(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda arg:f(arg[0]) and g(arg[1]) and len(arg)==2)
        
    def intersection(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) and g(args),)
    
    @staticmethod
    def cup(*sets):
        return PySet(lambda args:any([s.membership(args) for s in sets]))
                                    
    @staticmethod
    def cap(*sets):
        return PySet(lambda args:all([s.membership(args) for s in sets]))
    
    @staticmethod
    def product(*sets):
        ''' return Cartesian product of sets. 
        Following two codes are equivalent. '''
        
        '''
        def member(args):
            res = True
            assert len(sets) == len(args), (sets, args)
            for i in range(len(sets)):
                res = res and sets[i].membership(args[i])
            return res
        return PySet(member)
        '''
        
        return PySet(lambda args:all([s.membership(a) \
                                    for s,a in zip(sets, args)]) and \
                                    len(args) == len(sets))
        
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
        if len(lst) == 1:
            yield lst
            yield ()
        else:
            res = []
            for elem in PyFiniteSet._subsets(lst[1:]):
                yield elem
                yield (lst[0],) + elem
             
    def subsets(self):
        for sub in PyFiniteSet._subsets(self.elements):
            yield PyFiniteSet(*sub)

    def size(self):
        return len(self.elements)
       
    # test for equality and inclusion 
    def __gt__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        for elem in other.elements:
            if elem in self.elements:
                pass
            else:
                return False
        if self.size() > other.size():
            return True
            
    def __ge__(self, other): 
        assert isinstance(other, PyFiniteSet)
        
        for elem in other.elements:
            if elem in self.elements:
                pass
            else:
                return False
        if self.size() >= other.size():
            return True
    
    def __eq__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        for elem in other.elements:
            if elem in self.elements:
                pass
            else:
                return False
        if self.size() == other.size():
            return True
    
    def __ne__(self, other):
        res = False
        for elem in other.elements:
            if elem not in self.elements:
                res = True
                break
                
        if not res:
            return False
        
        for elem in self.elements:
            if elem not in other.elements:
                res = True
        
        return res
    
    def __lt__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        for elem in self.elements:
            if elem in other.elements:
                pass
            else:
                return False
        if self.size() < other.size():
            return True
    
    def __le__(self, other):
        assert isinstance(other, PyFiniteSet)
        
        for elem in self.elements:
            if elem in other.elements:
                pass
            else:
                return False
        if self.size() <= other.size():
            return True
    
        
class PyOrderedSet(PyCountableSet):
    def __init__(self, generator, cmp):
        PyCountableSet.__init__(self, generator)
        self.cmp = cmp

    def list_elements(self, limit = 5, return_sorted = True):
        from functools import cmp_to_key
        '''
        # for your reference, function cmp_to_key looks like below; 
        def cmp_to_key(mycmp):
            'Convert a cmp= function into a key= function'
            class K:
                def __init__(self, obj, *args):
                    self.obj = obj
                def __lt__(self, other):
                    return mycmp(self.obj, other.obj) < 0
                def __gt__(self, other):
                    return mycmp(self.obj, other.obj) > 0
                def __eq__(self, other):
                    return mycmp(self.obj, other.obj) == 0
                def __le__(self, other):
                    return mycmp(self.obj, other.obj) <= 0
                def __ge__(self, other):
                    return mycmp(self.obj, other.obj) >= 0
                def __ne__(self, other):
                    return mycmp(self.obj, other.obj) != 0
            return K
        '''
        i = 0
        g = self.generator()
        history = []
        while i<limit:
            try:
                a = next(g)
                if a not in history:
                    history.append(a)
                    i += 1
                
            except StopIteration:
                break
        if return_sorted:
            history.sort(key = cmp_to_key(self.cmp))
        for elem in history:
            print(elem)
        
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
    