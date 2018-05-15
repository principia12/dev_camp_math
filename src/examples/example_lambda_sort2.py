def mysort(lst): # insertion sort
    if len(lst) == 1:
        return lst
    else:
        head, tail = lst[0], lst[1:]
        tail = mysort(tail)
        for idx, elem in enumerate(tail):
            if sum(head) >= sum(elem):
                return tail[:idx] + [head] + tail[idx:]
assert mysort([(1,2,3), (2,-4,2), (1,3,1)]) == [(1, 2, 3), (1, 3, 1), (2, -4, 2)]
