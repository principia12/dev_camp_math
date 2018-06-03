import re

if __name__ == '__main__':

    pattern1 = r''
    pattern2 = r''

    phone_num = ['010-8750-4742', '011-222-2323', '010-2325-1111',]
    for elem in phone_num:  
        assert re.match(pattern1, phoen_num, )
    emails = ['principia12@kaist.com', 'hello1231@gmail.com', 'goodbye@daum.com']
    
    for elem in emails:
        assert re.match(pattern2, emails)
    sent1 = ''
    sent2 = ''
    
    assert re.match(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', sent1)
    assert re.match(r'^#.*$', sent2)
