#!/usr/bin/env python

import socket
import time
import random
import logging
import argparse
import netifaces

from protocol import Protocol
from network import Network

from loglevel import loglevel

def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--switch-mac', '-s')
    parser.add_argument('--host-mac', )
    parser.add_argument('--ip-address', '-i')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    parser.add_argument('action', default=None, nargs='?')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    net = Network(args.ip_address, args.host_mac, args.switch_mac)
    actions = Protocol.tp_ids
    net.login(args.username, args.password)

    if args.action in actions:
        header, payload = net.query(Protocol.GET, [(actions[args.action], b'')])
        print(*payload, sep="\n")
    else:
        print("Actions:" , *actions.keys())

if __name__ == "__main__":
    main()
