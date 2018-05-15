def compare(l, r): # (1) 
    return sum(l) >= sum(r)
    
def mysort(lst, cmp): # (2)
    if len(lst) == 1:
        return lst
    else:
        head, tail = lst[0], lst[1:]
        tail = mysort(tail)
        for idx, elem in enumerate(tail):
            if cmp(head, elem): # (3)
                return tail[:idx] + [head] + tail[idx:]

assert mysort([(1,2,3), (2,-4,2), (1,3,1)],
                cmp = compare) == [(1, 2, 3), (1, 3, 1), (2, -4, 2)] # (4)
