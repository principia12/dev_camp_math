from example_sequence1 import *

print('e' in d) # True
print([1,2,3] + [4,5,6]) # [1,2,3,4,5,6]
print(d[1]) # 'e'
print(d[1:3]) # 'el'
print(d[1:6:2]) # 'el '
print(d[::-1]) # !dlrow olleh'
print(len(d)) # 12
for idx, elem in enumerate(d):
    print(idx, elem) 
