from PySet import PySet, PyCountableSet

class PyFunction(PySet):
    def __init__(self, domain, # domain of a function 
                       func_range, # range of a function 
                       f, ): # relationship 
        pass
    
    def composition(self, other):
        pass
    def calculate(self, args):
        pass

        
if __name__ == '__main__':
    length = PyFunction(PySet(lambda x:isinstance(x, list)), 
                        PySet(lambda x:isinstance(x, int)), 
                        lambda x:len(x),)
                    
    print(length.calculate([1,2,3]))