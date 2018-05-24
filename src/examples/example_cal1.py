result = 0

def adder(num):
    global result
    result += num 
    return result 
    
print(adder(3))
print(adder(4))