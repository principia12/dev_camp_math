#-------------------------------------
# global variables
#-------------------------------------

debug = False

OPERATIONS = {'+' : 1, 
              '-' : 1, 
              '*' : 2, 
              '/' : 2, 
              '^' : 3, } 
              
OPERATION_WITH_FUNCTIONS = {\
    '+' : lambda x,y : x+y,
    '*' : lambda x,y : x*y, 
    '/' : lambda x,y : x/y, 
    '-' : lambda x,y : x-y,
    '^' : lambda x,y : x**y,
}

PARA = ['(', ')', '[', ']', '{', '}',]

#-------------------------------------              
# auxilliary functions
#-------------------------------------

def precedes(l, r):
    assert l in OPERATIONS.keys(), '%s is not a valid operation'%l
    assert r in OPERATIONS.keys(), '%s is not a valid operation'%r
   
    return OPERATIONS[l] >= OPERATIONS[r]

def compress_tok(toks):
    res = []
    cur_type = toks[0][0]
    buf = toks[0][1]
    
    for tok_type, tok in toks[1:]:
        if cur_type == tok_type != 'para':
            buf += tok
        else:
            res.append((cur_type, buf))
            cur_type = tok_type
            buf = tok
    
    res.append((cur_type, buf))

    return res
    
def matching_para(tok):
    assert tok in PARA, 'No paranthesis %s.'%tok
    
    ind = PARA.index(tok)
    if ind%2 == 0:
        return PARA[ind+1]
    else:
        return PARA[ind-1]
        
def opening_para(tok):
    return PARA.index(tok)%2 == 0
   
    
def find_match(tokens, t_idx):
    tok_type, tok = tokens[t_idx]
    if debug:
        print(tok_type, tok)
    assert tok_type == 'para', 'Should find for paranthesis matching.' 
    cnt = 0 
    
    for idx, elem in enumerate(tokens[t_idx:]):
        token_type, token = elem
        if token == tok:
            cnt += 1
        elif token == matching_para(tok):
            cnt -= 1
        
        if cnt < 0:
            assert False, 'Paranthesis matching error!'
        if cnt == 0:
            return idx + t_idx
    
def find_chunk(tokens, t_idx):
    ''' find next chunk to be calculated. 
    '''
    assert tokens[t_idx][0] == 'op', 'Not an operation.'
    
    try:
        if tokens[t_idx+1][0] == 'op':
            assert False, 'Not a valid expression; too many operations.'
    except IndexError:
        assert False, 'Not a valid expression; %s'%str(tokens)
        
    flag = -1
    for idx, token in enumerate(tokens[t_idx+1:]):
        token_type, tok = token
        if idx < flag:
            continue 
            
        if token_type == 'op' and precedes(tokens[t_idx][1], tok):
            # example : 3*4+1 -> * > +, so True
            return (t_idx + 1, idx + t_idx + 1, tok)
        elif token_type == 'para':
            if debug:
                print(tokens)
                print(t_idx + idx + 1)
            flag = find_match(tokens, t_idx + idx + 1)
        
        
    return (t_idx+1, len(tokens), '')


    
#-------------------------------------              
# auxilliary functions
#-------------------------------------
   
