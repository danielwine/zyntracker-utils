from time import sleep
from jack import JackError
from relive.io.logger import LoggerFactory, format
import relive.io.process as proc
from .engines import engines, use_linuxsampler
from .nodes import *
from .sequencer import Sequencer
from relive.config import autorun_jack
from relive.audio.sampler import LinuxSampler
from relive.res.presets import default_presets
from relive.config import PATH_SAMPLES


class Instrument:
    def __init__(self) -> None:
        ls_chan_info = {}

    def __str__(self) -> str:
        return f'{self.ls_chan_info}'


class AudioBackend():
    engines = {}
    client_name = 'zynseq'
    service_names = ['jackd', 'jalv']
    services = {}
    midiin = None
    client = None
    first_run = True
    sequencer = None
    sampler = None
    systemout = JackSystemOutNode('system')

    def __init__(self, init_delay=0.1, verbose=False, debug=False):
        self.verbose = verbose
        self.delay = init_delay
        self.debug = debug

    def get_logger(self):
        self.logger = LoggerFactory(__name__)

    def check_services(self):
        self.context = proc.get_context()
        for service in self.service_names:
            ret, err = proc.get_process_id(service)
            self.services[service] = ret.split('\n'), err
            if self.verbose:
                self.logger.info(format(
                    f'{service}: {self.is_online(service)}'))
        if self.is_running('jalv') and (
                self.first_run and not self.context['zynthian']):
            code = self.services['jalv'][0]
            if self.verbose:
                self.logger.info(format(f'Jalv is killed.'))
            proc.kill(code)
        self.first_run = False

    def is_running(self, name):
        if name in self.services:
            return True if len(self.services[name][0]) > 0 else False

    def is_online(self, name):
        return "OK" if self.is_running(name) else "OFF"

    @property
    def audio_status(self):
        status = {}
        for key in self.services:
            status[key] = self.is_online(key)
        status['audio'] = self.context['audio']
        return status

    def load_samples(self):
        self.instruments = []
        for instrument_nr in range(len(default_presets)):
            engine = 'sfz'
            font = default_presets[instrument_nr]
            instrument = Instrument()
            self.sampler.ls_add_channel(instrument)
            fpath = f'{PATH_SAMPLES}{engine}/{font}'
            # logger.info(fpath)
            self.sampler.ls_set_preset(instrument, 'sfz', fpath)
            self.instruments.append(instrument)
            # logger.info(instrument)

    def start_engines(self):
        if self.context['zynthian']:
            return
        self.logger.info(format('Initializing engines...'))
        if not use_linuxsampler:
            for engine_id, engine in engines.items():
                self.engines[engine_id] = JackPluginNode(
                    engine['name'], engine_id, engine['uri'],
                    debug=self.debug)
                self.engines[engine_id].launch()
                sleep(self.delay)
        else:
            self.engines[0] = JackSamplerNode(
                'LinuxSampler', 'linuxsampler')
            self.engines[0].launch()
            sleep(self.delay)
            self.sampler = LinuxSampler()
            sleep(self.delay)
            self.load_samples()

    def stop_engines(self):
        if self.context['zynthian']:
            return
        self.logger.info(format('  stopping engines...'))
        for engine in self.engines.values():
            print(engine.name)
            engine.process.terminate()

    def shutdown_client(self):
        self.logger.info(format('  deactivating client...'))
        self.client.deactivate()
        self.client.close()

    def connect_all(self):
        if self.debug:
            stdout.unmute()
        try:
            self.systemout.plug(self.sequencer, self.client)
            for engine_id, engine in self.engines.items():
                self.systemout.plug(self.engines[engine_id], self.client)
                self.engines[engine_id].plug(self.sequencer, self.client)
        except JackError as e:
            self.logger.info(format(f'JackError: {e}'))
            return
        self.logger.info(format('Connections established'))

    def get_all_connections(self):
        connections = []
        ports_list = self.client.get_ports()
        for port in ports_list:
            cons = self.client.get_all_connections(port)
            if cons:
                # print(port, cons)
                connections.append((port, cons))
        return connections

    def disconnect_all(self):
        for pair in self.get_all_connections():
            for port in pair[1]:
                print(pair[0], port)
                self.client.disconnect(pair[0], port)


class AudioManager(AudioBackend):
    def __init__(self, init_delay=0.1, verbose=False, debug=False):
        super().__init__(init_delay, verbose, debug)

    def newline(self):
        if self.verbose:
            print()

    def initialize(self):
        self.newline()
        self.get_logger()
        self.check_services()
        self.is_jack_running = self.is_running('jackd')
        if not self.is_jack_running:
            if not autorun_jack:
                self.logger.warning(
                    'zynseq will not be able to access jack server.')
            else:
                self.start_jack()
        self.newline()
        self.sequencer = JackSequencerNode(
            self.client_name, self.client_name)
        self.seq = Sequencer()
        if not self.context['path_lib']:
            stdout.unmute()
            self.logger.error('Missing zynseq library.')
            self.stop()
            exit()

    def start(self):
        if not self.debug:
            stdout.mute()
        self.seq.initialize(self.context['path_lib'])
        if self.is_jack_running:
            stdout.unmute()
            self.start_engines()
        stdout.mute()
        self.client = self.sequencer.launch()
        self.newline()
        if self.is_jack_running:
            stdout.unmute()
            self.connect_all()
            stdout.mute()
            self.newline()
        if self.debug:
            self.seq.libseq.enableDebug(True)
        if not self.is_jack_running:
            sleep(2)
        stdout.unmute()

    def stop(self):
        self.logger.info(format('Shutting down...'))
        # self.disconnect_all()
        self.seq.transport_stop(self.client_name)
        self.stop_engines()
        self.shutdown_client()
        # self.seq.destroy()
        sleep(0.5)


stdout = proc.StdOut()
