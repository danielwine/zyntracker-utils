
import curses
import relive.cli.colors as CLR
import logging
import time

logger = logging.getLogger()


class Screen:
    def __init__(self, screen) -> None:
        self.scr = screen
        self.scr.keypad(1)
        self.scr.notimeout(True)
        self.init_colors()

    def init_colors(self):
        CLR.set_colors()


class WindowManager:
    def __init__(self):
        self.maxy = curses.LINES - 1
        self.maxx = curses.COLS - 1

    def _update(self, dct):
        self.__dict__.update(dct)

    def add(self, **kwargs):
        for category in kwargs.keys():
            if category == 'standard':
                cls = Window
            elif category == 'message':
                cls = MessageWindow
            elif category == 'data':
                cls = DataWindow
            elif category == 'pattern':
                cls = PatternWindow
            for window_name, params in kwargs[category].items():
                pn = 'height', 'width', 'begin_y', 'begin_x', 'clr'
                win = cls(
                    **{name: params[num] for num, name in enumerate(pn)},
                    hide_empty=True if window_name == 'sequences' else False)
                self._update({window_name: win})

    def refresh_all(self):
        for name, object in self.__dict__.items():
            if hasattr(object, 'refresh'):
                object.get_data()
                object.refresh()


class Window:
    def __init__(
            self,  scrollable=False, **kwargs):
        self.win = curses.newwin(
            kwargs['height'], kwargs['width'],
            kwargs['begin_y'], kwargs['begin_x'])
        self.scrollable = scrollable
        if scrollable:
            # self.win.setscrreg(0, 1)
            self.win.scrollok(True)
            self.win.leaveok(True)
            self.win.idlok(True)
        self.set_background(kwargs['clr'])
        self.active_line = 0
        self.active_row = 0
        self.height = kwargs['height']
        self.clr = kwargs['clr']

    def set_background(self, color_pair):
        self.win.bkgd(' ', curses.color_pair(color_pair))

    def focus(self, row=0):
        self.win.move(0, row)
        self.win.refresh()

    def backspace(self):
        self.print(f'{self.active_line} {self.active_row -1}', end='')
        # self.win.move(self.active_line, self.active_row - 1)
        # self.write(' ')

    def clear(self):
        self.win.erase()
        self.active_line = 0
        self.active_row = 0
        self.win.refresh()

    def write(self, char):
        self.win.addch(char)
        self.active_row += 1
        self.win.refresh()

    def print(self, msg, end='\n', x=0, y=0,
              pad=None, pad_chr=None, clr=0):
        clr = self.clr if clr == 0 else clr
        msg = str(msg)
        if x == 0 and y == 0:
            y = self.active_line
            x = self.active_row
        if y < 0 or y > curses.LINES or x < 0 or x > curses.COLS:
            return
        if x + len(msg) > curses.COLS:
            s = msg[:curses.COLS - x]
        else:
            s = msg
            if pad:
                ch = pad_chr or " "
                if pad is True:
                    pad = curses.COLS  # pad to edge of screen
                    s += ch * (pad - x - len(msg))
                else:
                    # pad to given length (or screen width)
                    if x + pad > curses.COLS:
                        pad = curses.COLS - x
                    s += ch * (pad - len(msg))

        if not clr:
            clr = CLR.CLR_LOG1
        self.active_row += len(msg)
        maxy, maxx = self.win.getmaxyx()
        self.win.addstr(y, x, s, clr)
        if self.active_line + 1 == maxy and self.height > 1:
            if self.scrollable:
                self.win.scroll()
                self.active_row = 0
        elif end == '\n':
            self.active_line += 1
            self.active_row = 0
        self.win.refresh()


class MessageWindow(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, scrollable=True)


class DataWindow(Window):
    def __init__(self, vertical=True, hide_empty=False, **kwargs):
        super().__init__(**kwargs, scrollable=True)
        self.data = {}
        self.vertical = True if kwargs['height'] > 1 else False
        self.header = ''
        self.pending = False
        self.hide_empty = hide_empty
        self.cb_get_data = None

    def add_get_data_cb(self, object, namespace, method):
        self.cb_get_data = [object, namespace, method]

    def get_data(self):
        self.data = {}
        cb = self.cb_get_data
        if not cb:
            return False
        getter = cb[0]
        obj = getter()
        if cb and obj:
            if cb[1] == '':
                if hasattr(obj, cb[2]):
                    self.data = getattr(obj, cb[2])
            else:
                if hasattr(obj, cb[1]):
                    sub = getattr(obj, cb[1])
                    if hasattr(sub, cb[2]):
                        self.data = getattr(sub, cb[2])

    def refresh(self):
        self.clear()
        if self.header and self.vertical:
            self.print(self.header)
            self.print('')
        if self.data:
            for item in self.data.items():
                if not (item[1] == '' and self.hide_empty):
                    msg = f'{str(item[0])}: {str(item[1])}'
                    msg = msg if self.vertical else f' {msg} '
                    self.print(
                        msg, end='\n' if self.vertical else '')


class PatternWindow(DataWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.cb_line_renderer = None

    def add_line_renderer(self, cb):
        self.cb_line_renderer = cb

    def refresh(self):
        if not self.data or not self.cb_line_renderer:
            return
        self.clear()
        if type(self.data) is list:
            for step in self.data:
                if len(step) > 1:
                    repr = self.cb_line_renderer(step[1])
                else:
                    repr = ''
                self.print(f'[{step[0]}] {repr}')
