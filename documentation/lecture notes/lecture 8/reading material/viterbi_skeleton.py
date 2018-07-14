import numpy as np

def argmax(lst):
    max_lst = max(lst)
    for idx, elem in enumerate(lst):
        if elem == max_lst:
            return idx, elem
            
def get_score(y, emission_scores,trans_scores, start_scores, end_scores):
    '''
    get y and return score of y
    '''
    N = len(y)
    
    score = 0.0
    score += start_scores[y[0]]
    for i in xrange(N-1):
        score += trans_scores[y[i]][y[i+1]]
        score += emission_scores[i][y[i]]
    score += emission_scores[N-1,y[N-1]]
    score += end_scores[y[N-1]]
    
    return score
    
    

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    '''Run the Viterbi algorithm.
    N - number of tokens (length of sentence)
    L - number of labels
    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array
    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is the size N array/seq of integers representing the best sequence.
    '''
    pass