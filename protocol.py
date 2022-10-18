import struct
from ipaddress import ip_address
from binary import byte2ports,mac_to_str

class Protocol:
    PACKET_END = b'\xff\xff\x00\x00'

    KEY = bytes ([191, 155, 227, 202, 99, 162, 79, 104, 49, 18, 190, 164, 30,
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
    159, 221, 244, 110, 119, 48])

    header = {
        "len": 32,
        "fmt": '!bb6s6shihhhhi',
        "blank": {
            'version': 1,
            'op_code': 0,
            'switch_mac': b'\x00\x00\x00\x00\x00\x00',
            'host_mac':   b'\x00\x00\x00\x00\x00\x00',
            'sequence_id': 0,
            'error_code': 0,
            'check_length': 0,
            'fragment_offset': 0,
            'flag': 0,
            'token_id': 0,
            'checksum': 0,
        }
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

    ids_tp = {
        1:     ('str',   'type',	0),
        2:     ('str',   'hostname',	1,	"Without arguments, shows switch details"),
        3:     ('hex',   'mac',		0),
        4:     ('ip',    'ip_addr',	0),
        5:     ('ip',    'ip_mask',	0),
        6:     ('ip',    'gateway',	0),
        7:     ('str',   'firmware',	0),
        8:     ('str',   'hardware',	0),
        9:     ('bool',  'dhcp', 	0),
        10:    ('dec',   'num_ports',	0),
        12:    ('bool',  'led_status',	0),
        13:    ('bool',  'auto_save',	0),
        14:    ('bool',  'is_factory',	0),
        15:    ('hex',   'flash_type',  0),
        512:   ('str',   'username',	0),
        514:   ('str',   'password',	0),
        773:   ('bool',  'reboot',	1,	"Reboot the device"),
        2304:  ('action','save',	1,	"Saves the current configuration"),
        2305:  ('action','get_token_id',1,	"Unknown"),
        4352:  ('bool',  'igmp_snooping', 0),
        4096:  ('hex',   'ports',	0),
        4608:  ('hex',   'trunk',	0),
        8192:  ('hex',   'mtu_vlan',	0),
        8704:  ('hex',   'vlan_enabled', 0),
        8705:  ('vlan',  'vlan', 	1,	"Configure VLAN Membership"),
        8706:  ('pvid',  'pvid',	0),
        8707:  ('str',   'vlan_filler',	0),
        12288: ('bool',  'qos1',	0),
        12289: ('hex',   'qos2',	0),
        16640: ('hex',   'mirror',	0),
        16384: ('stat',  'stats',	0),
        17152: ('bool',  'loop_prev',	0),
    }

    tp_ids = {v[1]: k for k, v in ids_tp.items()}

    def get_sequence_kind(sequence):
        for key, value in Protocol.sequences.items():
            if value == sequence: return key
        return 'unknown'

    def get_id(name):
        return Protocol.tp_ids[name]

    def decode(data):
        data = bytearray(data)
        s = bytearray(Protocol.KEY)
        j = 0
        for k in range(len(data)):
            i = (k + 1) & 255
            j = (j + s[i]) & 255
            s[i], s[j] = s[j], s[i]
            data[k] = data[k] ^ s[(s[i] + s[j]) & 255]
        return bytes(data)

    encode = decode

    def split(data):
        if len(data) < Protocol.header["len"] + len(Protocol.PACKET_END):
            raise AssertionError('invalid data length')
        if not data.endswith(Protocol.PACKET_END):
            raise AssertionError('data without packet end')
        return (data[0:Protocol.header["len"]], data[Protocol.header["len"]:])

    def interpret_header(header):
        names = Protocol.header['blank'].keys()
        vals = struct.unpack(Protocol.header['fmt'], header)
        return dict(zip(names, vals))

    def interpret_payload(payload):
        results = []
        while len(payload) > len(Protocol.PACKET_END):
            dtype, dlen = struct.unpack('!hh', payload[0:4])
            data = payload[4:4+dlen]
            results.append( (
                dtype,
                Protocol.ids_tp[dtype][1],
                Protocol.interpret_value(data, Protocol.ids_tp[dtype][0])
                )
            )
            payload = payload[4+dlen:]
        return results

    def analyze(data):
        header, payload = Protocol.split(data)
        return Protocol.interpret_header(header), Protocol.interpret_payload(payload)

    def assemble_packet(header, payload):
        payload_bytes = b''
        for dtype, value in payload:
            payload_bytes += struct.pack('!hh', dtype, len(value))
            payload_bytes += value
        header['check_length'] = Protocol.header["len"] + len(payload_bytes) + len(Protocol.PACKET_END)
        header = tuple(header[part] for part in Protocol.header['blank'].keys())
        header_bytes = struct.pack(Protocol.header['fmt'], *header)
        return header_bytes + payload_bytes + Protocol.PACKET_END

    def interpret_value(value, kind):
        if kind == 'str':
            value = value.split(b'\x00', 1)[0].decode('ascii')
        elif kind == 'ip':
            value = ip_address(value)
        elif kind == 'hex':
            value = mac_to_str(value)
        elif kind == 'action':
            value = "n/a"
        elif kind == 'dec':
            value = int.from_bytes(value, 'big')
        elif kind == 'vlan':
            value = list(struct.unpack("!hii", value[:10]) + (value[10:-1].decode('ascii'), ))
            value[1] = byte2ports(value[1])
            value[2] = byte2ports(value[2])
        elif kind == 'pvid':
                value = struct.unpack("!bh", value) if value else None
        elif kind == 'stat':
            value = struct.unpack("!bbbiiii", value)
        elif kind == 'bool':
            if   len(value) == 0:
                pass
            elif len(value) == 1:
                value = value[0] > 0
            else:
                raise AssertionError('boolean should be one byte long')
        return value

    def set_vlan(vlan_num, member_mask, tagged_mask, vlan_name):
        value = struct.pack("!hii",vlan_num, member_mask, tagged_mask) + vlan_name.encode("ascii") + b'\x00'
        return value

    def set_pvid(vlan_num, port):
        value = struct.pack("!bh", port, vlan_num)
        return value

if __name__ == "__main__":
    #v = Protocol.set_vlan(10, 255, 254, "test")
    #print(v, len(v))
    out = bytearray()
    print(Protocol.set_pvid(90, 5).hex())
