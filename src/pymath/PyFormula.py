from PyFunction import PyFunction
from PySet import PySet, PyCountableSet
from util import *
from copy import deepcopy

import math

#-------------------------------------              
# Formula Class
#-------------------------------------

class PyFormula(): # might inherit from PyFunction class
    ''' Function from PyRational to PyRational
    '''
    def __init__(self, formula):
        if isinstance(formula, str):
            self.formula = formula
            tree = parse(tokenize(formula))
            self.tree = tree
            var_list = [x[1] for x in tree.nodes() if x[0] == 'var']
            self.variables = PyCountableSet(lambda :(x for x in var_list))
        elif isinstance(formula, Tree):
            self.tree = formula
            self.formula = tree2str(formula)
            var_list = [x[1] for x in formula.nodes() if x[0] == 'var']
            self.variables = PyCountableSet(lambda :(x for x in var_list))
        else:
            print('Input should be either tree or a string.')
            raise TypeError
           
        
    def __add__(self, other): 
        return PyFormula('(' + self.formula + ')+(' + other.formula + ')',)
    
    def __sub__(self, other):
        return PyFormula('(' + self.formula + ')-(' + other.formula + ')',)
    
    def __mul__(self, other):
        return PyFormula('(' + self.formula + ')*(' + other.formula + ')',)

    def __div__(self, other):
        return PyFormula('(' + self.formula + ')/(' + other.formula + ')',)
        
    def __str__(self):
        return self.formula
        
    def terms(self):
        if self.tree.datum[1] == '+':
            return self.tree.children
        return self        
    
    def simplify(self):
        var_coeff_dict = {}
        
    def __call__(self, *value_list, **value_dict):
        if value_dict == {}:
            assert len(list(self.variables.generator())) == len(value_list),\
                    'Not a valid input.'
            value_dict = {}
            for var,val in zip(\
                    sorted(list(self.variables.generator())), value_list):
                value_dict[var] = val
            return PyFormula._calculate(self.tree, value_dict)
        elif value_list == ():
            assert set(self.variables.generator()) == set(value_dict.keys()), \
                    'Not a valid input.'
            
            return PyFormula._calculate(self.tree, value_dict)
        else:
            print(value_list, value_dict)
            raise TypeError
    
    @staticmethod    
    def _calculate(tree, value_dict):
        if tree.datum[0] == 'op':
            args = [PyFormula._calculate(c, value_dict) for c in tree.children]
            return OPERATION_WITH_FUNCTIONS[tree.datum[1]](*args)
        elif tree.datum[0] == 'num':
            return tree.datum[1]
        elif tree.datum[0] == 'var':
            return value_dict[tree.datum[1]]
        elif tree.datum[0] == 'func':
            args = [PyFormula._calculate(c, value_dict) for c in tree.children]
            return FUNCTION_DICT[tree.datum[1]](args)
    
        


#-------------------------------------
# global variables
#-------------------------------------

debug = False

OPERATIONS = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, 
    } 
              
OPERATION_WITH_FUNCTIONS = {\
    '+' : binary2nary(lambda x,y : x+y),
    '*' : binary2nary(lambda x,y : x*y), 
    '/' : binary2nary(lambda x,y : x/y), 
    '-' : binary2nary(lambda x,y : x-y),
    '^' : binary2nary(lambda x,y : x**y),
    }

PARA = ['(', ')', '[', ']', '{', '}',]

FUNCTION_DICT = {\
    'cos' : math.cos, 
    'sin' : math.sin, 
    'tan' : math.tan, 
    'cosh' : math.cosh,
    'sinh' : math.sinh,
    'tanh' : math.tanh,
    'e' : lambda : math.e, 
    'pi' : lambda : math.pi, 
    'ln' : math.log,
    'log' : math.log10,
    }

#-------------------------------------              
# auxilliary functions
#-------------------------------------


def precedes(l, r, eq = True):
    assert l in OPERATIONS.keys(), '%s is not a valid operation'%l
    assert r in OPERATIONS.keys(), '%s is not a valid operation'%r
    if not eq:
        return OPERATIONS[l] > OPERATIONS[r]
    return OPERATIONS[l] >= OPERATIONS[r]

