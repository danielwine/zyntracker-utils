import logging
from .repl import REPL
from app.audio.audio import AudioManager
from app.shared.xrns import XRNS
from app.cli.messages import MSG_HEADER, MSG_USAGE

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


class CLIApp(REPL):
    def __init__(self, debug=True) -> None:
        super().__init__()
        self.debug = debug
        self.xrns = XRNS()
        print(MSG_HEADER)
        print(MSG_USAGE)
        if self.debug:
            print('DEBUG mode on.')

    def start(self):
        self.audio = AudioManager(
            init_delay=0.2, verbose=True, debug=self.debug)
        self.audio.initialize()
        self.audio.start()
        self.set_dir(self.audio.context['path_snapshot'],
                     self.audio.context['path_xrns'])
        self.loop()

    def loop(self):
        quit = False
        while not quit:
            res = input(
                f'b{self.audio.seq.bank:02d}p{self.audio.seq.pattern.id:02d}> ')
            res = res.strip()
            if res == '':
                res = prev_res
            else:
                prev_res = res
            if not self.evaluate(res):
                quit = True
        self.stop()

    def stop(self):
        self.audio.stop()
