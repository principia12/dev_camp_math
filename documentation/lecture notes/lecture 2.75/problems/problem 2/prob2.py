import re
def prob2(dart_str):
    tries = []
    while dart_str != '':
        m = re.match(r"[0-9][0-9]?[SDT](\*|\#)?", dart_str)
        tries.append(m.group())
        dart_str = dart_str[m.end():]

    sco = []
    idx = 0
    for t in tries:
        m = re.match(r"[0-9][0-9]?", t)
        sco.append(int(m.group(), 10))
        oo = t[m.end():]
        for o in oo:
            if o == 'S':
                sco[idx] **= 1
            elif o == 'D':
                sco[idx] **= 2
            elif o == 'T':
                sco[idx] **= 3

            if o == '*':
                sco[idx] *= 2
                if idx > 0:
                    sco[idx - 1] *= 2

            if o == '#':
                sco[idx] *= -1
        idx += 1
    return sum(sco)

if __name__ == '__main__':
    assert prob2('1S2D*3T') == 37
    assert prob2('1D2S#10S') == 9
    assert prob2('1D2S0T') == 3
    assert prob2('1S*2T*3S') == 23
    assert prob2('1D#2S*3S') == 5
    assert prob2('1T2D3D#') == -4
    assert prob2('1D2S3T*') == 59
