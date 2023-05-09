import app.io.os as proc
from app.io.os import StdOut
from app.shared.xrns import XRNS
from app.audio.sequencer import Sequencer


class App:
    def __init__(self) -> None:
        self.stdout = StdOut()
        self.context = proc.get_context()
        self.seq = Sequencer()
        self.xrns = XRNS()

    def run(self):
        file = 'test.xrns'
        self.stdout.mute()
        self.seq.initialize(self.context['path_lib'], scan=False)
        self.xrns.load('test.xrns')
        self.seq.import_project(file, self.xrns.project)
        self.stdout.unmute()
        self.seq.save_file()


if __name__ == '__main__':
    app = App()
    app.run()
