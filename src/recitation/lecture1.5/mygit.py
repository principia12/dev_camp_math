import os, sys, re
import pickle
from util import *
from global_variables import *

class Snapshot:
    def __init__(self, 
                    version = 0, # snapshot version no.
                    branch = 'master', # branch id 
                    root_dir = '.',): # root directory of git repository
        self.version = version 
        self.root_dir = root_dir
        self.branch = branch
        self.tracking_patterns = []
        self.status = dir2tree(root_dir)
    
    def read_cur_state(self):
        pass
        
    def save_cur_state(self):
        r = self.root_dir
        copy_directory_tree(r, os.path.join(r, GIT_DIR))
        # write change log as pickle on 
    
    def check_cur_state(self):
        untracked_log = '' # untracked files that are not added
        new_log = '' # added, and first to commit 
        modified_log = '' # already added, modified after last snapshot
        staged_log = '' # already added, and ready for next commit
        deleted_log = '' # deleted from last snapshot 
        
        ignore_list = parse_gitignore()
        new = dir2tree(self.root_dir, ignore = ignore_list)
        if self.version == 0:
            track_change(new)
        else:
            old = history2tree(self.version-1, ignore = [GIT_DIR, ])
            track_change(new, old)
        for n in new.leaves():
            print(n)
            
def git_clone(src, dest = '.'):
    pass
        
def git_init(root_dir):
    create_dir(os.path.join(root_dir, GIT_DIR))
    with open(os.path.join(root_dir, GIT_DIR, 'git_info'), 'w') as f:
        f.write('latestversion 0\ncurversion 0\n')
        
    with open(os.path.join(root_dir, GITIGNORE), 'w') as f:
        f.write('# first gitignore\n')
    create_dir(os.path.join(root_dir, HISTORY))
    
def parse_gitignore(path):
    res = [GIT_DIR]
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] == '#':
                pass
            else:
                res.append(line)
    return res
                
def parse_gitinfo(path)
    res = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            res[line[0]] = line[1]
    return res
    
    
def git_status(cur_state):
    pass
    
def git_remove(cur_state, *filenames):
    pass
    
def git_add(cur_state):
    pass
    
def git_commit(cur_state):
    pass
    
def git_push():
    pass
    
def git_pull():
    pass
    
def git_branch(cur_state):
    pass
    
def git_checkout(cur_state):
    pass
    
def git_history():
    pass
    
    
if __name__ == '__main__':
    print('start mygit bash') 
    prompt = '>>'
    history = Graph([], [])
    cur = Snapshot()
    while True:
        
        args = input(prompt)
        args = parse_args(args)
        
        func_list = ['init', 'status', 'add', 'commit', 'clone', 'branch', 'checkout','history', 'remove', 'removegit']
        
        opt = []
        func = ''
        para = []
        
        for arg in args:
            if arg[0] == '-':
                opt.append(arg)
            elif arg in func_list:
                func = arg
            else:
                para.append(func)
                
        if func == 'init':
            try:
                root_dir = para[0]
            except IndexError:
                root_dir = 'old' # for now, default 
            git_init(root_dir)
            cur = Snapshot(
        elif func == 'status':
            pass
        elif func == 'add':
            pass
        elif func == 'commit':
            pass
        elif func == 'clone':
            pass
        elif func == 'branch':
            pass
        elif func == 'checkout':
            pass
        elif func == 'history':
            pass
        elif func == 'remove':
            pass
        elif func == 'removegit':
            pass
         
          
       
        
        if args == ['quit'] or args == ['exit']:
            print('Bye!')
            break