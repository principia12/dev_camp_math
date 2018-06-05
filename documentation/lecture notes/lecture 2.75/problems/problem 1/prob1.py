def prob1(map_size, arr1, arr2):
    '''
    input parameter
    - map_size : 지도의 크기. 지도는 map_size * map_size 배열이다. 
    - arr1, arr2 : map_size 크기의 정수 배열. 
    
    output
    - 비밀지도를 해독하여, # 및 공백으로 구성된 배열을 출력하라. 
    '''
    mask = 2**map_size - 1
    return ['{0:032b}'.format((a|b)&mask)[-map_size:].replace('0', ' ').replace('1','#') for a,b in zip(arr1, arr2)]
    
    
if __name__ == '__main__':
    assert prob1(5, [9, 20, 28, 18, 11], [30, 1, 21, 17, 28]) == \
                    ['#####', '# # #', '### #', '#  ##', '#####']
    assert prob1(6, [46, 33, 33, 22, 31, 50], [27, 56, 19, 14, 14, 10]) == \
                    ["######", "###  #", "##  ##", " #### ", " #####", "### # "]
