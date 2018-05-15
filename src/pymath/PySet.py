from global_variables import *

class PySet:
    def __init__(self, 
                    membership, # membership checking 아리랑
                    eq_func,): # equivalance checking function between elements
        self.membership = membership
        self.eq_func = eq_func
        
    def __add__(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) or g(args))
        
    def __sub__(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) and not g(args))
        
    def intersection(self, other):
        f, g = self.membership, other.membership
        return PySet(lambda args:f(args) and g(args))
    
    @staticmethod
    def cup(*sets):
        return PySet(lambda args:any([s.membership(args)\
                                    for s in sets]))
                                    
    @staticmethod
    def hat(*sets):
        return PySet(lambda args:all([s.membership(args)\
                                    for s in sets]))
    
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
                                    for s,a in zip(sets, args)]))
        
class PyCountableSet(PySet):
    def __init__(self, generator):
        def membership(args):
            a = generator()
            i = 0
            while i<MAXIMUM_ITERATION:
                if args == next(a):
                    return True
                i += 1
                
        PySet.__init__(self, membership)
        self.generator = generator
        
    def list_elements(self, limit = 100,):
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
            
    
    
if __name__ == '__main__':
    a = PySet(lambda x:x%2==0)  # {x|x is even}
    b = PySet(lambda x:x in [1,2,3]) # {1,2,3}

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
    