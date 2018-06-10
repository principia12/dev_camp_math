from tree import *


def parse_car_data(data):
    pass
    
def divide_dataset(dataset, ratio, dev_set = False):
    pass
    
def train_tree(dataset):
    pass
    
def evaluate_tree(tree, dataset):
    pass
    
    
if __name__ == '__main__':
    dataset = parse_car_data()
    train, test = divide_dataset(dataset, ratio = (0.9, 0.1))
    
    tree = train_tree(train)
    
    precision = evaluate_tree(tree, test)
    print(precision)