"""
TP-Link TL-SG105E and TL-SG108E switces
UDP configuration protocol

Wireshark filter:
ip.addr ==192.168.178.250 || ip.addr ==192.168.178.254 && udp.port == 29808
"""

import struct
from ipaddress import ip_address
from collections import OrderedDict

HEADER_LEN = 32
PACKET_END = b'\xff\xff\x00\x00'

DEFAULT_HEADER = {
  'fragment_offset': 0,
  'sequence_id': 0,
  'checksum': 0,
  'switch_mac': b'\x00\x00\x00\x00\x00\x00',
  'check_length': 0,
  'token_id': 0,
  'op_code': 0,
  'error_code': 0,
  'host_mac':   b'\x00\x00\x00\x00\x00\x00',
  'version': 1,
  'flag': 0
}

header_structure = {
  'fmt': '!bb6s6shihhhhi',
  'designators': [
    'version',
    'op_code',
    'switch_mac',
    'host_mac',
    'sequence_id',
    'error_code',
    'check_length',
    'fragment_offset',
    'flag',
    'token_id',
    'checksum',
  ]
}

DISCOVERY = 0
GET =       1
SET =       2
LOGIN =     3
RETURN =    4
READ5 =     5

op_codes = {
  DISCOVERY: 'DISCOVERY',
  GET:    'GET',
  SET:    'SET',
  LOGIN:  'LOGIN',
  RETURN: 'RETURN',
  READ5:  'READ5'
}

sequences = {
  # name      ->switch    switch->
  'login/change': (LOGIN,     RETURN),
  'query':        (GET,       SET),
  'discover':     (DISCOVERY, SET),
}

receive_ids = {
    1:     ['*s', 'str',   'type'],
    2:     ['*s', 'str',   'hostname'],
    3:     ['6s', 'hex',   'mac'],
    4:     ['4s', 'ip',    'ip_addr'],
    5:     ['4s', 'ip',    'ip_mask'],
    6:     ['4s', 'ip',    'gateway'],
    7:     ['*s', 'str',   'firmware_version'],
    8:     ['*s', 'str',   'hardware_version'],
    9:     ['?',  'bool',  'dhcp'],
    10:    ['b',  'dec',   'num_ports'],
    13:    ['?',  'bool',  'v4'],
    512:   ['*s', 'str',   'username'],
    514:   ['*s', 'str',   'password'],
    2304:  ['a',  'action','save'],
    2305:  ['a',  'action','get_token_id'],
    4352:  ['?',  'bool',  'igmp_snooping'],
    4096:  ['*s', 'hex',   'port_settings'],
    4608:  ['5s', 'hex',   'port_trunk'],
    8192:  ['2s', 'hex',   'mtu_vlan'],
    8704:  ['?',  'hex',   '802.1q vlan enabled'],
    8705:  ['*s', 'hex',   '802.1q vlan'],
    8706:  ['*s', 'hex',   '802.1q vlan pvid'],
    12288: ['?',  'bool',  'QoS Basic 1'],
    12289: ['2s', 'hex',   'QoS Basic 2'],
    16640: ['10s','hex',   'port_mirror'],
    16384: ['*s', 'hex',   'port_statistics'],
    17152: ['?',  'bool',  'loop_prevention'],
}

def get_sequence_kind(sequence):
    for key, value in sequences.items():
        if value == sequence: return key
    return 'unknown'

def get_id(name):
    for key, value in receive_ids.items():
        if value[2] == name: return key
    raise Exception()

def hex_readable(bts):
    return ':'.join(['{:02X}'.format(byte) for byte in bts])

def payload_str(payload):
    ret = ''
    if type(payload) == bytes:
        items = interpret_payload(payload)
    else:
        items = payload
    for item_id in items.keys():
        value = items[item_id]
        try:
            value = interpret_value(value, receive_ids[item_id][1])
        except:
            pass
        if item_id not in receive_ids:
            ret += 'Unknown code: %s (content: %s)\n' % (item_id, value)
            continue
        struct_fmt = receive_ids[item_id][0]
        kind = receive_ids[item_id][1]
        name = receive_ids[item_id][2]
        fmt = '{name}: {value}  (id: {id}, kind: {kind})\n'
        ret += fmt.format(name=name, value=value, id=item_id, kind=kind)
    return ret

