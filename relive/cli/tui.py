import logging
import curses
from sys import stdout
import relive.cli.colors as CLR
from relive.io.logger import CursesHandler
from relive.shared.tracker import Note
from .screen import Screen, WindowManager
from .layout import get_layout
from .repl import REPL
from relive.audio.service import AudioManager

messageWindow = None
ctrl_c_was_pressed = False
logger = logging.getLogger()


def print(message):
    if hasattr(messageWindow, 'print'):
        messageWindow.print(message)


def ctrl_c_handler(signum, frame):
    global ctrl_c_was_pressed
    ctrl_c_was_pressed = True


def ctrl_c_pressed():
    global ctrl_c_was_pressed
    if ctrl_c_was_pressed:
        ctrl_c_was_pressed = False
        return True
    else:
        return False


class TUIApp(REPL):
    def __init__(self, stdscr, debug=False) -> None:
        super().__init__()
        self.debug = debug
        self.screen = Screen(stdscr)
        self.screen.init_colors()
        self.initialize_screen()
        self.print_help()
        self.print('')
        if self.debug:
            print('DEBUG mode on.')
        self.start()

    def setup_logging(self, message_window):
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                logging.StreamHandler(),
                CursesHandler(message_window)
            ]
        )

    def register_callbacks(self):
        global messageWindow
        messageWindow = self.win.messages
        self.set_print_callback(messageWindow.print)
        self.register_event('file_loaded', self.win.refresh_all)


    def add_data_cb(self, win, namespace, method):
        def get_seq():
            if hasattr(self, 'audio'):
                if hasattr(self.audio, 'seq'):
                        return self.audio.seq
            return False
        win.add_get_data_cb(get_seq, namespace, method)

    def initialize_windows(self):
        self.win.header.print(self.MSG_HEADER)
        self.win.footer.print('ESC Window  F1 Help')
        self.win.console.print('>', end='')
        self.win.sequences.header = 'BANK'
        self.win.window2.header = 'PATTERN'
        self.add_data_cb(self.win.status, '', 'statistics')
        self.add_data_cb(self.win.sequences, '', 'sequences_in_bank')
        self.add_data_cb(self.win.window2, 'pattern', 'info')
        self.add_data_cb(self.win.pattern, 'pattern', 'notes')

    def initialize_renderers(self):
        self.win.pattern.add_line_renderer(Note.get_string)

    def initialize_screen(self):
        self.win = WindowManager()
        self.win.add(**get_layout(self.win.maxx, self.win.maxy))
        self.initialize_windows()
        self.setup_logging(self.win.messages)
        self.register_callbacks()

    def print_help(self):
        print('Basic commands (press F1 for more):')
        self.show_help(basic=True)

    def draw_status(self):
        self.statusbar1.clear()
        self.statusbar2.clear()
        for item in self.audio.seq.statistics.items():
            self.statusbar1.print(
                f' {str(item[0])}: {str(item[1])} ', end='', clr=3)
        status2 = ''
        for key in self.audio.services:
            status2 += f'{key}: {self.audio.is_online(key)}' + '   '
        status2 += f'audio: {self.audio.context["audio"]}'
        self.statusbar2.print(status2)

    def get_input(self):
        self.win.console.print(' ')

    def start(self):
        self.audio = AudioManager(
            init_delay=0.2, verbose=False, debug=self.debug)
        self.audio.initialize()
        self.set_dir(self.audio.context['path_snapshot'])

        self.win.refresh_all()
        self.audio.start()
        self.initialize_renderers()
        self.win.refresh_all()
        self.get_input()
        self.loop()

    def loop(self):
        self.screen.scr.nodelay(True)
        try:
            while True:
                c = 0
                c = self.win.console.win.getch()
                code = 0
                try:
                    if ctrl_c_pressed():
                        c = 24
                    else:
                        # Don't block, this allows us to refr the scr while
                        # waiting on initial messagebus connection, etc
                        # scr.timeout(1)
                        # c = scr.get_wch()
                        #    # unicode char or int for special keys
                        # if c == -1:
                        # continue
                        pass
                except curses.error as e:
                    logger.error(f'Error: {e}')

                if isinstance(c, int):
                    code = c
                else:
                    code = ord(c)

                # scr.timeout(-1)   # resume blocking
                if code == 27:
                    # Hitting ESC twice clears the entry line
                    # self.messages.print('ESC')
                    self.win.pattern.focus()
                    hist_idx = -1
                    line = ""
                elif c == curses.KEY_RESIZE:
                    # Generated by Curses when window/screen
                    # has been resized
                    y, x = self.screen.scr.getmaxyx()
                    curses.resizeterm(y, x)
                    c = self.screen.scr.get_wch()
                elif code == 10:
                    self.win.messages.print('')
                    res = self.win.console.win.instr(0, 2).decode('utf-8')
                    self.win.console.clear()
                    if not self.evaluate(res):
                        break
                    self.win.console.focus(2)
                elif code == 24:
                    break
                elif code == 127:
                    self.console.backspace()
                elif (code >= 48 and code <= 57) or (
                        (code >= 97 and code <= 122)) or code == 32:
                    self.win.console.write(chr(code))
                elif code:
                    self.win.messages.print(str(code))

        finally:
            self.screen.scr.erase()
            self.screen.scr.refresh()
            messageWindow = None
            self.screen.scr = None

    def stop(self):
        self.audio.stop()
        curses.endwin()
