def func1(input_num):
    a = int(input_num[0])
    b = int(input_num[1])
    c = int(input_num[2])
    
    
    return func2(a,b,c,)
    
def func2(a,b,c):
    return 100*c + 10*b + a
    
print(func1('123'))