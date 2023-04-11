
import curses
import relive.cli.colors as CLR


class Screen:
    def __init__(self, screen) -> None:
        self.scr = screen
        self.scr.keypad(1)
        self.scr.notimeout(True)
        self.init_colors()

    def init_colors(self):
        CLR.set_colors()


class Window:
    def __init__(self, height, width, begin_y, begin_x, clr) -> None:
        self.win = curses.newwin(height, width, begin_y, begin_x)
        self.set_background(clr)
        self.active_line = 0
        self.active_row = 0
        self.clr = clr

    def set_background(self, color_pair):
        self.win.bkgd(' ', curses.color_pair(color_pair))

    def clear(self):
        self.win.clrtobot()
        self.active_line = 0
        self.active_row = 0

    def print(self, msg, end='\n', x=0, y=0, pad=None, pad_chr=None, clr=0):
        clr = self.clr if clr == 0 else clr
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
        if end == '\n':
            self.active_line += 1
            self.active_row = 0
        self.win.addstr(y, x, s, clr)
        self.win.refresh()
