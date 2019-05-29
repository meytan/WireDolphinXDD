import select
import socket
import urwid

from packet_list_box import PacketListBox


class WireDolphin:
    palette = [
        ('reveal focus', 'black', 'dark cyan', 'standout'),
        ('reveal focus1', 'black', 'black', 'standout'),
        ('layer_title', 'dark red', 'black'),
        ('layer_desc', 'white', 'black')
    ]

    def __init__(self):
        header_text = urwid.Text(
            ('banner', '{:<6}{:<15}{:<19}{:<19}{:17}{:25}{} '.format(
                'Nr.', 'EtherType', 'Src. MAC', 'Dst. Mac', 'Src. IP', 'Dst. IP', 'Info')),
            align='left')
        self.header = urwid.AttrMap(header_text, 'banner')
        self.listbox = PacketListBox()
        self.listbox.offset_rows = 0
        self.listbox.inset_fraction = 1
        self.filter = urwid.Edit("Filter: ")
        self.footer = urwid.AttrWrap(self.filter, 'foo')
        self.view = urwid.Frame(
            self.listbox,
            header=urwid.AttrWrap(self.header, 'head'),
            footer=urwid.LineBox(self.footer))
        self.view = urwid.LineBox(self.view)
        self.loop_widget = self.view
        self.loop = urwid.MainLoop(self.loop_widget, palette=self.palette, unhandled_input=self.unhandled_input)
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        self.sock.setblocking(0)
        self.readable, writable, exceptional = select.select([self.sock], [], [self.sock])
        self.check_for_packets()
        self.focus = True  # True if list is focused False when filter
        self.details_showed = False  # True if list is focused False when filter

    def main(self):
        self.loop.run()

    def check_for_packets(self):
        self.loop.set_alarm_in(0.01, self._check)

    def _check(self, a, b):
        if self.listbox.is_searching:
            try:
                for s in self.readable:
                    raw_data, addr = s.recvfrom(65535)
                    self.listbox.add_item(raw_data)

            except BlockingIOError as e:

                pass
        self.check_for_packets()

    def unhandled_input(self, k):
        # exit on esc
        if k in ['esc'] and not self.details_showed:
            raise urwid.ExitMainLoop()
        if k == 'tab':
            if self.focus:
                self.view.original_widget.set_focus("footer")
            else:
                self.view.original_widget.set_focus("body")
            self.focus = not self.focus
        if k == 'esc':
            self.reset_layout()
            self.details_showed = False
        # enter pressed on list
        if k == 'enter':
            if self.focus:
                self.details_showed = True
                index = self.listbox.content.get_focus()[1]
                data_index = int(self.listbox.content[index].base_widget.get_text()[0][:7]) - 1
                self.popup(self.listbox.data[data_index].get_description())
            # enter pressed on filter box
            else:
                self.listbox.filter_list(self.filter.get_edit_text())

    def popup(self, text):
        # Header
        header_text = urwid.Text(('banner', 'Packet Details'), align='left')
        header = urwid.AttrMap(header_text, 'banner')

        # Body
        content = urwid.SimpleListWalker([
            urwid.AttrMap(w, None, 'reveal focus1') for w in text])

        listbox = urwid.LineBox(urwid.ListBox(content))

        # Layout
        layout = urwid.Frame(
            listbox,
            header=header,
            focus_part='body'
        )

        w = urwid.Overlay(
            urwid.LineBox(layout),
            self.view,
            align='center',
            width=('relative', 75),
            valign='middle',
            height=('relative', 80)
        )
        self.loop.widget = w

    def reset_layout(self, thing=None):
        '''
        Resets the console UI to the default layout
        '''

        self.loop.widget = self.view
        self.loop.draw_screen()


if __name__ == "__main__":
    WireDolphin().main()