def compress_tok(toks):
    res = []
    cur_type = toks[0][0]
    buf = toks[0][1]
    
    for tok_type, tok in toks[1:]:
        if cur_type == tok_type and not tok_type in ['para',]:
            buf += tok
        else:
            if buf.isalpha():
                if buf in FUNCTION_DICT.keys(): 
                    res.append(('func', buf))
                else:
                    for c in buf:
                        res.append(('var', c))
            else:    
                res.append((cur_type, buf))
            cur_type = tok_type
            buf = tok
    if buf in FUNCTION_DICT.keys():
        res.append(('func', buf))
    else:
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
    return len(tokens)+1
    
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

def parse_args(tokens):
    res = [[]]
    for tok in tokens:
        if tok[0] == 'comma':
            res.append([])
        else:
            res[-1].append(tok)
    return [parse(e) for e in res]
    
def tree2str(tree):
    res = ''
    if tree.datum[0] == 'op':
        if tree.children != []:
            for child in tree.children[:-1]:
                res += '(%s)'%tree2str(child)
                res += str(tree.datum[1])
            res += '(%s)'%tree2str(tree.children[-1])
        else:
            res = str(tree.datum[1])
    elif tree.datum[0] == 'func':
        res += str(tree.datum[1])
        res += '('
        for child in tree.children:
            res += '%s, '%tree2str(child)
        res += ')'
    elif tree.datum[0] in ['num', 'var']:
        res = str(tree.datum[1])
        
    return res
    
#-------------------------------------              
# parsing functions
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
                #res.append(('num', '-1'))
                #res.append(('op', '*')), 
                res.append(('num', '-%s'%c))
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
        elif c.isalpha():
            res.append(['var', c])
        elif c == ',':
            res.append(['comma', c])
        
    return compress_tok(res)

