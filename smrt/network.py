#!/usr/bin/env python

import socket, random, logging

from .protocol import *
from .operations import *

BROADCAST_ADDR = "255.255.255.255"
UDP_SEND_TO_PORT = 29808
UDP_RECEIVE_FROM_PORT = 29809

logger = logging.getLogger(__name__)

def mac_to_bytes(mac):
    return bytes(int(byte, 16) for byte in mac.split(':'))

def mac_to_str(mac):
    return ':'.join('{:02X}'.format(byte) for byte in mac)

class SwitchConversation(object):

    def __init__(self, switch_mac, host_mac, ip_address):

        self.switch_mac = switch_mac
        self.host_mac = host_mac
        self.ip_address = ip_address

        self.sequence_id = random.randint(0, 1000)

        header = DEFAULT_HEADER.copy()
        header.update({
          'sequence_id': self.sequence_id,
          'host_mac':   mac_to_bytes(host_mac),
          'switch_mac': mac_to_bytes(switch_mac),
        })
        self.header = header

        # Sending socket
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ss.bind((ip_address, UDP_RECEIVE_FROM_PORT))
    
        # Receiving socket
        rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rs.bind((BROADCAST_ADDR, UDP_RECEIVE_FROM_PORT))
        rs.settimeout(0.4)

        self.ss, self.rs = ss, rs

    def send(self, op_code, payload):
        self.sequence_id = (self.sequence_id + 1) % 1000

        header = self.header
        header.update({
          'sequence_id': self.sequence_id,
          'op_code': op_code,
        })

        logger.debug('Sending Header:  ' + str(header))
        logger.debug('Sending Payload: ' + str(payload))
        packet = assemble_packet(header, payload)
        packet = encode(packet)

        self.ss.sendto(packet, (BROADCAST_ADDR, UDP_SEND_TO_PORT))

    def receive(self):
        try:
            fragment_offset = 1
            total_payload = b''
            while fragment_offset:
                data, addr = self.rs.recvfrom(1500)
                data = decode(data)
                header, payload = split(data)
                header, payload = interpret_header(header), interpret_payload(payload)
                fragment_offset = header['fragment_offset']
                logger.debug('Received Header:  ' + str(header))
                logger.debug('Received Payload: ' + str(payload))
                self.header['token_id'] = header['token_id']
                total_payload += payload
            return header, payload
        except:
                print("no response")
                raise ConnectionProblem()
                return {}, {}

    def query(self, op_code, payload):
        self.send(op_code, payload)
        header, payload = self.receive()
        sequence_kind = get_sequence_kind((op_code, header['op_code']))
        logger.debug('Sequence kind: ' + sequence_kind)
        return header, payload

    def login(self, username, password):
        self.query(GET, get_token_id_payload())
        self.query(LOGIN, login_payload(username, password))

