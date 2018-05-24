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
                  is_partial = True, 
                  is_symbolic = True, 
                  debug = False):
    if not isinstance(formula, PyFormula):
        formula = PyFormula(formula)
    args = [variable, constant_variables, is_partial, is_symbolic]
    cur_tree = formula.tree.copy()
    if debug:
        print(cur_tree)
    if is_symbolic:
        # below two line behaves differently. why????
        # res = Tree(None)
        res = Tree(None, children = [])
        if cur_tree.datum[0] == 'op':
            
            if cur_tree.datum[1] in ['+', '-']:
                res.datum = cur_tree.datum
                for child in cur_tree.children:
                    res.children.append(differentiate(child, *args).tree.copy())
            if cur_tree.datum[1] == '*':
                res.datum = ('op', '+')
                diff_children = [differentiate(c, *args).tree.copy() \
                                        for c in cur_tree.children]
                
                for i in range(len(cur_tree.children)):
                    tmp_children = []
                    for j in range(len(cur_tree.children)):
                        if i == j:
                            tmp_children.append(diff_children[j].copy())
                        else:
                            tmp_children.append(cur_tree.children[j].copy())
                    
                    res.children.append(Tree(('op', '*'), tmp_children))
                
            if cur_tree.datum[1] == '/':
                # for simplicity, assume binary 
                f,g = cur_tree.children
                df = differentiate(f, *args).tree
                dg = differentiate(g, *args).tree
                
                res =\
                Tree(('op', '/'), 
                        [ Tree(('op', '-'), 
                                    [Tree(('op', '*'), [df, g]),
                                     Tree(('op', '*'), [f, dg])]), 
                         Tree(('op', '^'), 
                                 [g, Tree(('num', '2'))])])
                
            if cur_tree.datum[1] == '^':
                # for simplicity, assume binary
                f,g = cur_tree.children
                df = differentiate(f, *args).tree
                dg = differentiate(g, *args).tree
                res =\
                Tree(('op', '*'), 
                        [cur_tree, 
                         Tree(('op', '+'), 
                                 [Tree(('op', '*'), 
                                          [dg, 
                                           Tree(('func', 'ln'), [f])]),
                                  Tree(('op', '/'),
                                          [Tree(('op', '*'), [g,df]),
                                           f,])])])
                
        elif cur_tree.datum[0] == 'func':
            pass
        elif cur_tree.datum[0] == 'num':
            return PyFormula('0')
        elif cur_tree.datum[0] == 'var':
            if cur_tree.datum[1] == variable:
                return PyFormula('1')
            elif cur_tree.datum[1] in constant_variables:
                return PyFormula('0')
            else:
                return PyFormula('%s`'%tree.datum[1])
        
        return PyFormula(res)
        
    
def integral(formula, 
             variable, 
             is_symbolic = True):
    pass
    
if __name__ == '__main__':
    formula1 = 'x+1'
    formula2 = 'x^2'
    formula3 = '3*x'
    formula4 = 'x/2'
    
    for i in range(100):
        try:
            eq = eval('formula%d'%i)
            formula = PyFormula(eq)
        except NameError:
            continue
            
        print('==================')
        print('formula')
        #print(formula.tree)
        #print(differentiate(formula))
        print(differentiate(formula))
        #print(differentiate(formula).tree)
        #print(formula.tree)
        #print(differentiate(formula).tree)
        #print(formula.tree)
        #print('tree')
        #print(differentiate(formula).tree)
        print('==================')
        assert i<4
