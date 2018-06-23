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
        res = Tree(None, children = [])
        if cur_tree.datum[0] == 'op':
            
            if cur_tree.datum[1] in ['+', '-']:
                pass
            elif cur_tree.datum[1] == '*':
                pass
            elif cur_tree.datum[1] == '/':
                pass
            elif cur_tree.datum[1] == '^':
                pass
        elif cur_tree.datum[0] == 'func':
            pass
        elif cur_tree.datum[0] == 'num':
            pass
        elif cur_tree.datum[0] == 'var':
            pass
        
        return PyFormula(res)
        
def taylor_exansion(formula, a, n):
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
        print(differentiate(formula).tree)
        print(formula.tree)
        #print(differentiate(formula).tree)
        #print(formula.tree)
        #print('tree')
        #print(differentiate(formula).tree)
        print('==================')
        
