import struct
import urwid
from bs4 import BeautifulSoup


class TCP:

    def __init__(self, raw_data):
        (self.src_port, self.dest_port, self.sequence, self.acknowledgment, offset_reserved_flags) = struct.unpack(
            '! H H L L H', raw_data[:14])
        self.offset = (offset_reserved_flags >> 12) * 4
        self.reserved = (offset_reserved_flags & 3584) >> 9
        self.flag_non = (offset_reserved_flags & 256) >> 8
        self.flag_con = (offset_reserved_flags & 128) >> 7
        self.flag_ecn = (offset_reserved_flags & 64) >> 6
        self.flag_urg = (offset_reserved_flags & 32) >> 5
        self.flag_ack = (offset_reserved_flags & 16) >> 4
        self.flag_psh = (offset_reserved_flags & 8) >> 3
        self.flag_rst = (offset_reserved_flags & 4) >> 2
        self.flag_syn = (offset_reserved_flags & 2) >> 1
        self.flag_fin = offset_reserved_flags & 1
        self.data = raw_data[self.offset:]
        self.type = None
        if ((self.src_port == 80 or self.dest_port == 80) and self.flag_psh) or (
                self.src_port == 80 and len(self.data) > 30):
            self.type = 'http'
            self.data = BeautifulSoup(self.data, 'html.parser').prettify()
            # self.data.

    def get_name(self):
        name = ''

        name += '{:18}'.format(f'{self.src_port} --> {self.dest_port} ')

        if (self.src_port == 443 or self.dest_port == 443) and self.flag_psh:
            name += 'TLSv1.2 '
        if self.type == 'http':
            name += 'HTTP '
            if self.dest_port == 80:
                name += self.data.splitlines()[0]

        else:
            name += 'TCP '
            if self.flag_syn == 1:
                name += '[SYN]'
            if self.flag_ack == 1:
                name += '[ACK]'
            if self.flag_rst == 1:
                name += '[RST]'
            if self.flag_fin == 1:
                name += '[FIN]'

        return name

    def get_description(self):
        description = [urwid.Text(('layer_title', 'Transmission Control Protocol')),
                       urwid.Text(('layer_desc', f'Source Port: {self.src_port}')),
                       urwid.Text(('layer_desc', f'Destination Port: {self.dest_port}')),
                       urwid.Text(('layer_desc', f'Sequence Number: {self.sequence} bytes')),
                       urwid.Text(('layer_desc', f'Acknowledgment Number: {self.acknowledgment}')),
                       urwid.Text(('layer_desc', f'Header Length: {self.offset}')),
                       urwid.Text(('layer_desc', f'FLAGS:')),
                       urwid.Text(('layer_desc', f'Reserved: {self.reserved} bytes')),
                       urwid.Text(('layer_desc', f'Nonce Flag: : {self.flag_non}')),
                       urwid.Text(('layer_desc', f'Congestion Window Reduced: {self.flag_con}')),
                       urwid.Text(('layer_desc', f'ECN-Echo: {self.flag_ecn}')),
                       urwid.Text(('layer_desc', f'Urgent: {self.flag_urg}')),
                       urwid.Text(('layer_desc', f'Acknowledgment: {self.flag_ack}')),
                       urwid.Text(('layer_desc', f'Push: {self.flag_psh}')),
                       urwid.Text(('layer_desc', f'Reset: {self.flag_rst}')),
                       urwid.Text(('layer_desc', f'Syn: {self.flag_syn}')),
                       urwid.Text(('layer_desc', f'Fin: {self.flag_fin}'))
                       ]
        if self.type == 'http':
            description.append(urwid.Text(('layer_desc', f'{self.data.prettify()}')))
        else:

            description.append(urwid.Text(('layer_desc', f'DATA:')))
            description.append(urwid.Text(('layer_desc', f'{self.data}')))

        return description
