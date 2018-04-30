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

def look_and_say(n, first_element):
    pass

assert(look_and_say(1, '12321') == '12321')
assert(look_and_say(10000, '22') == '22')
assert(look_and_say(5, '1') == '111221')
# make more test cases on your own! 

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

def hanoi_tower(n):
    pass

assert(hanoi_tower(1) == 'disk 1 moved from A to C')
hanoi_2 = '''disk 1 moved from A to B
disk 2 moved from A to C
disk 1 moved from B to C'''
assert(hanoi_tower(2).strip() ==  hanoi_2)


