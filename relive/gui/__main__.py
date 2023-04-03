
import sys
# import signal
import io
from .gui import ReliveApp
from relive.audio.sequencer import Sequencer
from relive.audio.service import AudioBackend


def custom_except_hook(exctype, value, traceback):
    print(sys.stdout.getvalue(), file=sys.__stdout__)
    print(sys.stderr.getvalue(), file=sys.__stderr__)
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
    sys.__excepthook__(exctype, value, traceback)


sys.excepthook = custom_except_hook  # noqa


def main():
    audio = AudioBackend(init_delay=0.2, verbose=False)
    seq = Sequencer()
    GUIapp = ReliveApp()
    GUIapp.add_engine(audio)
    GUIapp.run()
    seq.destroy()
    audio.disconnect_all()
    audio.stop_engines()

if __name__ == "__main__":
    main()
