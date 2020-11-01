#!/usr/bin/env python

import socket, time, random, argparse, logging

from protocol import Protocol
from network import Network

def loglevel(x):
    try:
        return getattr(logging, x.upper())
    except AttributeError:
        raise argparse.ArgumentError('Select a proper loglevel')

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
    # l = net.login_dict(args.username, args.password)
    # v = Protocol.set_vlan(10, 255, 248, "test2")
    # l.update({actions["vlan"]: v})
    # net.set(args.username, args.password, l)

    if args.action in actions:
        header, payload = net.query(Protocol.GET, [(actions[args.action], b'')])
        print(*payload, sep="\n")
    else:
        print("Actions:" , *actions.keys())

if __name__ == "__main__":
    main()
