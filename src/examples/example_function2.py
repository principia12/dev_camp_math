def f(a = 0, *args, **kwargs):
    print("Received by f(a, *args, **kwargs)")
    print("=> f(a=%s, args=%s, kwargs=%s" % (a, args, kwargs))
    print("Calling g(10, 11, 12, *args, d = 13, e = 14, **kwargs)")
    g(10, 11, 12, *args, d = 13, e = 14, **kwargs)

def g(f, g = 0, *args, **kwargs):
    print("Received by g(f, g = 0, *args, **kwargs)")
    print("=> g(f=%s, g=%s, args=%s, kwargs=%s)" % (f, g, args, kwargs))

print("Calling f(1, 2, 3, 4, b = 5, c = 6)")
f(1, 2, 3, 4, b = 5, c = 6)
