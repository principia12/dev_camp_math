import os

def file_explorer(src_dir, extension = ''):
    pass
    
def folder_explorer(src_dir):
    pass
    
if __name__ == '__main__':
    file_explorer('..', extension = 'py')
    folder_explorer(os.path.join('..', '..'))