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
    parser.add_argument('--switch-mac', '-s')
    parser.add_argument('--host-mac', )
    parser.add_argument('--ip-address', '-i')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--vlan', type=int)
    parser.add_argument('--vlan_name')
    parser.add_argument('--vlan_member', type=int)
    parser.add_argument('--vlan_tagged', type=int)
    parser.add_argument('--delete', action='store_true')
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    parser.add_argument('action', default=None, nargs='?')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    net = Network(args.ip_address, args.host_mac, args.switch_mac)
    actions = Protocol.tp_ids
    net.login(args.username, args.password)
    l = net.login_dict(args.username, args.password)
    if (args.delete):
        v = Protocol.set_vlan(int(args.vlan), 0, 0, "")
    else:
        v = Protocol.set_vlan(int(args.vlan), int(args.vlan_member), int(args.vlan_tagged), args.vlan_name)
    l.update({actions["vlan"]: v})
    header, payload = net.set(args.username, args.password, l)
    print(*payload, sep="\n")

if __name__ == "__main__":
    main()
