'''
Problem 1 : Look-and-say sequence
In this problem, you are asked to write a function look_and_say for computing nth element of look-and-say sequence. 
For the definition of look-and-say sequence, consult wikipedia(https://en.wikipedia.org/wiki/Look-and-say_sequence)
Two inputs will be given: n and first_element. 
- n : Natural number for the output. 
      Output of this function should be nth element of look-and-say sequence, given first element of the sequence. 
- first_element : String for the first element of look-and-say sequence. 
                  Note that look-and-say sequence can have any starting element; for example, 22.
                  Also, since this is the first element, look_and_say(1, first_element) == first_element. 
Output of this function should be nth element of look-and-say sequence, given the first element as a parameter first_element.
'''

def advance(elem):
    '''
    Return next element for look-and-say sequence. 
    '''
    cur_char = elem[0]
    res = [[cur_char, 0]]
    for char in elem:
        if char == cur_char:
            res[-1][1] += 1
        else:
            res.append([char, 1])
            cur_char = char
    
    # if you are not familiar with map or lambda, following line would be easier
    # return ''.join([str(e[1]) + e[0] for e in res])
    # if you are familiar with map or lambda,
    return ''.join(map(lambda e:str(e[1]) + e[0], res))

def look_and_say(n, first_element):
    elem = first_element
    for i in range(n-1): # compute next element for n-1 times 
        elem = advance(elem) 
    return elem
    
assert(look_and_say(1, '12321') == '12321')
assert(look_and_say(10000, '22') == '22')
assert(look_and_say(5, '1') == '111221')

'''
Problem 2 : Tower of Hanoi 
In this problem, you are asked to write a function hanoi_tower that prints how disks are moved in Tower of Hanoi problem. 
The output of this function should look like below; 
disk 1 moved from A to B
dist 2 moved from A to C
.... 
For definition of Tower of Hanoi problem, consult wikipedia(https://en.wikipedia.org/wiki/Tower_of_Hanoi)
In this problem, we will only consider the case of three rods(A, B, C), and disks are originally in the rod A. 
After a sequence of movement, all disks will be located in the rod C. 
A disk with larger number is wider than the disks with smaller number. 
For instance, disk 2 is larger than disk 1, but smaller than disk 3. 
One input will be givne: n. 
- n : number of disks 
Output should be string that explains how the disks are moved. 
Each movement of a disk should be in a seperate line, without any trailing spaces. (You can simply use strip(), and return)
'''

def move_string(from_rod, to_rod, disk_num):
    ''' Auxillary function for printing a single movement of disk from from_rod to to_rod. 
    '''
    return 'disk %d moved from %s to %s'%(disk_num, from_rod, to_rod)
    
def hanoi(from_rod, pass_rod, to_rod, disk_num):
    ''' Main function of the program. 
    Move disks 1 ~ disk_num from from_rod to to_rod, using pass_rod. 
    
    This is done as following; 
    - move 1 ~ disk_num-1
    '''
    if disk_num == 1:
        return move_string(from_rod, to_rod, 1)
    else:
        return hanoi(from_rod, to_rod, pass_rod, disk_num-1) + '\n' \
            + move_string(from_rod, to_rod, disk_num) + '\n' \
            + hanoi(pass_rod, from_rod, to_rod, disk_num-1)
            

def hanoi_tower(n):
    return hanoi('A', 'B', 'C', n)

assert(hanoi_tower(1) == 'disk 1 moved from A to C')
hanoi_2 = '''disk 1 moved from A to B
disk 2 moved from A to C
disk 1 moved from B to C'''
assert(hanoi_tower(2).strip() ==  hanoi_2)
