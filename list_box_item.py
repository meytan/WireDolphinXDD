import urwid


class SelectableText(urwid.Text):

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class ListBoxItem(urwid.Widget):
    def __init__(self, value):
        self.name = self._set_name(value)
        self.data = value

    def selectable(self):
        return True

    def _set_name(self, name):
        return name

    def get_widget(self):
        return urwid.AttrMap(SelectableText(self.name,), '', 'reveal focus')


