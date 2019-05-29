import struct
import urwid


class UDP:

    def __init__(self, raw_data):
        self.src_port, self.dest_port, self.size = struct.unpack('! H H 2x H', raw_data[:8])
        self.data = raw_data[8:]

    def get_name(self):
        name = ''
        name += '{:18}UDP '.format(f'{self.src_port} --> {self.dest_port} ')
        return name

    def get_description(self):
        description = [urwid.Text(('layer_title', 'User Datagram Protocol')),
                       urwid.Text(('layer_desc', f'Source Port: {self.src_port}')),
                       urwid.Text(('layer_desc', f'Destination Port: {self.dest_port}')),
                       urwid.Text(('layer_desc', f'Length: {self.size}')),
                       urwid.Text(('layer_desc', f'DATA:')),
                       urwid.Text(('layer_desc', f'{self.data}'))]

        return description
