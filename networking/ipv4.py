import struct
import urwid

from networking.TCP import TCP
from networking.UDP import UDP

protocols = {
    0: 'HOPOPT',
    1: 'ICMP',
    2: 'IGMP',
    3: 'GGP',
    4: 'IP',
    5: 'ST',
    6: 'TCP',
    7: 'CBT',
    8: 'EGP',
    9: 'IGP',
    10: 'BBN - RCC - MON',
    11: 'NVP - II',
    12: 'PUP',
    13: 'ARGUS',
    14: 'EMCON',
    15: 'XNET',
    16: 'CHAOS',
    17: 'UDP',
    18: 'MUX',
    19: 'DCN - MEAS',
    20: 'HMP',
    21: 'PRM'
}


class Ipv4:
    def __init__(self, raw_data):
        version_header_length = raw_data[0]
        self.version = version_header_length >> 4
        self.header_length = (version_header_length & 15) * 4
        self.total_length, self.ttl, proto, src, target = struct.unpack('! 2x H 4x B B 2x 4s 4s', raw_data[:20])
        self.src = self.ipv4(src)
        self.target = self.ipv4(target)
        self.data = raw_data[self.header_length:]
        self.protocol = protocols.get(proto, proto)
        self.next_layer = None
        if self.protocol == 'TCP':
            self.next_layer = TCP(self.data)
        elif self.protocol == 'UDP':
            self.next_layer = UDP(self.data)

    @staticmethod
    def get_protocol_name():
        return 'IPv4'

    @staticmethod
    def get_desc_protocol_name():
        return 'IPv4 (0x0800)'

    def get_name(self):
        name = "{:17}{:17}".format(self.src, self.target)

        if self.next_layer is not None:
            name += self.next_layer.get_name()
        else:
            name += self.protocol
        return name

    def get_description(self):
        description = [urwid.Text(('layer_title', 'Internet Protocol Version 4')),
                       urwid.Text(('layer_desc', f'Version: {self.version}')),
                       urwid.Text(('layer_desc', f'Header Length: {self.header_length} bytes')),
                       urwid.Text(('layer_desc', f'Total Length: {self.total_length} bytes')),
                       urwid.Text(('layer_desc', f'TTL: {self.ttl}')),
                       urwid.Text(('layer_desc', f'Protocol: {self.protocol}')),
                       urwid.Text(('layer_desc', f'Source: : {self.src}')),
                       urwid.Text(('layer_desc', f'Destination: {self.target}'))
                       ]
        if self.next_layer is not None:
            description.extend(self.next_layer.get_description())
        return description

    def ipv4(self, addr):
        return '.'.join(map(str, addr))
