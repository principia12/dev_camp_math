import os
import sys
sys.path.append(os.path.join('..', '..'))

from PySet import *
from PyTensor import *
from global_variables import *
from util import *

def make_matrix(file_path):
    with open(file_path, 'r') as f:
        x_col = []
        y_col = []
        col = []
        for l in f.readlines():
            try:
                x,y = l.strip().split(',')
            except ValueError:
                pass
            if x == 'x':
                pass
            else:
                x_col.append(float(x))
                y_col.append(float(y))
                col.append(1.0)
        X = PyMatrix(PyVector(*x_col), PyVector(*col))
        Y = PyVector(*y_col)
        return X, Y
        
if __name__ == '__main__':
    X, Y = make_matrix('data/train.csv')
    print(PyMatrix.LLS(X,Y))

 