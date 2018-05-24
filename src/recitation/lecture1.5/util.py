import os, sys, re
import shutil
import pickle
from global_variables import *


def create_dir(path_to_dir):    
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)
        
def copy_directory(src, dest):
    pass
    
def compare_file(src, dest):
    '''
    if same, return True 
    else, return False
    '''
    with open(src, 'r') as f, open(dest, 'r') as g:
        return f.read() == g.read()
        
def track_change(new, old):
    from copy import copy
    old_root = copy(old.datum)
    for n in old.nodes():
        n.datum = os.path.join(new.datum, *n.datum.split(os.sep)[1:])
    record_change(new, old, old_root)
    
    
def record_change(new, old = None, old_root = None):
    from copy import deepcopy
    if old is None:
        for leaf in new.leaves():
            leaf.datum = ('untracked', leaf.datum)
    else:
        if new.children == [] and old.children == []:   
            old.datum = os.path.join(old_root, *old.datum.split(os.sep)[1:])
            if compare_file(new.datum, old.datum):
                new.datum = ('unmodified', new.datum)
            else:
                new.datum = ('modified', new.datum)
        copy_new = deepcopy(new.children)
        for child in new.children:
            if child.datum not in [c.datum for c in old.children]:
                record_change(child)
            else:
                old_child = \
                list(filter(lambda x:x.datum == child.datum, old.children, ))[0]
                
                record_change(child, old_child, old_root = old_root)
        for old_child in old.children:
            if old_child.datum not in [c.datum for c in copy_new]:
                old_child.datum = ('deleted', old_child.datum)
                new.children.append(old_child)

def history2tree(ver, ignore = [GIT_DIR, GITIGNORE]):
    return dir2tree(os.path.join(HISTORY, str(ver)), ignore = ignore)
    
def dir2tree(root_dir, ignore = [GIT_DIR, GITIGNORE]):
    datum = root_dir
    children = []
    for elem in os.listdir(root_dir):
        for ig in ignore:
            if re.match(ig, elem):
                continue
        elem = os.path.join(root_dir, elem)
        if os.path.isdir(elem):
            children.append(dir2tree(elem))
        else:
            children.append(Tree(elem))
    return Tree(datum, children)

    
def parse_args(args):
    return args.split()
    
# Auxillary data structure
class Graph:
    '''
    Will be used as a graph with vertices containing snapshots
    '''
    def __init__(self, V, E):
        self.V = V
        self.E = E
        
class Tree:
    '''
    Will be used as a directory wrapper
    '''
    def __init__(self, 
                 datum, 
                 children = [], 
                 _id = 0, 
                 _name = ''):    
        self.datum = datum 
        assert not isinstance(self.datum, Tree), '\n' + str(self.datum)
        
        for idx, child in enumerate(children):
            if isinstance(child, Tree):
                children[idx] = child
            else:
                children[idx] = Tree(child)
        
        self.children = children
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.datum == other.datum:
                if self.children == other.children == []:
                    return True
                return set(self.children) == set(other.children)
            return False
        return NotImplemented
    
    def __ne__(self, other):
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemente
    
    def __str__(self):
        res = str(self.datum)
        for child in self.children:
            res += '\n\t' + str(child).replace('\n', '\n\t')
        return res
            
    def nodes(self):
        yield self
        for child in self.children:
            yield from child.nodes()
            
    def leaves(self):
        if self.children == []:
            yield self
        else:
            for child in self.children:
                yield from child.leaves()
            
    def append_leftmost(self, elem):
        ''' Append Tree(elem) to the leftmost non-leaf node. 
        If root node is only non-leaf node in the tree, just append to children of root. 
        
        Return the position where elem is appended. 
        '''
        if not isinstance(elem, Tree):
            elem = Tree(elem)
        
        if self.children == []:
            self.children.append(elem)
            return [0]
        elif self.children[-1].children == []:
            self.children.append(elem)
            return [-1]
        else:
            return [-1] + self.children[-1].append_leftmost(elem)
            
    def get_subtree(self, path_to_root):
        '''Get subtree given the path to the root of the subtree. 
        '''
        res = self
        for p in path_to_root:
            res = res.children[p]
        return res
        
    def path_to_subtree(self, sub):
        '''Get path to subtree. If sub is not a subtree of path_to_subtree, 
        return False. 
        '''
        if self == sub:
            return []
        else:
            for idx, child in enumerate(self.children):
                p = child.path_to_subtree(sub)
                if p != -1:
                    return [idx] + p
        return -1
        
    def append_to_position(self, elem, path_to_pos):
        if not isinstance(elem, Tree):
            elem = Tree(elem)
        assert path_to_pos != [], 'Make new tree.'
        
        # python insert on negative index does not work as desired! 
        #self.get_subtree(path_to_pos[:-1]).children.insert(path_to_pos[-1], elem)
        idx = path_to_pos[-1]
        sub = self.get_subtree(path_to_pos[:-1])
        
        if idx < 0:
            idx = len(sub.children) + idx + 1
        
        sub.children = sub.children[:idx] + [elem] + sub.children[idx:]
        
    def append_to_subtree(self, elem, sub):
        if not isinstance(elem, Tree):
            elem = Tree(elem)
        if sub.children == []:
            sub.children = [elem]
        else:
            sub.children.append(elem) # why does error occur when leaf? 
        
    def copy(self):
        from copy import deepcopy 
        return deepcopy(self)
        
if __name__ == '__main__':
    old = dir2tree('old')
    
    # modify old file 
    shutil.rmtree('old')
    os.rename('new', 'old')
    
    new = dir2tree('old')
    
    #record_change(new)
    print(new)
    print(old)
    track_change(new, old)
    print(new)