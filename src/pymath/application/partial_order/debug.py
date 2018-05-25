import os
import sys
sys.path.append(os.path.join('..', '..'))

from PySet import *
from global_variables import *
from util import *


'''
Do topological sort on python files for debugging; 
'''
def dir2tree(root_dir):
    datum = root_dir
    children = []
    for elem in os.listdir(root_dir):
        elem = os.path.join(root_dir, elem)
        if os.path.isdir(elem):
            children.append(dir2tree(elem))
        else:
            children.append(Tree(elem))
    return Tree(datum, children)

def get_imported_files(path):
    res = []
    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip().split()
                if len(line) < 2:
                    pass
                elif line[0] == 'import':
                    res.append(line[1] + '.py')
                elif line[0] == 'from':
                    res.append(line[1] + '.py')
    except FileNotFoundError:
        pass
    return res
    
        
def construct_poset(root_dir):
    def cmp_file(l, r):
        l = os.path.join(root_dir, l)
        r = os.path.join(root_dir, r)
        cond1 = os.path.split(r)[-1] in get_imported_files(l) 
        cond2 = os.path.split(l)[-1] in get_imported_files(r) 
        
        if cond1:
            if not cond2:
                return False
            else:
                return None
        else:
            if not cond2:
                return None
            else:
                return True

    def file_generator():
        for l in os.listdir(root_dir): # for files in a root_dir, 
            if l.endswith('.py') and l != 'test.py' : # # for python file except test.py file 
                yield l
        yield 'os.py'
        yield 'sys.py'
        yield 'math.py'
        yield 'functools.py'
        yield 'copy.py'
    
    return PyPartiallyOrderedSet(file_generator, cmp_file)
    
    
def files2graph(root_dir):
    file_list = [] # list of tuple filepath
    file_dependency = [] # list of tuple (filepath, filepath)
    for l in os.listdir(root_dir): # for files in a root_dir, 
        if l.endswith('.py') and l != 'test.py' : # # for python file except test.py file 
            file_list.append(l)
            path = os.path.join(root_dir, l)
            for imported_file in get_imported_files(path):
                file_dependency.append((l, imported_file))
                
    for f, g in file_dependency:
        if g not in file_list:
            file_list.append(g)
        if f not in file_list:  
            file_list.append(f)
        if (g,f) in file_dependency:
            print(f,g)
            file_dependency.remove((g,f)) # to remove cycle
        
    return Graph(file_list, file_dependency,)
    
def resolve_pyfile_dependency(root_dir):
    g = files2graph(root_dir)
    
    for e in g.topological_sort():
        print(e)
    
        
def get_dependency(pyfile, method = 'dfs', result = 'list'):
    root_dir, file_name = os.path.split(pyfile)
    g = files2graph(root_dir)
    
    if method == 'dfs':
        if result == 'list':
            for e in g.dfs(file_name, to_tree = False):
                print(e)
        elif result == 'tree':
            print(g.dfs(file_name))
    elif method == 'bfs':
        if result == 'list':
            for e in g.bfs(file_name, to_tree = False):
                print(e)
        elif result == 'tree':
            print(g.bfs(file_name))
            
            
    
if __name__ == '__main__':
    root_dir = os.path.join('..', '..',)
    filename = 'PySet.py'
    
    poset = construct_poset(root_dir)
    for l in poset.topological_sort():
        print(l)
    '''    
    # for test
    for e in files2graph(root_dir).topological_sort():
        print(e)
    print('------------')
    
    get_dependency(os.path.join(root_dir, filename))
    
    print('------------')
    get_dependency(os.path.join(root_dir, filename), 
                        method = 'dfs', result = 'list')
    
    print('------------')
    get_dependency(os.path.join(root_dir, filename), 
                        method = 'dfs', result = 'tree')
    print('------------')
    '''
    