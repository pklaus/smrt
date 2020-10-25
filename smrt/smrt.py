#!/usr/bin/env python

import socket, time, random, argparse, logging

from .protocol import *
from .network import SwitchConversation
from .operations import *

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

    switch_mac = args.switch_mac
    host_mac = args.host_mac
    ip_address = args.ip_address

    sc = SwitchConversation(switch_mac, host_mac, ip_address)

    sc.login(args.username, args.password)

    actions = {
            "stat":   4096,
            "mirror": 16640,
            "vlan":   8704,
            "pvid":   8706,
    }

    if args.action in actions:
        header, payload = sc.query(GET, {actions[args.action]: b''})
    else:
        header, payload = sc.query(GET, {int(args.action): b''})

    print(*decode_payload(payload), sep="\n")

if __name__ == "__main__":
    main()
