# from global_variables import *

class Field:
    def __init__(self, set, addition, multiplication, one, zero):
        self.set = set
        self.adddition = addition 
        self.multiplication = multiplication    
        
        assert one in set
        assert zero in set
        
        self.one = one
        self.zero = zero
        