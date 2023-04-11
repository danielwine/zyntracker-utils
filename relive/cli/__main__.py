import sys
import signal
import io
import curses
import relive.config as cfg
from relive.cli.colors import Col
from .tui import ctrl_c_handler


def custom_except_hook(exctype, value, traceback):
    print(
        f"\n{Col.RED}ERROR{Col.RESET} occured during executing zyntracker.",
        end='')
    print(sys.stdout.getvalue(), file=sys.__stdout__)
    print(sys.stderr.getvalue(), file=sys.__stderr__)
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
    sys.__excepthook__(exctype, value, traceback)


sys.excepthook = custom_except_hook  # noqa


def main():
    if '--simple' in sys.argv:
        from .cli import CLIApp
        # sys.stdout = sys.__stdout__
        # sys.stderr = sys.__stderr__
        debug = cfg.debug_mode
        if 'debug' in sys.argv:
            debug = True
        cli = CLIApp(debug=debug)
        cli.start()
    else:
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        from .tui import TUIApp
        signal.signal(signal.SIGINT, ctrl_c_handler)
        curses.wrapper(TUIApp)
        curses.endwin()


if __name__ == "__main__":
    main()
