
import sys
# import signal
import io
# import curses

from .cli import CLI

sys.stdout = io.StringIO()
sys.stderr = io.StringIO()


def custom_except_hook(exctype, value, traceback):
    print(sys.stdout.getvalue(), file=sys.__stdout__)
    print(sys.stderr.getvalue(), file=sys.__stderr__)
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
    sys.__excepthook__(exctype, value, traceback)


sys.excepthook = custom_except_hook  # noqa


def main():
    # config = Configuration.get()
    if '--pretty' in sys.argv:
        pass
        # signal.signal(signal.SIGINT, ctrl_c_handler)
        # curses.wrapper(gui_main)
        # curses.endwin()
    else:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        cli = CLI()
        cli.start()
        cli.stop()


if __name__ == "__main__":
    main()
