def prob4(m, n, board):
    '''
    input parameter
    - m, n : 보드의 사이즈를 나타낸다.
    - board : 보드는 m개의 길이가 n인 문자열로 되어있다. 문자열은 A에서 Z까지가 사용된다. 
    
    output
    - 주어진 보드에서 사라질 블록의 갯수를 구하라. 빈 후 떨어진 블록에 대해서도 계산하여야 함을 명심히라.
    
    * 떨어짐 예시 
    TTTANT
    RRFACC
    RRRFCC
    TRRRAA
    TTMMMF
    TMMTTJ
    
    는 한번 없어진 후, 
    
    TTTANT
    --FA--
    ---F--
    T--RAA
    TTMMMF
    TMMTTJ
    
    가 되며, 이후 떨어지면 
    
    ---A--
    ---A--
    T-TFNT
    TTFRAA
    TTMMMF
    TMMTTJ
    
    가 된다. 
    '''
    pass
    
if __name__ == '__main__':
    assert prob4(4, 5, ['CCBDE', 'AAADE', 'AAABF', 'CCBBF']) == 14
    assert prob4(6, 6, ['TTTANT', 'RRFACC', 'RRRFCC', 'TRRRAA', 'TTMMMF', 'TMMTTJ']) ==	15