from global_variables import *


'''
Tree datastructure 
'''
class Tree:
    def __init__(self, 
                 datum, 
                 children = [], 
                 _id = 0, 
                 _name = ''):    
        self.datum = datum 
        assert not isinstance(self.datum, Tree), '\n' + str(self.datum)
        '''
        for idx, child in enumerate(children):
            if isinstance(child, Tree):
                children[idx] = child
            else:
                children[idx] = Tree(child)
        '''
        self.children = children
        
    def __str__(self):
        res = str(self.datum)
        for child in self.children:
            res += '\n\t' + str(child).replace('\n', '\n\t')
        return res
            
    def nodes(self):
        yield self.datum
        for child in self.children:
            yield from child.nodes()
            
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
        
        
'''
Graph datastructure 
'''

class Graph:
    def __init__(self, V, E, is_directed = True):
        for from_node, to_node in E:
            assert from_node in V
            assert to_node in V, to_node
            
        self.V = V
        self.E = E
        
    def adjacency_list(self):
        res = {}
        for v in V:
            res[v] = [[],[]]
        for from_node, to_node in E:
            pass
        
    def adjacency_matrix(self):
        pass
        
    def have_cycle(self):
        pass
    
    def dfs(self):
        pass
     
    def bfs(self):
        pass
        
    def topological_sort(self):
        # implementation of Kahn's algorithm for topological sort 
        res = []
        starting_nodes = []
        to_nodes = [e[1] for e in self.E]
        edges = [e for e in self.E]
        
        for v in self.V:
            if v not in to_nodes:  
                starting_nodes.append(v)
        
        while len(starting_nodes) != 0:
            n = starting_nodes.pop()
            res.append(n)
            for e in self.E:
                if e[0] == n:
                    m = e[1]
                    edges.remove(e)
                    if m not in [e[1] for e in edges]:
                        starting_nodes.append(m)
            
        if edges != []:
            assert False, 'Something Wrong!' 
        else:
            return res
        
#-------------------------------------------------------
# Auxilliary Functions 
#-------------------------------------------------------

def binary2nary(func):
    def res_func(*lst):
        res = lst[0]
        for elem in lst[1:]:
            res = func(res, elem)
        return res
    return res_func
    
def generator2membership(generator):
    def membership(args):
        a = generator()
        i = 0
        while i<MAXIMUM_ITERATION:
            if args == next(a):
                return True
            i += 1
    return membership
    
if __name__ == '__main__':
    
    
    #-------------------------------------------------------
    # Datastructure test 
    #-------------------------------------------------------

    
    # Tree construction test 
    t1 = Tree(1)
    t2 = Tree(1, [Tree(2), Tree(3)])
    t3 = Tree(1, [Tree(1, [Tree(2), Tree(3)]), 
                  Tree(1),])
    t4 = Tree(1, [Tree(2, [Tree(3), Tree(4), Tree(5), ]), 
                  Tree(1, [Tree(1, [Tree(2), Tree(3)]), 
                           Tree(1),]),
                  Tree(1, [Tree(2), Tree(3)])])
    
    # __str__ test 
    print(t1, end='\n-----------\n')
    print(t2, end='\n-----------\n')
    print(t3, end='\n-----------\n')
    print(t4, end='\n-----------\n') 
    
    # append_leftmost test
    t2.append_leftmost(4)
    print(t2, end='\n-----------\n')
    t4.append_leftmost(10)
    print(t4, end='\n-----------\n')
    
    # get_subtree test
    print('==================')
    print(t4.get_subtree([0]))
    print(t4.get_subtree([0,1]))
    
    # path_to_subtree test
    print('==================')
    assert [] == t4.path_to_subtree(t4)
    assert [0] == t4.path_to_subtree(t4.get_subtree([0]))
    assert [0,1] == t4.path_to_subtree(t4.get_subtree([0,1]))
    
    # append_to_position test
    print('==================')
    t2.append_to_position(4, [2])
    print(t2)
    #t4.append_to_position(100, [1, 2])
    #print(t4)
    
    # nodes test
    print('==================')
    for elem in t2.nodes():
        print(elem)
        
    # append_to_subtree test
    print('==================')
    print(t4)
    #a = t4.get_subtree([0,1])
    #t4.append_to_subtree(100,a)
    
    t4.append_to_subtree(100, t4)
    print(t4)
    
    # copy test
    print('==================')
    print('copy test')
    print(t4)
    t5 = t4.copy()
    print(t5)
    
    #-------------------------------------------------------
    # Auxilliary Functions Test
    #-------------------------------------------------------
    
    # binary_to_nary_func test 
    print('==================')
    f = binary2nary(lambda x,y :x+y)
    print(f(1,2,3,4,5))