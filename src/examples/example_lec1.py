class PySet:
    def __init__(self, membership):
        self.membership = membership 
        
    def __contains__(self, elem):
        print('__contains__ function called!')
        return self.membership(elem)

    def __add__(self, other):
        print('__add__ function called!')
        '''
        def membership(arg):
            return arg in self or \
                    arg in other
        '''
        
        return PySet(lambda arg: arg in self or \
                                arg in other)
        pass
    def __sub__(self, other):
        print('__sub__ function called!')
        '''
        def membership(arg):
            return arg in self and \
                    not arg in other
        '''
        return PySet(lambda arg :arg in self and \
                    not arg in other)
    
    def __mul__(self, other):
        def membership(x):
            return x[0] in self and x[1] in other
        return PySet(membership)
        
    @staticmethod
    def cup(*args):
        # cup(even, odd, els, ...)
        # args = (even, odd, els, ...)
        
        def membership(x):
            res = False
            for s in args:
                res = res or x in s
            return res
            
        return PySet(membership)   
        
    @staticmethod
    def cap(*args):
        def membership(x):
            res = True
            for s in args:
                res = res and x in s
            return res
            
        return PySet(membership)   
    
    @staticmethod
    def inter(l, r):
        return PySet(lambda arg: arg in l and arg in r)
        
    
    
    def intersection(self, other):
        print('intersection function called!')
        '''
        def membership(arg):
            return arg in self and \
                    arg in other
        '''
        return PySet(lambda arg: arg in self and \
                                arg in other)
                                
class PyFiniteSet(PySet):
    def __init__(self, *elements):
        def membership(arg):
            return arg in elements
        PySet.__init__(self, membership)
        self.elements = elements
        
        
    def size(self):
        return len(element)
    
    def subset(self):
        for elem in PyFiniteSet._subset_util(self.elements):
            yield PyFiniteSet(*elem)
        
    @staticmethod
    def _subset_util(lst): 
        if lst == []:
            return []
        elif len(lst) == 1:
            return [[], lst]
        else:
            res = []
            head, tail = lst[0], lst[1:]
            for e in PyFiniteSet._subset_util(tail):
                res.append(e)
                res.append((head,) + e)
                
            return res
        
    def __gt__(self, other):
        # self > other? 
        res = True
        for elem in other.elements:
            res = res and elem in self.elements
        if self.size() != other.size():
            return res
            
            
    def __ge__(self, other): 
        return __gt__(self, other) or\
            __eq__(self, other)
    
    def __eq__(self, other):
        res = True
        for elem in self.elements:
            res = res and elem in other.elements
            
        for elem in other.elements:
            res = res and elem in self.elements
            
            
        res = res and elem.size() == other.size()
        
        return res
        
    def __ne__(self, other):
        return not PySet.__eq__(self, other)
        
    def __lt__(self, other):
        res = True
        for elem in self.elements:
            res = res and elem in other.elements
        if self.size() != other.size():
            return res
    
    def __le__(self, other):
        return PySet.__eq__(self, other) or\
            PySet.__lt__(self, other)
        
a = PyFiniteSet(1,2,3)
b = PyFiniteSet(2,3,4)
d = PyFiniteSet(1)
e = PyFiniteSet(1,2,3,4,5)

for elem in e.subset():
    print(elem.elements)

c = PySet(lambda x:x%2==0)

