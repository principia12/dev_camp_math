from tree import *
from random import *
from math import log 

# dataset from https://archive.ics.uci.edu/ml/datasets/Car+Evaluation

def max_index(lst, key = lambda x:x):
    if lst == []:
        return None
    return lst.index(max(lst, key = key))

def get_label(lst, label_index = -1):
    # get most frequent label and return it. 
    res_dict = {}
    for elem in lst:
        if elem[0] in res_dict.keys():
            res_dict[elem[label_index]] += 1
        else:
            res_dict[elem[label_index]] = 1
    
    lst = [(k, res_dict[k]) for k in res_dict.keys()]
    lst.sort(key = lambda x:x[1])
    return lst[-1][1]
    
def entropy(lst):
    p_1 = lst[0]/sum(lst)
    p_2 = lst[1]/sum(lst)
    if p_1 == 0 or p_2 == 0:
        return 0
    try:
        return -(p_1*log(p_1) + p_2*log(p_2))
    except ValueError:
        print(p_1, p_2)

def decide_threshold(dataset, column_idx, label_index = -1):
    assert len(dataset)!=0
    
    if len(dataset) == 1:
        return dataset
    # need to be generalized - label is the first elem of data
    label = [e[label_index] for e in dataset]     
    col = [e[column_idx] for e in dataset]
    data = list(zip(label, col, dataset))
    data.sort(key = lambda x:x[1])
    
    lst = []
    
    m_count = label.count(1.0) # need to be generalized
    f_count = label.count(2.0) # need to be generalized
    size = len(data)
    front_accum = [0,0]
    back_accum = [m_count, f_count]
    p_m, p_f = m_count/size, f_count/size
    initial_entropy = entropy(back_accum)
    
    for idx, elem in enumerate(data):   
        i = idx + 1
        
        if elem[0] == 1.0:
            front_accum[0] += 1
            back_accum[0] -= 1            
        else:
            front_accum[1] += 1
            back_accum[1] -= 1
        if i != len(data):
            # append idx and information gain. 
            lst.append(i * entropy(front_accum)/len(data)\
                        + (size-i) * entropy(back_accum)/len(data) \
                        - initial_entropy)
    
    # max information gain 
    #assert size-1 == len(lst)
    
    max_idx = max_index(lst)
    # return threshold
    assert lst!=[], dataset
    assert len(dataset) == len([e[2] for e in data[max_idx:]]) + \
                            len([e[2] for e in data[:max_idx]])
    # back have bigger values
    return data[max_idx][1], \
            [e[2] for e in data[max_idx:]], \
            [e[2] for e in data[:max_idx]]
    
    
    
    
def train_tree(dataset, col_idx = 1):
    ''' Given a dataset, train the tree with the dataset. 
    '''

    #print('train tree %d, %d'%(col_idx, len(dataset)))
    if col_idx == len(dataset[0])-1:
        return Tree(datum = ('leaf', get_label(dataset)))
    if len(dataset) == 1:
        return Tree(datum = ('leaf', get_label(dataset)))
    threshold, front_data, back_data = decide_threshold(dataset, col_idx)
    assert len(dataset) == len(front_data) + len(back_data), col_idx
    if len(front_data) == 0:
        return Tree(datum = (col_idx, threshold), \
                children = [train_tree(back_data, col_idx +1), ])
    elif len(back_data) == 0:
        return Tree(datum = (col_idx, threshold), \
                children = [train_tree(front_data, col_idx +1)])
    else:
        return Tree(datum = (col_idx, threshold), \
                children = [train_tree(front_data, col_idx +1), \
                           train_tree(back_data, col_idx +1), ]) 
    

    
def classify(tree, datum):
    cur_pos = tree
    idx = 1
    while len(cur_pos.children) == 0:
        elem = datum[idx]
        if elem >= cur_pos.datum[1]:
            cur_pos = cur_pos.children[-1]
        else:
            cur_pos = cur_pos.children[0]
        idx += 1
    
    return cur_pos.datum[1]
    
def evaluate_tree(tree, dataset, label_index = -1):
    ''' Perform decision tree classification. 
    '''
    right, wrong = 0, 0
    for datum in dataset:
        if classify(tree, datum) == datum[label_index]:
            right += 1
        else:
            wrong += 1
    return right/(right+wrong)
            
def divide_dataset(dataset, ratio = (0.9,0.1), dev_set = False):
    ''' Divide dataset to training set and test set according to the given ratio.  
    If dev_set is True, divide dataset to training set/development set/test set. 
    '''
    assert sum(ratio) == 1
    if dev_set:
        assert len(ratio) == 3
        train, dev, test = \
            dataset[:int(len(dataset)*ratio[0])], \
            dataset[int(len(dataset)*ratio[1]):int(len(dataset)*ratio[2])], \
            dataset[int(len(dataset)*ratio[2]):],
            
        return train, dev, test
    else:
        assert len(ratio) == 2
        train, test = \
            dataset[:int(len(dataset)*ratio[0])], \
            dataset[int(len(dataset)*ratio[0]):],
        return train, test
 
def parse_car_data(data = '../data/car.data'):
    # class attribute
    evaluation = {'unacc' : 1.0, 'acc' : 1.0, 'good' : 2.0, 'vgood' : 2.0}

    # non-class attributes
    buying = {'vhigh' : 1.0, 'high' : 2.0, 'med' : 3.0, 'low' : 4.0}
    maint = {'vhigh' : 1.0, 'high' : 2.0, 'med' : 3.0, 'low' : 4.0}
    doors = {'2' : 1.0, '3' : 2.0, '4' : 3.0, '5more' : 4.0}
    persons = {'2' : 1.0, '4' : 2.0, 'more' : 3.0}
    lug_boot = {'small' : 1.0, 'med' : 2.0, 'big' : 3.0}
    safety = {'low' : 1.0, 'med' : 2.0, 'high' : 3.0}
    
    attr_dict = [buying, maint, doors, persons, lug_boot, safety, evaluation]
    
    res = []
    # same as f = open(data, 'r')
    with open(data, 'r') as f:
        for line in f.readlines():
                line = line.strip().split(',')
                datum = []
                for idx, elem in enumerate(line):
                    datum.append(attr_dict[idx][elem])
                res.append(datum)
    return res

if __name__ == '__main__':
    dataset = parse_car_data()
    
    train, test = divide_dataset(dataset, ratio = (0.8, 0.2))
    
    tree = train_tree(train)
    
    precision = evaluate_tree(tree, test)
    print(precision)
    
    