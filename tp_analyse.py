#!/usr/bin/env python

import socket, time, random, argparse, logging
from protocol import Protocol

def main():
    with open("tp_analyse.txt") as f:
        first = True
        ret = []
        for l in f:
            try:
                adr = int(l[:4], 16)
            except ValueError:
                continue
            if adr == 0:
                if not first:
                    ret.append(data)
                first = False
                data = bytearray()
            if adr % 16 == 0:
                #print(adr, bytearray.fromhex(l[6:53].split(" ")))
                data += bytearray.fromhex(l[6:53])
        ret.append(data)

        for s in ret:
            data = Protocol.decode(s)
            print(data.hex(" "))
            print(Protocol.analyze(data))


if __name__ == '__main__':
    main()

