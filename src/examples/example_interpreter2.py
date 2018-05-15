def func2(n): #calculate n!
    if n == 1:
        return 1
    else:
        return n*func2(n-1)