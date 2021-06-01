#!/usr/bin/env python

import random
import logging
import argparse

from protocol import Protocol
from network import Network, ConnectionProblem, InterfaceProblem
from loglevel import loglevel

logger = logging.getLogger(__name__)

def discover_switches(interface=None):
    net = Network(interface)
    net.send(Protocol.DISCOVERY, {})
    ret = []
    while True:
        try:
            header, payload = net.receive()
            ret.append((ip, mac, header, payload))
        except ConnectionProblem:
            break
    return ret

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i')
    parser.add_argument('--command', '-c', action="store_true")
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    try:
        switches = discover_switches(args.interface)
    except InterfaceProblem as e:
        print("Error:", e)
    else:
        for ip, mac, header, payload in switches:
            if args.command:
                p = {x[1]: x[2] for x in payload}
                cmd = f"./smrt.py --username admin --password admin --host-mac={mac} --ip-address={ip} --switch-mac {p['mac']}"
                print(cmd)
            else:
                print(ip, mac, *payload, sep="\n")
                print("-"*16)

if __name__ == "__main__":
    main()
