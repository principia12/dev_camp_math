class MyString:
    class_name = 'MyString'
    maker = 'Schin' 
    
    datum = ''

a = MyString # a is a class
b = MyString() # b is an instance

print(a.class_name) # prints 'MyString'
print(b.class_name) # prints 'MyString'
a.class_name = 'new MyString'
print(a.class_name) # prints 'new MyString'
print(b.class_name) # prints 'new MyString'
b.class_name = 'MyString again' 
print(a.class_name) # prints 'new MyString'
print(b.class_name) # prints 'MyString again'

b.datum = 'hello world!' 
print(b.datum)