def tokenize(equation):
    ''' tokenize equation into tokens. 
    tokens can be either 
    - a numeric value : 0-9 or . 
    - an operator : keys in the dict OPERATIONS
    - a paranthesis : (,),{,},[,]
    - a variable : should be a string of alphabets [a-z, A-Z]
    
    return a list of tuple containing (tok_type, token). 
    '''
    ops = OPERATIONS.keys()
    
    equation = equation.strip()
    equation = equation.replace(' ', '')
    
    para = PARA
    res = []
    minus_flag = False
    
    for c in equation:
        if c in ops:
            if c != '-':
                res.append(('op', c))
            else:
                '''
                res.append(('op', '+'))
                res.append(('num', '-1'))
                res.append(('op', '*'))
                '''
                minus_flag = True
        elif c in para:
            if minus_flag:
                if len(res) == 0:
                    res.append(('num', '-1'))
                    res.append(('op', '*'))
                else:
                    res.append(('op', '+'))
                    res.append(('num', '-1'))
                    res.append(('op', '*'))
                minus_flag = False
            elif len(res) > 0 and res[-1][0] == 'num'\
                    and opening_para(c):
                res.append(('op', '*'))
            
            res.append(('para', c))
        elif c in [str(e) for e in range(9)] or c == '.':
            if minus_flag and len(res) == 0 :
                res.append(('num', '-1'))
                res.append(('op', '*')), 
                res.append(('num', c))
                minus_flag = False
            elif minus_flag and res[-1][0] == 'num':
                res.append(('op', '+'))
                res.append(('num', '-%s'%c))
                minus_flag = False
            elif minus_flag and res[-1][0] == 'op':
                res.append(('num', '-%s'%c))
                minus_flag = False
            elif minus_flag and res[-1][0] == 'para':
                res.append(('num', '-%s'%c))
                minus_flag = False
            else:
                res.append(('num', c))
        
    return compress_tok(res)

    
def evaluate(tokens):
    cur_val = 0
    buf = 0
    variables = []
    
    for idx, token in enumerate(tokens):
        tok_type, tok = token
        if tok_type == 'num':
           cur_val = float(tok)
        elif tok_type == 'op':
            nt_start, nt_end, next_op, = find_chunk(tokens, idx)
            cur_op = OPERATION_WITH_FUNCTIONS[tok]
            if next_op.strip() != '':
                next_op = OPERATION_WITH_FUNCTIONS[next_op]
                return next_op(\
                    cur_op(cur_val, evaluate(tokens[nt_start:nt_end])),
                    evaluate(tokens[nt_end+1:]))
            else:
                return cur_op(cur_val, evaluate(tokens[nt_start:])) 
        elif tok_type == 'para':
            match_idx = find_match(tokens, idx)
            cur_val = evaluate(tokens[idx+1:match_idx])
            
            return evaluate([('num', cur_val)] + tokens[match_idx+1:])
        else:
            raise TypeError
    
    return cur_val       
        
def calucluate(eq):
    return evaluate(tokenize(eq))
        
if __name__ == '__main__':
    
    # tests, tests, more tests! 
    
    # simple numbers
    eq1 = '(1)'
    eq2 = '3'
    eq3 = '-1'
    
    # +,- 
    eq4 = '1+1'
    eq5 = '1-1-2'
    eq6 = '-1-2-3-4-5'
    
    # +,-,*,/ 
    eq7 = '1+2/3+2'
    eq8 = '3*4+2'
    eq9 = '4/2'
    eq10 = '3+4*2'
    eq11 = '3+4/2'
    eq12 = '3/4/2'
    eq13 = '(3/4)/2'
    eq14 = '3/(4/2)'
    eq15 = '1+2/3'
    
    # +,-,*,/,^ with (,)
    eq16 = '(1+2)/3'
    eq17 = '(1*2)/3'
    eq18 = '(1+2)*3'
    eq19 = '3*(1+2)'
    eq20 = '3*(2-1)'
    eq21 = '3*(1-2)'
    eq22 = '3*(-2+1)'
    eq23 = '-3-2^3'
    eq24 = '-3-2^(3+2)'
    eq25 = '-2^3'
    eq26 = '-2^-3'
    
    # +,-,*,/ with nested (,)
    eq27 = '-1+(-1-2)'
    eq28 = '-(2+2)'
    eq29 = '3+(2^(-(2+2)))'
    eq30 = '3(2*2+1)'
    eq31 = '2-3(2*2+1)'
    eq32 = '2-3*(2*(2+1))'
    eq33 = '((3+2)*4-2)*(2+(3+2)*5^2)'
    
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        #print('=============')
        #print(eq)
        print(calculate(eq))
        '''
        try:
            print(calculate(eq))
            assert calculate(eq) == eval(eq.replace('^', '**'))
        except AssertionError:
            print(calculate(eq)), eval(eq.replace('^', '**')))
            assert False
        except TypeError:
            print('Check by yourself')
            print(eq) 
            print(calculate(eq))
        '''