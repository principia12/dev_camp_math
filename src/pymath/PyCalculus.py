from PyFormula import *
from global_variables import *
from util import *
from copy import deepcopy

def limit(formula, 
          is_symbolic = True,):
    pass

def differentiate(formula, 
                  variable = 'x', 
                  constant_variables = ['n'],
                  is_partial = False, 
                  is_symbolic = True, 
                  point = 0, 
                  delta = 0.001,
                  debug = False):
    if not isinstance(formula, PyFormula):
        #assert False, 'Should be PyFormula, now %s'%(str(formula)  + str(type(formula)))
        try:
            formula = PyFormula(formula)
        except:
            assert False, 'Pyformula Creation Failed : %s'%str(formula)
    args = [variable, constant_variables, is_partial, is_symbolic, debug]
    cur_tree = formula.tree.copy()
    if debug:
        print(cur_tree)
    if is_symbolic:
        res = Tree(None, children = [])
        if cur_tree.datum[0] == 'op':
            if cur_tree.datum[1] in ['+', '-']:
                res.datum = cur_tree.datum
                children = []
                for child in cur_tree.children:
                    children.append(differentiate(child, *args).tree)
                res.children = children
            elif cur_tree.datum[1] == '*':
                '''
                (f1*f2*...*fn)' = f1'*f2*f3*...*fn +
                                  f1*f2'*f3*...*fn + 
                                  ...
                                  f1*f2*f3*...*fn'
                '''
                res.datum = ('op', '+')
                children = []
                for i in range(len(cur_tree.children)):
                    tmp_children = []
                    for j, child in enumerate(cur_tree.children):
                        if i == j:
                            tmp_children.append(differentiate(child, *args).tree)
                        else:
                            tmp_children.append(child)
                    children.append(Tree(('op', '*'), tmp_children))
                res.children = children            
            elif cur_tree.datum[1] == '/':
                '''
                (f1/f2/f3/.../fn) = (f1*f3*...)/(f2*f4*...)
                (f/g)' = (f'g-g'f)/g^2
                '''
                top_children = []
                bottom_children = []
                for idx, child in enumerate(cur_tree.children):
                    if idx%2==0:
                        top_children.append(child)
                    else:
                        bottom_children.append(child)
                
                top = PyFormula(Tree(('op', '*'), top_children))
                bottom = PyFormula(Tree(('op', '*'), bottom_children))
                top_diff = differentiate(top, *args) 
                bottom_diff = differentiate(bottom, *args) 
                
                res = Tree(('op', '/'), children = [\
                    Tree(('op', '-'), [\
                        Tree(('op', '*'), [\
                            top_diff.tree, 
                            bottom.tree]), 
                        Tree(('op', '*'), [\
                            top.tree, 
                            bottom_diff.tree]),]),
                    Tree(('op', '^'), [\
                        bottom.tree, 
                        Tree(('num', '2'))])])
                        
                        
                
            elif cur_tree.datum[1] == '^':
                if len(cur_tree.children) != 2:
                    f = cur_tree.children[-1]
                    g = Tree(('op', '^'), [cur_tree.children[:-1]])
                    return differentiate(Tree(('op', '^'), [g,f]), *args)
                f = PyFormula(cur_tree.children[0])
                g = PyFormula(cur_tree.children[1])
                f_diff = differentiate(f, *args)
                g_diff = differentiate(g, *args)
                
                # (f^g)' = f^g ( g' ln f + gf'/f )
                res = Tree(('op', '*'), [\
                    Tree(('op', '^'), [f.tree ,g.tree ]), 
                    Tree(('op', '+'), [\
                        Tree(('op', '*'), [\
                            g_diff.tree , 
                            Tree(('func', 'ln'), [f.tree ]),]), 
                        Tree(('op', '/'), [\
                            Tree(('op', '*'), [\
                                g.tree , 
                                f_diff.tree , ],), 
                            f.tree ,])])])
                            
                
                
        elif cur_tree.datum[0] == 'func':
            func, diff_func, diff_formula = \
                    FUNCTION_DICT[cur_tree.datum[1]]
            if is_partial:
                return PyFormula(diff_formula).substitute(\
                        ('var', 'placeholder'), 
                        cur_tree.children[0])
            else:
                # (f(g(x)))' = f'(g(x)) g'(x)
                # (f(g(x,y)))' = f'(g(x,y))g'(x,y)
                
                children = []
                if len(formula.variables.elements) == 1:
                    arg = formula.variables.elements[0]
                    df = differentiate(formula, 
                                    variable = arg, 
                                    is_partial = True, )
                    darg = differentiate(cur_tree.children[0], *args)
                    res = Tree(('op', '*'), \
                            [df.tree, darg.tree])
                else:
                    for arg in formula.variables.elements:
                        df = differentiate(formula, 
                                    variable = arg, 
                                    is_partial = True, )
                        darg = differentiate(arg, *args)
                        children.append(Tree(('op', '*'), \
                            [df.tree, darg.tree]))
                    res = Tree(('op', '+'), children = children)
                
        elif cur_tree.datum[0] == 'num':
            res = Tree(('num', '0'))
        elif cur_tree.datum[0] == 'var':
            if is_partial:
                if cur_tree.datum[1] == variable:
                    res = Tree(('num', '1'))
                else:
                    res = Tree(('num', '0'))
            else:
                if cur_tree.datum[1] == variable:
                    res = Tree(('num', '1'))
                elif cur_tree.daum[1] in constant_variables:
                    res = Tree(('num', '0'))
                else:
                    # var token now carries additional argument for differentiation 
                    # if not differentiated before
                    if len(cur_tree.datum) == 2:
                        res = Tree(datum = (cur_tree.datum[0], 
                                            cur_tree.datum[1], 
                                            [variable] ))
                    elif len(cur_tree.datum) == 3:
                        datum = [e for e in cur_tree.datum]
                        datum[2].append(variable)
                        res = Tree(datum = datum)
        
        return PyFormula(res)
    elif is_symbolic == False:
        src = {variable : point}
        dest = {variable : point + delta}
        return (formula(**dest) - formula(**src))/delta
        
        