def decode(data):
    data = list(data)
    key = [ 191, 155, 227, 202, 99, 162, 79, 104, 49, 18, 190, 164, 30,
      76, 189, 131, 23, 52, 86, 106, 207, 125, 126, 169, 196, 28, 172, 58,
      188, 132, 160, 3, 36, 120, 144, 168, 12, 231, 116, 44, 41, 97, 108,
      213, 42, 198, 32, 148, 218, 107, 247, 112, 204, 14, 66, 68, 91, 224,
      206, 235, 33, 130, 203, 178, 1, 134, 199, 78, 249, 123, 7, 145, 73,
      208, 209, 100, 74, 115, 72, 118, 8, 22, 243, 147, 64, 96, 5, 87, 60,
      113, 233, 152, 31, 219, 143, 174, 232, 153, 245, 158, 254, 70, 170,
      75, 77, 215, 211, 59, 71, 133, 214, 157, 151, 6, 46, 81, 94, 136,
      166, 210, 4, 43, 241, 29, 223, 176, 67, 63, 186, 137, 129, 40, 248,
      255, 55, 15, 62, 183, 222, 105, 236, 197, 127, 54, 179, 194, 229,
      185, 37, 90, 237, 184, 25, 156, 173, 26, 187, 220, 2, 225, 0, 240,
      50, 251, 212, 253, 167, 17, 193, 205, 177, 21, 181, 246, 82, 226,
      38, 101, 163, 182, 242, 92, 20, 11, 95, 13, 230, 16, 121, 124, 109,
      195, 117, 39, 98, 239, 84, 56, 139, 161, 47, 201, 51, 135, 250, 10,
      19, 150, 45, 111, 27, 24, 142, 80, 85, 83, 234, 138, 216, 57, 93,
      65, 154, 141, 122, 34, 140, 128, 238, 88, 89, 9, 146, 171, 149, 53,
      102, 61, 114, 69, 217, 175, 103, 228, 35, 180, 252, 200, 192, 165,
      159, 221, 244, 110, 119, 48]
    length = len(data)
    #s = [bytes([char]) for char in key]
    s = key
    i, j = 0, 0
    for k in range(length):
        i = (k + 1) % 256;
        j = (j + s[i]) % 256;
        s[i], s[j] = s[j], s[i]
        data[k] = data[k] ^ s[(s[i] + s[j]) % 256];
    return bytes(data)

encode = decode

def split(data):
    assert len(data) >= HEADER_LEN + len(PACKET_END)
    assert data.endswith(PACKET_END)
    return (data[0:HEADER_LEN], data[HEADER_LEN:])

def interpret_header(header):
    names = header_structure['designators']
    vals = struct.unpack(header_structure['fmt'], header)
    return dict(zip(names, vals))

def interpret_payload(payload):
    results = []
    while len(payload) > len(PACKET_END):
        dtype, dlen = struct.unpack('!hh', payload[0:4])
        data = payload[4:4+dlen]
        payload = payload[4+dlen:]
        results.append( (dtype, data) )
    return results

def assemble_packet(header, payload):
    payload_bytes = b''
    for dtype, value in payload.items():
        payload_bytes += struct.pack('!hh', dtype, len(value))
        payload_bytes += value
    header['check_length'] = HEADER_LEN + len(payload_bytes) + len(PACKET_END)
    header = tuple(header[part] for part in header_structure['designators'])
    header_bytes = struct.pack(header_structure['fmt'], *header)
    return header_bytes + payload_bytes + PACKET_END

def interpret_value(value, kind):
    if kind == 'str':
        value = value.split(b'\x00', 1)[0].decode('ascii')
    elif kind == 'ip':
        value = ip_address(value)
    elif kind == 'hex':
        value = ':'.join(['{:02X}'.format(byte) for byte in value])
    elif kind == 'action':
        value = "n/a"
    elif kind == 'dec':
        value = int(''.join('%02X' % byte for byte in value), 16)
    elif kind == 'bool':
        if   len(value) == 0: pass
        elif len(value) == 1: value = value[0] > 0
        else: raise AssertionError('boolean should be one byte long')
    return value

def get_payload_item_context(items, name_key):
    hits = [key for key in items.keys() if receive_ids[key][2] == name_key]
    assert len(hits) == 1
    item_id = hits[0]

    kind = receive_ids[item_id][1]
    raw_value = items[item_id]
    value = interpret_value(raw_value, kind)

    return {
      'id': item_id,
      'struct_fmt': receive_ids[item_id][0],
      'kind': kind,
      'name': receive_ids[item_id][2],
      'value': value,
      'raw_value': raw_value,
    }

def get_payload_item_value(items, name_key):
    context = get_payload_item_context(items, name_key)
    return context['value']
