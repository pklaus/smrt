#!/usr/bin/env python3

SEP = ","

def ports2byte(numports):
    out = 0
    for i in numports.split(SEP):
        out |= (1 << (int(i) - 1))
    return out

def byte2ports(byte):
    out = []
    for i in range(32):
        if byte % 2:
            out.append(str(i + 1))
        byte = (byte >> 1)
    return SEP.join(out)

if __name__ == '__main__':
    #print(ports2byte("12345678"))
    a = ports2byte("1:2:5:6:8:12:15")
    print(a, byte2ports(a))
