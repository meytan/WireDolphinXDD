import struct
import urwid


class PPPoE:
    def __init__(self, raw_data):
        version_type = raw_data[0]
        self.version = version_type >> 4
        self.type = (version_type & 15) * 4
        code, session_id, self.payload_length = struct.unpack('! x B H H', raw_data[:6])
        self.code = '0x' + hex(code)[2:].zfill(2)
        self.session_id = '0x' + hex(session_id)[2:].zfill(4)
        self.data = raw_data[6:]

    @staticmethod
    def get_protocol_name():
        return 'PPPoE'

    @staticmethod
    def get_desc_protocol_name():
        return 'PPPoE (0x8863)'

    def get_name(self):
        return ''

    def get_description(self):
        description = [
            urwid.Text(('layer_title', 'PPP-over-Ethernet')),
            urwid.Text(('layer_desc', f'Version: {self.version}')),
            urwid.Text(('layer_desc', f'Type: {self.type}')),
            urwid.Text(('layer_desc', f'Code: {self.code}')),
            urwid.Text(('layer_desc', f'Session ID: {self.session_id}')),
            urwid.Text(f'Payload Length: {self.payload_length} bytes')
        ]
        return description

    # def pppoe_code_dict(self,):
