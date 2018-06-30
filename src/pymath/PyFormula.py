from PyFunction import PyFunction
from PySet import PySet, PyFiniteSet
from util import *
from global_variables import *
from copy import deepcopy

import math
import re



#-------------------------------------              
# Formula Class
#-------------------------------------

class PyFormula: 
    ''' PyFormula is essentially a instance of util.Tree parsed from string equation. It can also be instantiated using tree. 
    '''
    def __init__(self, 
                    eq, 
                    constant_variable = [], 
                    debug = False):
        if isinstance(eq, str):
            self.eq = eq
            tree = parse(eq)
            self.tree = tree
            var_list = [x.datum[1] for x in tree.leaves() \
                            if x.datum[0] == 'var']
            var_list = list(set(var_list))                
            self.variables = PyFiniteSet(*var_list)
        elif isinstance(eq, Tree):
            self.tree = eq
            self.eq = PyFormula._tree2str(eq)
            var_list = [x.datum[1] for x in eq.nodes() \
                            if x.datum[0] == 'var']
            var_list = list(set(var_list))
            self.variables = PyFiniteSet(*var_list)
        else:
            print('Input should be either tree or a string.')
            raise TypeError
        
    def __add__(self, other): 
        return PyFormula('(' + self.eq + ')+(' + other.eq + ')',)
    
    def __sub__(self, other):
        return PyFormula('(' + self.eq + ')-(' + other.eq + ')',)
    
    def __mul__(self, other):
        return PyFormula('(' + self.eq + ')*(' + other.eq + ')',)

    def __div__(self, other):
        return PyFormula('(' + self.eq + ')/(' + other.eq + ')',)
        
    def __str__(self):
        return self.eq
        
    def terms(self):
        if self.tree.datum[1] == '+':
            return self.tree.children
        return self   

    def substitute(self, var, val):
        # find var token and replace to val Tree or PyFormula
        tree = self.tree
        return PyFormula(tree.replace_subtree(Tree(datum = var), val))
        
    
    def _expand(self):
        pass
        
    def _factorization(self):
        pass
        
    def simplify(self):
        var_coeff_dict = {}
        
    def solve(self, variables):
        pass
        
    def __call__(self, *value_list, **value_dict):
        if value_dict == {}:
            assert self.variables.size() == len(value_list),\
                    'Not a valid input.'
            value_dict = {}
            for var,val in zip(\
                    sorted(self.variables.elements), value_list):
                value_dict[var] = val
            return PyFormula._calculate(self.tree, value_dict)
        elif value_list == ():
            assert set(self.variables.elements) == set(value_dict.keys()), \
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
        else:
            assert False, 'TypeError : invalid type %s'%str(tree.datum[1])
    
    @staticmethod
    def _tree2str(tree):
        assert isinstance(tree, Tree)
        res = ''
        #if tree.children == []:
        #    return str(tree.datum[1])
        if tree.datum[0] == 'op':
            if tree.children != []:
                if tree.datum[1] == '*':
                    for child in tree.children:
                        if child.children == []:
                            if child.datum[1] == '1':
                                pass
                            else:
                                res += str(child.datum[1])
                        elif child.datum[0] == 'func':
                            res += '%s'%PyFormula._tree2str(child)
                        else:
                            res += '(%s)'%PyFormula._tree2str(child)
                        res += '*'
                    res = res.strip('*')
                elif tree.datum[1] == '/':
                    denom, numer = '', ''
                    for idx, child in enumerate(tree.children):
                        if idx%2 == 0:
                            if child.children == []:
                                denom += str(child.datum[1])
                            else:
                                denom += '(%s)'%PyFormula._tree2str(child)
                        else:
                            if child.children == []:
                                numer += str(child.datum[1])
                            else:
                                numer += '(%s)'%PyFormula._tree2str(child)
                                
                    res = '%s/%s'%(denom, numer)
                else:
                    
                    for idx, child in enumerate(tree.children):
                        if child.children == []:
                            res += str(child.datum[1])
                        else:
                            res += '(%s)'%PyFormula._tree2str(child)
                        if idx != len(tree.children)-1:
                            res += str(tree.datum[1])
            else:
                res = str(tree.datum[1])
        elif tree.datum[0] in ['num', 'var']:
            res = str(tree.datum[1])
        elif tree.datum[0] in ['func']:
            res = tree.datum[1] 
            res += '('
            for child in tree.children:
                res += PyFormula._tree2str(child)
                res += ','
            res = res[:-1]
            res += ')' 
            
        return res    


