
import sys
# import signal
import io
from .gui import ReliveApp
from relive.audio.sequencer import Sequencer
from relive.audio.service import AudioManager


def main():
    audio = AudioManager(init_delay=0.2, verbose=False)
    GUIapp = ReliveApp()
    GUIapp.add_engine(audio)
    GUIapp.run()
    # audio.stop()

if __name__ == "__main__":
    main()
