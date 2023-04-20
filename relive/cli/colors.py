import curses


class Col:
    RESET = '\033[0m'
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    White = '\033[0;37m'


class BCol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def set_colors():
    global CLR_HEADING, CLR_FOOTER
    global CLR_CMDLINE, CLR_INPUT, CLR_LOG1, CLR_LOG2
    global CLR_LOG_DEBUG, CLR_LOG_ERROR, CLR_LOG_CMDMESSAGE

    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        bg = curses.COLOR_BLACK
        for i in range(1, curses.COLORS):
            curses.init_pair(i + 1, i, bg)
    
    curses.init_pair(1, 7, 0)
    curses.init_pair(2, 0, 7)
    curses.init_pair(3, 7, 0)
    curses.init_pair(4, 3, 0)
    curses.init_pair(5, 2, 0)
    curses.init_pair(6, 0, 1)

    curses.init_pair(10, 0, 2)
    curses.init_pair(11, 7, 1)

    # Colors (on black backgound):
    # 1 = white         5 = dk blue
    # 2 = dk red        6 = dk purple
    # 3 = dk green      7 = dk cyan
    # 4 = dk yellow     8 = lt gray
    CLR_LOG1 = curses.color_pair(3)
    CLR_LOG2 = curses.color_pair(6)
    CLR_LOG_DEBUG = curses.color_pair(4)
    CLR_LOG_ERROR = curses.color_pair(2)
    CLR_LOG_CMDMESSAGE = curses.color_pair(2)
    
