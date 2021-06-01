#!/usr/bin/env python

import socket, time, random, argparse, logging

from protocol import Protocol
from network import Network, InterfaceProblem
from binary import ports2byte, ports2list

def loglevel(x):
    try:
        return getattr(logging, x.upper())
    except AttributeError:
        raise argparse.ArgumentError('Select a proper loglevel')

def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('--switch-mac', '-s')
    parser.add_argument('--interface', '-i')
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--vlan', type=int)
    parser.add_argument('--vlan_name')
    parser.add_argument('--vlan_member')
    parser.add_argument('--vlan_tagged')
    parser.add_argument('--vlan_pvid')
    parser.add_argument('--delete', action="store_true")
    parser.add_argument('--loglevel', '-l', type=loglevel, default='INFO')
    parser.add_argument('action', default=None, nargs='?')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    actions = Protocol.tp_ids

    if args.action not in Protocol.tp_ids:
            print("Actions:\n")
            for action in Protocol.ids_tp.keys():
                if Protocol.ids_tp[action][2]:
                    print("%s:%s %s [%s]" %
                        (Protocol.ids_tp[action][1],
                        tabout(Protocol.ids_tp[action][1]),
                        Protocol.ids_tp[action][3],
                        Protocol.ids_tp[action][0]))
    else:
        net = None
        try:
            net = Network(args.interface, args.switch_mac)
        except InterfaceProblem as e:
            print("Error:", e)

        if net:
            net.login(args.username, args.password)
        else:
            exit(1)

        if args.action == "vlan" and args.vlan:
            if args.vlan_member or args.vlan_tagged or args.delete:
                if (args.delete):
                    v = Protocol.set_vlan(int(args.vlan), 0, 0, "")
                else:
                    v = Protocol.set_vlan(int(args.vlan), ports2byte(args.vlan_member), ports2byte(args.vlan_tagged), args.vlan_name)
                l = [(actions["vlan"], v)]

            if args.vlan_pvid is not None:
                l = []
                for port in ports2list(args.vlan_pvid):
                    if port != 0:
                        l.append( (actions["pvid"], Protocol.set_pvid(args.vlan, port)) )
            header, payload = net.set(args.username, args.password, l)
        elif args.action in actions:
            header, payload = net.query(Protocol.GET, [(actions[args.action], b'')])
        print(*payload, sep="\n")

def tabout(cmd):
    # Format help output
    if len(cmd) < 8:
      return "\t\t"
    return "\t"

if __name__ == "__main__":
    main()
