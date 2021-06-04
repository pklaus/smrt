#!/usr/bin/env python

################################################################################################
# Listen to bidirectional network communication (to and from TP-Link switches / easy switch tool
# Analyze the network communications

import socket, time, random, argparse, logging
from protocol import Protocol
from network import Network

def show_packet(payload):
        print(payload)
        data = Protocol.decode(payload)
        print("TEST: " + data.hex(" "))
        try:
            print(Protocol.analyze(data)[1])
        except AssertionError:
            return
        except KeyError:
            return

def main():

    # Handle command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i')
    args = parser.parse_args()

    # Instantiate network driver
    net = None
    try:
        net = Network(args.interface, "fe:ff:ff:ff:ff:ff")
    except InterfaceProblem as e:
        print("Error:", e)

    while True:
        data = net.recieve_socket(net.rs)
        if data:
            show_packet(data)
        data = net.recieve_socket(net.ss)
        if data:
            show_packet(data)

        time.sleep(0.1)

if __name__ == '__main__':
    main()

