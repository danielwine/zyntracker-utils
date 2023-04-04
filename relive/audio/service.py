from time import sleep
from jack import JackError
from relive.io.logger import LoggerFactory
import relive.io.process as proc
from .engines import engines
from .nodes import *
from relive.config import debug_mode

logger, ln = LoggerFactory(__name__)


class AudioBackend():
    engines = {}
    service_names = ['jack', 'jalv']
    services = {}
    midiin = None
    client = None
    sequencer = JackSequencerNode('zynseq', 'zynseq')
    systemout = JackSystemOutNode('system')

    def __init__(self, init_delay=0.1, verbose=False):
        self.verbose = verbose
        self.delay = init_delay

    def check_services(self):
        for service in self.service_names:
            self.services[service] = proc.launch_and_get_code(service)
            logger.info(
                f'{ln}{service}: '
                f'{"online" if self.is_running(service) else "offline"}')
        if self.is_running('jalv'):
            logger.info(f'{ln}Jalv is killed.')
            proc.kill(self.services['jalv'][0])

    def is_running(self, name):
        if name in self.services:
            return True if len(self.services[name][0]) > 0 else False

    def start_engines(self):
        logger.info(f'{ln}Initializing engines...')
        for engine_id, engine in engines.items():
            self.engines[engine_id] = JackPluginNode(
                engine['name'], engine_id, engine['uri'])
            self.engines[engine_id].launch()
            sleep(self.delay)

    def stop_engines(self):
        logger.info(f'{ln}Shutting down...')
        for engine in self.engines.values():
            engine.process.terminate()

    def connect_all(self):
        if not debug_mode:
            stdout.unmute()
        self.client = self.sequencer.launch()
        if not debug_mode:
            stdout.unmute()
        try:
            self.systemout.plug(self.sequencer, self.client)
            for engine_id, engine in self.engines.items():
                self.systemout.plug(self.engines[engine_id], self.client)
                self.engines[engine_id].plug(self.sequencer, self.client)
        except JackError as e:
            logger.error(f'{ln}JackError: {e}')
            return
        logger.info(f'{ln}Connections established')

    def disconnect_all(self):
        pass


stdout = proc.StdOut()
