#!/usr/bin/env python

import random
import logging
import argparse
import netifaces

from protocol import Protocol
from network import Network, ConnectionProblem
from loglevel import loglevel

logger = logging.getLogger(__name__)

class InterfaceProblem(Exception):
    pass

def discover_switches(interface=None):
    if interface is None:
        interfaces = netifaces.interfaces()
        if "lo" in interfaces:
            interfaces.remove("lo")
        if len(interfaces) > 1:
            msg = [""]
            msg.append("Error: more than 1 interface. Use -i or --interface to specify the name")
            msg.append("Interfaces:")
            for iface in interfaces:
                msg.append("    " + repr(iface))
            raise InterfaceProblem("\n".join(msg))

    settings = []
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET not in addrs:
        raise ConnectionProblem("Error: not AF_INTER address")
    if netifaces.AF_LINK not in addrs:
        raise ConnectionProblem("Error: not AF_LINK address")
    assert len(addrs[netifaces.AF_LINK]) == 1
    mac = addrs[netifaces.AF_LINK][0]['addr']
    for addr in addrs[netifaces.AF_INET]:
        if 'broadcast' not in addr or 'addr' not in addr:
            continue
        settings.append((interface, addr['addr'], mac, addr['broadcast']))

    ret = []
    for iface, ip, mac, broadcast in settings:
        net = Network(ip, mac)
        logger.debug((iface, ip, mac, broadcast))
        net.send(Protocol.DISCOVERY, {})
        while True:
            try:
                header, payload = net.receive()
                yield header, payload
            except ConnectionProblem:
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i')
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    switches = discover_switches(args.interface)
    for header, payload in switches:
        print(*payload, sep="\n")
        print("-"*16)

if __name__ == "__main__":
    main()
