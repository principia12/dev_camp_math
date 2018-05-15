def mysort(lst): # insertion sort
    if len(lst) == 1:
        return lst
    else:
        head, tail = lst[0], lst[1:]
        tail = mysort(tail)
        for idx, elem in enumerate(tail):
            if head <= elem:
                return tail[:idx] + [head] + tail[idx:]
        return tail + [head]
        
assert mysort([2,1,3]) == [1,2,3]
