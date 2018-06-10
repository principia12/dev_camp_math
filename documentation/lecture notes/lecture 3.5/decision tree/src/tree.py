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
            
    def leaves(self):
        if self.children == []:
            yield self 
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
   