precedence = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, 
    'unary -' : 4}
    
def tokenizer(equation):
    left = equation.replace(' ', '')
    tokens = {\
        'op' : ['^', '+', '-', '*', '+', '/'],
        'unary' :  ['-'],
        'para' : ['(', ')'],
        'num' : [r"[1-9][0-9]*\.?[0-9]*|0",],
        'var' : [r"[a-zA-Z]+_?[0-9]*",], 
        'comma' : [',']}
    
    #tok_strings = tokens['op'] + tokens['unary'] + \
    #    tokens['para'] + tokens['num'] + tokens['var'] 
    tok_strings = []
    for k in tokens.keys():
        tok_strings.extend(tokens[k])
    num_flag = False
    def find_key_from_elem(d, e):
        res = []
        for k in d.keys():
            if e in d[k]:
                res.append(k)
        return res
    
    while left != '':
        for tok in tok_strings:
            if tok in tokens['num']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('num', left[m.start():m.end()]))
                    left = left[m.end():]
                    num_flag = True
            elif tok in tokens['comma']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('comma', left[m.start():m.end()]))
                    left = left[m.end():]
            elif tok in tokens['var']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('var', left[m.start():m.end()]))
                    left = left[m.end():]
                    num_flag = True
            else:
                if left.startswith(tok):
                    k = find_key_from_elem(tokens, tok)
                    
                    if len(k) == 1:
                        yield (k[0], left[0])
                    else:
                        if num_flag:
                            yield ('op', '+')
                            yield ('unary', 'unary %s'%left[0])
                        else:
                            yield ('unary', 'unary %s'%left[0])
                    left = left[1:]        
                    num_flag = False
                    
    
def compress_tok(tokenizer):
    for tok_type, tok in tokenizer:
        if tok_type == 'var' and tok in FUNCTION_DICT.keys():
                yield ('func', tok)
        else:
            yield (tok_type, tok)
            
    
def recursive_descent(tokens):
    
    operator = Stack()
    operand = Stack()
    idx = expr(operator, operand, tokens, 0)
    res = operand.pop()
    
    return res
    
def expr(operator, operand, tokens, idx):
    # expr := part (binary part)*
    idx = part(operator, operand, tokens, idx)
    idx += 1
    if idx != len(tokens):        
        next_tok = tokens[idx]
        
        while next_tok[1] in ['^', '+', '-', '*', '/']:
            push_operator(operator, operand, next_tok)
            idx += 1
            idx = part(operator, operand, tokens, idx)
            idx += 1
            try:
                next_tok = tokens[idx]
            except IndexError:
                next_tok = [None, None]
    
    while not operator.is_empty():
        pop_operator(operator, operand)
        
        
    return idx
        
def find_match(tokens, t_idx):
    tok_type, tok = tokens[t_idx]
    
    assert tok_type == 'para' and tok == '(', \
            'Should find for paranthesis matching.' 
    cnt = 0 
    
    for idx, elem in enumerate(tokens[t_idx:]):
        token_type, token = elem
        if token == tok:
            cnt += 1
        elif token == ')':
            cnt -= 1
        
        if cnt < 0:
            assert False, 'Paranthesis matching error!'
        if cnt == 0:
            return idx + t_idx
    return len(tokens)+1
    
