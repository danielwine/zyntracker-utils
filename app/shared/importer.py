import app.io.process as proc
from app.shared.xrns import XRNS
from lib.zynseq import zynseq


class Sequencer(zynseq.zynseq):
    def __init__(self):
        super().__init__()

    def init(self, path):
        self.initialize(path)


class App:
    def __init__(self) -> None:
        self.context = proc.get_context()
        self.seq = Sequencer()
        self.xrns = XRNS()

    def run(self):
        self.seq.init(self.context['path_lib'])
        self.xrns.load('test.xrns')
        print(self.xrns.project.info)


if __name__ == '__main__':
    app = App()
    app.run()