def parse(tokens, debug = False):
    ''' Parse tokens to a binary tree
    '''
    cur_tree = Tree((None, None))
    empty_flag = []
    pass_flag = -1
    para_flag = []
    
    for idx, token in enumerate(tokens):
        if debug:
            if idx<pass_flag and False:
                print('-------------')
                print(idx, token)
            else:
                print('-------------')
                print(idx, token)    
                print(cur_tree)
                print('para flag')
                for e in para_flag:
                    print('~~~~~~~~')
                    print(e)
                print('~~~~~~~~')
                print('empty flag')
                for e in empty_flag:
                    print('~~~~~~~~')
                    print(e)
                print('~~~~~~~~')
            
        assert isinstance(cur_tree.datum, tuple), cur_tree.datum
        tok_type, tok = token 
        if idx < pass_flag:
            continue
        
        if tok_type in ['num', 'var']:
            if cur_tree.datum[0] == 'op':
                # empty flag can be optimized... how? CHANGE NEEDED
                if empty_flag != []:
                    empty_tree = empty_flag.pop()
                    cur_tree.append_to_subtree(token, empty_tree)
                else:
                    cur_tree.children.append(Tree(token))
            elif cur_tree.datum[0] in ['var', 'func']:
                cur_tree = Tree(('op', '*'), [cur_tree, Tree(token)])
            elif cur_tree.datum[0] == 'num':
                if tok_type == 'num':
                    assert False, 'Syntax error in %dth token, %s'%(idx, tokens)
                else:
                    cur_tree = Tree(('op', '*'), [cur_tree, Tree(token)])
            else:
                cur_tree = Tree(token)
                
        elif tok_type == 'op':
            if cur_tree.datum[0] in ['var', 'num', 'func']:
                cur_tree =  Tree(token, [cur_tree])
            elif cur_tree.datum[0] == 'op':
                cur_pos = cur_tree
                cur_op = cur_pos.datum[1]
                next_op = tok
                if precedes(next_op, cur_op, eq = False):
                    if para_flag == []:
                        while cur_pos.datum[0] not in ['num', 'var', 'func']        and precedes(next_op, cur_op, eq = False):
                            cur_pos = cur_pos.children[-1]
                            cur_op = cur_pos.datum[1]
                        
                        if cur_pos.datum[0] in ['num', 'var', 'func']:
                            tmp = cur_pos.copy()
                            cur_pos.children = [tmp]
                            cur_pos.datum = token
                            
                        elif cur_pos.datum[0] == 'op':
                            tmp = cur_pos.copy()
                            cur_pos.children = [tmp]
                            cur_pos.datum = token
                        else:
                            raise TypeError
                        empty_flag.append(cur_pos)
                    else: 
                        # para_flag points to the root of () term
                        para_tree = para_flag.pop()
                        tmp = para_tree.copy()
                        para_tree.children = [tmp]
                        para_tree.datum = token
                        empty_flag.append(para_tree)
                        #para_flag = []
                elif next_op == cur_op:
                    continue
                else:
                    cur_tree = Tree(token, [cur_tree,])
                    empty_flag.append(cur_tree)
            #elif cur_tree.datum[0] == 'func':
        elif tok_type == 'para':
            if opening_para(tok):
                pass_flag = find_match(tokens, idx)
                next_tree = parse(tokens[idx+1:pass_flag])
                if cur_tree.datum[0] == 'op':
                    if empty_flag != []:
                        empty_tree = empty_flag.pop()
                        cur_tree.append_to_subtree(next_tree, empty_tree)
                        para_flag.append(next_tree)
                    else:
                        #pth = cur_tree.append_leftmost(next_tree)
                        cur_tree.append_leftmost(next_tree)
                        para_flag.append(next_tree)
                elif cur_tree.datum[0] in ['num', 'var']:
                    cur_tree = Tree(('op', '*'), [cur_tree, next_tree])
                    para_flag.append(cur_tree.children[1])
                else:
                    cur_tree = next_tree
                    para_flag.append(cur_tree)
            #else:
            #    cur_tree.children.append(para_flag
        elif tok_type == 'func': 
            if len(tokens) == 1:
                return Tree(token)
            try:
                pass_flag = find_match(tokens, idx+1)
                args = parse_args(tokens[idx+2:pass_flag])
                func_tree = Tree(token, args)
            except AssertionError:
                func_tree = Tree(token)
            if cur_tree.datum[0] in ['num', 'var',]:
                pass
            elif cur_tree.datum[0] == 'op':
                if empty_flag != []:
                    empty_tree = empty_flag.pop()
                    cur_tree.append_to_subtree(func_tree, empty_tree)
                else:
                    cur_tree.children.append(func_tree)
            else:
                cur_tree = func_tree
        else:
            raise TypeError
            
        if debug:
            print(cur_tree)
            print('-------------')
    if debug:
        print(eq)
    return cur_tree
   
    
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
    eq33 = '((3+2)*4-(2*4+2^(2-5)))*(2+(3+2)*5^2)'
    eq34 = '2+(3+2)*5^2'
    eq35 = '1+2^2*1'
    '''
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        try:
            print(tokenize(eq))
            print(evaluate(tokenize(eq)))
            assert evaluate(tokenize(eq)) == eval(eq.replace('^', '**'))
        except AssertionError:
            print(evaluate(tokenize(eq)), eval(eq.replace('^', '**')))
            assert False
        except TypeError:
            print('Check by yourself.')
            print(eq) 
            print(evaluate(tokenize(eq)))
    
    
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        print(parse(tokenize(eq)))
        
    '''
    '''
    eq = eq33
    
    print(eq)
    print(tokenize(eq))
    print(parse(tokenize(eq), debug = True))
    '''
    
    formula1 = 'x'
    formula2 = 'xz+y'
    formula3 = 'cos(pi)'
    formula4 = 'cos(x)'
    formula5 = '1+3^3*c'
    formula6 = 'sin(x)^2 + cos(y)'
    formula7 = 'sin(e^(pi/2) + 1)'
    formula8 = 'sin(cos(tan(x)))'
    formula9 = 'sin(x) * cos(y) - cos(x) * sin(y)'
    formula10 = 'a+b+C+d+e+f+g+h'
    
    for i in range(100):
        try:
            eq = eval('formula%d'%i)
            formula = PyFormula(eq)
        except NameError:
            continue
            
        print('==================')
        print(eq)
        print(tokenize(eq))
        print(parse(tokenize(eq)))
        #formula.variables.list_elements()
        print(PyFormula(parse(tokenize(eq))))
    
    '''
    eq = formula9
    print(eq)
    f = PyFormula(eq)
    print(parse(tokenize(eq), debug = True))
    '''
    
    eq = PyFormula(formula2)
    print(eq(1,2,3))
    print(eq(x = 1, y = 2, z = 3)) 
    
    
    