def part(operator, operand, tokens, idx):
    # part := num | var 
    #      := "(" expr ")"
    #      := func "(" (expr ,)* expr ")"
    #      := unary part 
    
    next_tok = tokens[idx]
    
    if next_tok[0] == 'num' or next_tok[0] == 'var':
        # part := num | var
        operand.push(Tree(datum=next_tok))
    elif next_tok[1] == '(':
        # part := "(" expr ")"
        tokens_in_para = tokens[idx+1:find_match(tokens, idx)]
        e = recursive_descent(tokens_in_para)
        idx = find_match(tokens, idx) 
        operand.push(e)
        tokens = tokens[idx:]
    elif next_tok[0] == 'unary':
        # part := unary part
        push_operator(operator, operand, next_tok)
        idx += 1
        idx = part(operator, operand, tokens,  idx)
    elif next_tok[0] == 'func':
        # part := func "(" (expr ,)* expr ")"
        
        idx += 1
        tokens_in_para = tokens[idx+1:find_match(tokens, idx)]
        args = [[]]
        
        for tok_type, tok in tokens_in_para:
            if tok_type == 'comma':
                args.append([])
            else:
                args[-1].append((tok_type, tok))
        
        args = [recursive_descent(arg) for arg in args]
        idx = find_match(tokens, idx)
        
        operand.push(Tree(datum=next_tok, children = args))
        
    else:
        assert False, 'Something wrong at %s'%str(tokens[idx])
    return idx
    
def pop_operator(operator, operand):
    top = operator.pop()
    if top[1] in ['+', '*', '/', '^', '-']:
        arg1 = operand.pop()
        arg2 = operand.pop()
        operand.push(Tree(datum = top, children = [arg2, arg1]))
    elif top[1] in ['unary -',]:
        arg1 = operand.pop()

        if isinstance(arg1, Tree):
            if (arg1.children == [] and arg1.datum[0] == 'num'):
                operand.push(Tree(datum = ('num', '-%s'%arg1.datum[1])))
            else:
                operand.push(Tree(datum = ('op', '*'), \
                        children = [('num', -1), arg1]))
        else:   
            operand.push(Tree(datum = ('num', '-%s'%arg1[1])))
    else:
        assert False, 'operator expected; not a valid operator %s'%str(top)

def push_operator(operator, operand, op):
    if not operator.is_empty():
        top = operator.top()
        while precedence[top[1]] > precedence[op[1]]:
            pop_operator(operator, operand)
            top = operator.top()
            if top is None:
                break
    operator.push(op)
    
def parse(eq):
    return recursive_descent(list(compress_tok(tokenizer(eq))))

    
        
if __name__ == '__main__':
    
    # tests, tests, more tests! 
    
    # simple numbers
    eq1 = '(1)'
    eq2 = '3'
    eq3 = '-1'
    
    # +,- 
    eq4 = '1+1'
    eq5 = '1-1-2' # check
    eq6 = '-1-2-3-4-5'
    
    # +,-,*,/ 
    eq7 = '1+2/3+2'
    eq8 = '3*4+2'
    eq9 = '4/2'
    eq10 = '3+4*2'
    eq11 = '3+4/2'
    eq12 = '3/4/2'
    eq13 = '(3/4)/2' # check
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
    eq30 = '3*(2*2+1)'
    eq31 = '2-3*(2*2+1)'
    eq32 = '2-3*(2*(2+1))'
    eq33 = '((3+2)*4-(2*4+2^(2-5)))*(2+(3+2)*5^2)'
    eq34 = '2+(3+2)*5^2'
    eq35 = '1+2^2*1'
    
    eq36 = 'x'
    eq37 = '-x_0*z+y'
    eq40 = '1+3^3*c'
    eq45 = 'a+b+C+d+e+f+g+h'
    eq46 = '1'
    eq47 = '0'
    
    eq48 = 'sin(x+y)'
    for t, tok in compress_tok(tokenizer(eq48)):
        print(t, tok)
       
    print(parse(eq48))
    
    '''
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        for t, tok in compress_tok(tokenizer(eq)):
            print(t, tok)
        #print(parse(eq))
        print('=============')
    eq = PyFormula(eq37)
    print(eq(1,2,3))
    print(eq(x_0 = 1, y = 2, z = 3)) 
    '''
    
    
    