def diff(target, variable):
    if isinstance(target, Pyformula):
        if isinstance(variable, PyFormula):
            pass
        elif isinstance(variable, PyVector):
            pass
        elif isinstance(variable, PyMatrix):
            pass
        else:
            assert False, 'variable %s should be one of PyFormula, PyVector, or PyMatrix. Now %s'%(str(variable), type(variable))
    elif isinstance(target, PyVector):  
        if isinstance(variable, PyFormula):
            pass
        elif isinstance(variable, PyVector):
            pass
        else:        
            assert False, 'variable %s should be one of PyFormula or PyVector. Now %s'%(str(variable), type(variable))
    elif isinstance(target, PyMatrix):
        if isinstance(variable, PyFormula):
            pass
        else:
            assert False, 'variable %s should be PyFormula. Now %s'%(str(variable), type(variable)) 
    else:
        assert False, 'target %s should be one of PyFormula, PyVector, or PyMatrix. Now %s'%(str(target), type(target))
    

    
        
def taylor_expansion(formula, a, n):
    pass
    
def integral(formula, 
             variable, 
             is_symbolic = True):
    pass
    
if __name__ == '__main__':
    formula1 = 'x+1'
    formula2 = 'x^2'
    formula3 = '3*x'
    formula4 = 'x/2'
    formula5 = 'x^x'
    formula6 = 'sin(x)'
    formula7 = 'cos(x^2)'
    
    
    
    for i in range(100):
        try:
            eq = eval('formula%d'%i)
            formula = PyFormula(eq)
        except NameError:
            continue
            
        print('==================')
        #print('formula')
        print(formula.tree)
        #print(differentiate(formula))
        #print(differentiate(formula))
        print(differentiate(formula).tree)
        #print(formula.tree)
        #print(differentiate(formula).tree)
        #print(formula.tree)
        #print('tree')
        #print(differentiate(formula).tree)
        print('==================')
    '''    
    for key in FUNCTION_DICT.keys():
        print(PyFormula(FUNCTION_DICT[key][2]).substitute(('var', 'placeholder'), PyFormula('x').tree).tree)
    '''    
