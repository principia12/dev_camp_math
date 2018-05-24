class MyString:
    class_name = 'MyString'
    maker = 'Schin' 
    
    def __init__(self, datum = ''):
        self.datum = datum
    
    # instance method
    def get_first_letter(self):
        return self.datum[0]
    
    def most_frequent_word(self):
        bow = MyString._create_bow(self.datum)
        res = ''
        tmp = 0
        for k in bow.keys():
            if bow[k] > tmp:
                res = k
                tmp = bow[k]
        return res
    
    # magic method     
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return MyString(datum = self.datum + other.datum)
        return NotImplemented
    
    @classmethod
    def assign_author(cls, author):
        cls.author = author
        
    @staticmethod
    def _create_bow(input_str):
        res = {}
        for elem in input_str.split():
            if elem in res.keys():
                res[elem] += 1
            else:
                res[elem] = 1
        return res

a = MyString('hello')
b = MyString('world') 

print(a.get_first_letter())

c = a+b # MyString('helloworld') 
print(c.datum)

c.assign_author('Shin')
print(c.author)
print(a.author)

d = MyString('hello world it is so nice to meet you how are you doing world')
print(d.most_frequent_word())