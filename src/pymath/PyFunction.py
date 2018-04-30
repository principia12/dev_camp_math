from PySet import PySet, PyCountableSet

class PyFunction(PySet):
    def __init__(self, domain, # domain of a function 
                       func_range, # range of a function 
                       f, ): 
        def member(args):
            x,y = args
            return domain.membership(x) and func_range.membership(y) and \
                        y == f(x)
        PySet.__init__(self, member)
        self.domain = domain
        self.func_range = func_range
        self.f = f
        
    def calculate(self, args):
        assert self.domain.membership(args)
        assert self.func_range.membership(self.f(args))
        
        return self.f(args)

        
if __name__ == '__main__':
    length = PyFunction(PySet(lambda x:isinstance(x, list)), 
                        PySet(lambda x:isinstance(x, int)), 
                        lambda x:len(x),)
                    
    print(length.calculate([1,2,3]))