#from global_variables import *



'''
Stack ADT
'''

class Stack:
    def __init__(self, *initial_data, datastructure = 'list'):
        self.data = list(initial_data)
        
    def is_empty(self):
        return len(self.data) == 0
        
    def push(self, *elem):
        self.data.extend(elem)
        
    def pop(self):
        assert not self.is_empty()
        head, tail = self.data[:-1], self.data[-1]
        self.data = head
        
        return tail
        
    def top(self):
        if self.is_empty():
            return None
        return self.data[-1]
        
    def size(self):
        return len(self.data)
        
    def __str__(self):
        res = 'Stack'
        for elem in self.data:
            res += ' %s'%str(elem)
        return res

'''
Queue ADT
'''

class Queue:
    def __init__(self, *initial_data, datastructure = 'list'):
        self.data = list(initial_data)
        
    def is_empty(self):
        return len(self.data) == 0
        
    def push(self, *elem):
        self.data.extend(elem)
        
    def pop(self):
        assert not self.is_empty()
        head, tail = self.data[0], self.data[1:]
        self.data = tail
        return head
    def __str__(self):
        res = 'Stack'
        for elem in self.data:
            res += ' %s'%str(elem)
        return res            

'''
Tree datastructure 
'''

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
        
'''
Graph datastructure 
'''

class Graph:
    def __init__(self, V, E, is_directed = True):
        for from_node, to_node in E:
            assert from_node in V, from_node
            assert to_node in V, to_node
            
        self.V = V
        self.E = E
        self.is_directed = is_directed 
        
        # adjacency list generation 
        adj_list = {}
        for v in V:
            adj_list[v] = []
            
        for from_node, to_node in E:
            if from_node == v:
                adj_list[v].append(to_node)
        self.adjacency_list = adj_list
        
        # adjacency matrix generation 
        adj_mat = []
        for i, u in enumerate(V):
            adj_mat.append([])
            for j, v in enumerate(V):
                if v in adj_list[u]:
                    adj_mat[-1].append(1)
                else:
                    adj_mat[-1].append(0)
        
        self.adjacency_matrix = adj_mat
        
    def is_dag(self):
        try:
            self.topological_sort()
            return True
        except AssertionError:
            return False
    
    def get_adj(self, node):
        res = []
        
        for v,u in self.E:
            if node == v:
                res.append(u)
            elif node == u and not self.is_directed:
                res.append(v)
                
        return res
    
    def _dfs_util(self, start_node, visited, to_tree = True):
        if not to_tree:
            res  = []
            if visited[start_node]:
                return []
            visited[start_node] = True
            res.append(start_node)
            # get adj of start_node
            for node in self.get_adj(start_node):
                res.extend(self._dfs_util(node, visited, to_tree = to_tree))
        else:
            if visited[start_node]:
                return Tree(datum = start_node)
            visited[start_node] = True
            datum = start_node
            children = []
            for node in self.get_adj(start_node):
                if not visited[node]:
                    children.append(self._dfs_util(node, visited, to_tree = to_tree))
                    
            res = Tree(datum = datum, children = children)
        
        return res
    
    def dfs(self, start_node, to_tree = True):
        assert start_node in self.V
        visited = {}
        for v in self.V:
            visited[v] = False
            
        return self._dfs_util(start_node, visited, to_tree = to_tree)
    
    def bfs(self, start_node, to_tree = True):
        if not to_tree:
            res, queue = [], [start_node]
            while queue:
                v = queue.pop()
                if v not in res:
                    res.append(v)
                    queue.extend(list(set(self.V) - set(res)))
            return res
        else:
            queue = [start_node]
            res = Tree(datum = start_node, children = [])
            
            while queue:
                v = queue.pop()
                visited = [t.datum for t in res.nodes()]
                if v not in visited:
                    queue.extend(list(set(self.V) - set(visited)))
                    
            return res
            
            
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
            print(res)
            assert False, 'Something Wrong! %s'%(edges)
            
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
    
def isnumber(x):
    return isinstance(x, (int, float, complex))
    
escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def str2raw(text):
    '''Returns a raw string representation of text'''
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string
    
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