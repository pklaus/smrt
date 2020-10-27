#!/usr/bin/env python

import random
import logging
import argparse
import netifaces

from .protocol import Protocol
from .network import Network, ConnectionProblem

logger = logging.getLogger(__name__)

def discover_switches():
    interfaces = netifaces.interfaces()
    settings = []
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET not in addrs:
            continue
        if netifaces.AF_LINK not in addrs:
            continue
        assert len(addrs[netifaces.AF_LINK]) == 1
        mac = addrs[netifaces.AF_LINK][0]['addr']
        for addr in addrs[netifaces.AF_INET]:
            if 'broadcast' not in addr or 'addr' not in addr:
                continue
            settings.append((iface, addr['addr'], mac, addr['broadcast']))

    ret = []
    for iface, ip, mac, broadcast in settings:
        net = Network(ip, mac)
        logger.warning((iface, ip, mac, broadcast))
        net.send(Protocol.DISCOVERY, {})
        while True:
            try:
                header, payload = net.receive()
                yield header, payload
            except ConnectionProblem:
                break

def main():
    switches = discover_switches()
    for header, payload in switches:
        print(*payload, sep="\n")
        print("-"*16)

if __name__ == "__main__":
    main()
