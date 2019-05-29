import struct
import urwid

from networking.ipv4 import Ipv4
from networking.pppoed import PPPoE


class Ethernet:
    def __init__(self, raw_data, nr):
        dest, src, protocol = struct.unpack('! 6s 6s H', raw_data[:14])

        self.dest_mac = self.get_mac_addr(src)
        self.src_mac = self.get_mac_addr(src)
        self.proto = '0x' + hex(protocol)[2:].zfill(4)
        self.desc_proto = self.proto
        self.data = raw_data[14:]
        self.nr = nr
        self.next_layer = None
        if self.proto == '0x0800':
            self.next_layer = Ipv4(self.data)
        elif self.proto == '0x8863':
            self.next_layer = PPPoE(self.data)
        elif self.proto == '0x86dd':
            self.proto = 'IPv6'
        if self.next_layer:
            self.proto = self.next_layer.get_protocol_name()
            self.desc_proto = self.next_layer.get_desc_protocol_name()

    def get_name(self):

        name = '{:<7d}'.format(self.nr)

        name += '{:9}{:20}{:20}'.format(self.proto, self.src_mac, self.dest_mac)
        if self.next_layer is not None:
            name += self.next_layer.get_name()
        name = (name[:200] + '..') if len(name) > 200 else name
        return name + ' '

    def get_description(self):

        description = [urwid.Text(('layer_title', 'Ethernet II')),
                       urwid.Text(('layer_desc\\', f'Destination: {self.dest_mac}')),
                       urwid.Text(('layer_desc', f'Source: {self.src_mac}')),
                       urwid.Text(('layer_desc', f'Type: {self.desc_proto}'))
                       ]
        if self.next_layer is not None:
            description.extend(self.next_layer.get_description())
        return description

    @staticmethod
    def get_mac_addr(mac_raw):
        byte_str = map('{:02x}'.format, mac_raw)
        mac_addr = ':'.join(byte_str).upper()
        return mac_addr
