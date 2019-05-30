import urwid
import ethernet
from list_box_item import ListBoxItem


class PacketListBox(urwid.ListBox):

    def __init__(self):

        self.criteria = []
        self.data = []
        self.widgets = []
        self.content = urwid.SimpleListWalker(self.widgets)
        urwid.ListBox.__init__(self, self.content)
        self.is_searching = False
        self.counter = 0
        self.moved = False
        self.is_filtered = False

    def keypress(self, size, key):
        if key in ['s', 'S']:
            self.is_searching = not self.is_searching
            if self.is_searching:
                self.moved = False
            return
        elif key == 'e':
            self.update_list(last_position=True)
        elif key in ['up', 'down']:
            self.moved = True
        urwid.ListBox.keypress(self, size, key)
        return key

    def update_list(self, reset_position=False, last_position = False):
        last_focus = self.content.get_focus()[1]
        self.content = urwid.SimpleListWalker(self.widgets)
        if last_position:
            self.content.set_focus(len(self.widgets) - 1)
            self.moved = False
        elif not reset_position and self.content:
            if self.moved:
                self.content.set_focus(last_focus)
            else:
                self.content.set_focus(len(self.widgets) - 1)

        urwid.ListBox.__init__(self, self.content)

    def add_item(self, raw):
        self.counter += 1
        eth = ethernet.Ethernet(raw, self.counter)
        widget_to_add = ListBoxItem(eth.get_name()).get_widget()
        self.data.append(eth)
        if not self.is_filtered or self.filter_add(widget_to_add):
            self.widgets.append(widget_to_add)
        self.update_list()

    def filter_list(self, criteria):
        self.criteria = [f' {x} ' for x in criteria.split()]
        self.reset_list()
        if not self.criteria:
            self.is_filtered = False
            return
        self.is_filtered = True
        for singe_criteria in self.criteria:
            self.widgets = list(filter(lambda x: singe_criteria in x.base_widget.get_text()[0], self.widgets))
        self.update_list(reset_position=True)

    def filter_add(self, widget):
        for singe_criteria in self.criteria:
            if singe_criteria not in widget.base_widget.get_text()[0]:
                return False
        return True

    def reset_list(self):
        self.widgets.clear()
        for packet in self.data:
            self.widgets.append(ListBoxItem(packet.get_name()).get_widget())
        self.update_list(reset_position=True)
