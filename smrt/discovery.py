#!/usr/bin/env python

import random
import logging
import argparse
import netifaces

from . import IncompatiblePlatformException
from .protocol import Protocol
from .network import Network

logger = logging.getLogger(__name__)

def discover_switches():
    interfaces = netifaces.interfaces()
    settings = []
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET not in addrs: continue
        if netifaces.AF_LINK not in addrs: continue
        assert len(addrs[netifaces.AF_LINK]) == 1
        mac = addrs[netifaces.AF_LINK][0]['addr']
        for addr in addrs[netifaces.AF_INET]:
            if 'broadcast' not in addr or 'addr' not in addr: continue
            settings.append((iface, addr['addr'], mac, addr['broadcast']))

    for iface, ip, mac, broadcast in settings:
        net = Network(None, mac, ip)
        logger.warning((iface, ip, mac, broadcast))
        net.send(Protocol.DISCOVERY, {})
        header, payload = net.receive()
        yield header, payload

def main():
    switches = discover_switches()
    for header, payload in switches:
        print(*payload, sep="\n")
        print("-"*16)

if __name__ == "__main__":
    main()
