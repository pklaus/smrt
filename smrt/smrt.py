#!/usr/bin/env python

import socket, time, random, argparse, logging

from .protocol import Protocol
from .network import Network

def loglevel(x):
    try:
        return getattr(logging, x.upper())
    except AttributeError:
        raise argparse.ArgumentError('Select a proper loglevel')

def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', '-c')
    parser.add_argument('--switch-mac', '-s')
    parser.add_argument('--host-mac', )
    parser.add_argument('--ip-address', '-i')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    parser.add_argument('action')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    sc = Network(args.ip_address, args.host_mac, args.switch_mac)
    sc.login(args.username, args.password)

    actions = {
            "ports":   4096,
            "stats": 16384,
            "mirror": 16640,
            "vlan":   8704,
            "pvid":   8706,
    }

    if args.action in actions:
        header, payload = sc.query(Protocol.GET, {actions[args.action]: b''})
    else:
        header, payload = sc.query(Protocol.GET, {int(args.action): b''})

    print(*payload, sep="\n")

if __name__ == "__main__":
    main()
