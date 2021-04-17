#!/usr/bin/env python3

SEP = ","

def ports2list(ports):
    if ports is None:
        l = []
    else:
        try:
            l = [int(x) for x in ports.split(SEP)]
        except ValueError:
            l = []
    return l

def ports2byte(ports):
    out = 0
    l = ports2list(ports)
    if l == []:
        out = 0
    else:
        for i in l:
            out |= (1 << (int(i) - 1))
    return out

def byte2ports(byte):
    out = []
    for i in range(32):
        if byte % 2:
            out.append(str(i + 1))
        byte >>= 1
    return SEP.join(out)

def mac_to_bytes(mac):
    return bytes(int(byte, 16) for byte in mac.split(':'))

def mac_to_str(mac):
    return ':'.join(format(s, '02x') for s in mac)


if __name__ == '__main__':
    a = ports2byte("1,2,5,6,8,12,15")
    print(a, byte2ports(a))
    print(ports2list("1,2"))
    m = mac_to_bytes("ba:ff:ee:ff:ac:ee")
    print(mac_to_str(m))
