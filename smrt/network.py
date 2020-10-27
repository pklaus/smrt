#!/usr/bin/env python

import socket, random, logging

from .protocol import Protocol

logger = logging.getLogger(__name__)

class Network:

    BROADCAST_ADDR = "255.255.255.255"
    UDP_SEND_TO_PORT = 29808
    UDP_RECEIVE_FROM_PORT = 29809

    def __init__(self, switch_mac, host_mac, ip_address):

        self.switch_mac = '00:00:00:00:00:00' if switch_mac is None else switch_mac
        self.host_mac = host_mac
        self.ip_address = ip_address

        self.sequence_id = random.randint(0, 1000)

        header = Protocol.header["blank"].copy()
        header.update({
          'sequence_id': self.sequence_id,
          'host_mac':   Network.mac_to_bytes(self.host_mac),
          'switch_mac': Network.mac_to_bytes(self.switch_mac),
        })
        self.header = header

        # Sending socket
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ss.bind((ip_address, Network.UDP_RECEIVE_FROM_PORT))

        # Receiving socket
        rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rs.bind((Network.BROADCAST_ADDR, Network.UDP_RECEIVE_FROM_PORT))
        rs.settimeout(0.4)

        self.ss, self.rs = ss, rs

    def mac_to_bytes(mac):
        return bytes(int(byte, 16) for byte in mac.split(':'))

    def mac_to_str(mac):
        return ':'.join('{:02X}'.format(byte) for byte in mac)

    def send(self, op_code, payload):
        self.sequence_id = (self.sequence_id + 1) % 1000

        header = self.header
        header.update({
          'sequence_id': self.sequence_id,
          'op_code': op_code,
        })

        logger.debug('Sending Header:  ' + str(header))
        logger.debug('Sending Payload: ' + str(payload))
        packet = Protocol.assemble_packet(header, payload)
        packet = Protocol.encode(packet)
        self.send_packet(packet)

    def send_packet(self, packet):
        self.ss.sendto(packet, (Network.BROADCAST_ADDR, Network.UDP_SEND_TO_PORT))

    def receive(self):
        try:
            data, addr = self.rs.recvfrom(1500)
            data = Protocol.decode(data)
            header, payload = Protocol.split(data)
            header, payload = Protocol.interpret_header(header), Protocol.interpret_payload(payload)
            logger.debug('Received Header:  ' + str(header))
            logger.debug('Received Payload: ' + str(payload))
            self.header['token_id'] = header['token_id']
            return header, payload
        except:
            print("no response")
            raise ConnectionProblem()
            return {}, {}

    def query(self, op_code, payload):
        self.send(op_code, payload)
        header, payload = self.receive()
        sequence_kind = Protocol.get_sequence_kind((op_code, header['op_code']))
        logger.debug('Sequence kind: ' + sequence_kind)
        return header, payload

    def login(self, username, password):
        self.query(Protocol.GET, {Protocol.get_id("get_token_id"): b''})
        username = username.encode('ascii') + b'\x00'
        password = password.encode('ascii') + b'\x00'
        self.query(
                Protocol.LOGIN,
                {Protocol.get_id('username'): username, Protocol.get_id('password'): password}
        )
