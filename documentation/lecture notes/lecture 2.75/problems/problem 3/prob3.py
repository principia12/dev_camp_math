def prob3(text):
    import heapq
    from collections import defaultdict
    def build_table(text):
        freq = defaultdict(int)
        for c in text:
            freq[c] += 1

        heap = [[v, [k, '']] for k, v in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for code in lo[1:]:
                code[1] = '0' + code[1]
            for code in hi[1:]:
                code[1] = '1' + code[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        enc_table = {}
        dec_table = {}

        for code in heap[0][1:]:
            enc_table[code[0]] = code[1]
            dec_table[code[1]] = code[0]

        return enc_table, dec_table


    def encode(text, table):
        return ''.join([table[x] for x in text])

    def decode(text, table):
        out = ''
        code = ''
        for c in text:
            code += c
            if code in table:
                out += table[code]
                code = ''
        return out

    print("ORG: ", len(text)*8, text)
    et, dt = build_table(text)
    enc = encode(text, et)
    print("ENC: ", len(enc), enc)
    print("compress ratio : %3.3f%%" % ((len(enc)/(len(text)*8))*100))
    dec = decode(enc, dt)
    print("DEC: ", len(dec)*8, dec)

if __name__ == '__main__':
    text1 = '''skjfkdsjfldjslf'''
    text2 = '''hello world'''
    prob3(text1)
    prob3(text2)
