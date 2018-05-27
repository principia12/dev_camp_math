

def sqrt2(digit):
    ''' calculate sqrt(2) to given digit.
    For example, sqrt2(3) = 1.414 
    '''
    lower_limit = 1
    i = 1
    while i!=digit:
        for j in range(11):
            if (lower_limit + j*10**(-i))**2 > 2:
                lower_limit += (j-1)*10**(-i)
                i += 1
                break
    return lower_limit
    
def root2(digit):
    lower_limit = 1
    i = 1
    while i!=digit:
        for j in range(11):
            if (lower_limit + j*10**(-i))**2 > 2:
                lower_limit += (j-1)*10**(-i)
                i += 1
                break
    return lower_limit
    
def const(digit):
    if digit == 1:
        return 1
    elif digit == 2:
        return 1.4 
    else:
        return 1.4

def test_equal(l, r):
    i = 1
    while True:
        if l(i) == r(i):
            i += 1
        else:
            return False
        
    
if __name__ == '__main__':
    print(sqrt2(10))
    print(test_equal(const, sqrt2))
    print(test_equal(sqrt2, root2))