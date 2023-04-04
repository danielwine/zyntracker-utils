
import sys
# import signal
import io
from .gui import ReliveApp
from relive.audio.sequencer import Sequencer
from relive.audio.service import AudioBackend


def main():
    audio = AudioBackend(init_delay=0.2, verbose=False)
    # seq = Sequencer()
    GUIapp = ReliveApp()
    GUIapp.add_engine(audio)
    GUIapp.run()
    # seq.destroy()
    # audio.disconnect_all()
    # audio.stop_engines()

if __name__ == "__main__":
    main()
