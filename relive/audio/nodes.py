from abc import abstractmethod
from jack import Client, JackOpenError
from relive.io.logger import LoggerFactory, format
from relive.io.process import launch_plugin

logger = LoggerFactory(__name__)


class JackBaseNode:
    def __init__(self, name='', inports=[], outports=[], debug=False) -> None:
        self.name = name
        self.inports = inports
        self.outports = outports
        self.debug = debug

    def launch(self):
        logger.info(format(f'  starting {self.id}'))

    def plug(self, Node, client):
        self._connect(Node, client.connect)

    def unplug(self, Node, client):
        self._connect(Node, client.disconnect)

    @abstractmethod
    def _connect(self, Node, action):
        pass


class JackMidiInputNode(JackBaseNode):
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        super().__init__(None, ['foo'])

    def plug(self):
        pass


class JackSequencerNode(JackBaseNode):
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        super().__init__(
            name,
            inports=['input'],
            outports=['output', 'metronome'])

    def launch(self):
        super().launch()
        try:
            self.client = Client(self.name)
            # self.client = jack.Client("test",no_start_server=True)
        except JackOpenError:
            logger.error("Cannot connect to jack server.")
            return
        # client.midi_inports.register('input')
        return self.client

    def _connect(self, Node, action):
        for inport in self.inports:
            if isinstance(Node, JackMidiInputNode):
                action(f'{Node.name}:{Node.outport[0]}',
                       f'{self.name}:{inport}')


class JackPluginNode(JackBaseNode):
    process: None

    def __init__(self, name, id, uri, debug=False) -> None:
        self.name = name
        self.id = id
        self.uri = uri
        super().__init__(
            name,
            inports=['lv2_events_in'],
            outports=['lv2_audio_out_1', 'lv2_audio_out_2'],
            debug=debug)

    def launch(self):
        super().launch()
        self.process = launch_plugin(self.uri, debug=self.debug)

    def _connect(self, Node, action):
        for inport in self.inports:
            if isinstance(Node, JackSequencerNode):
                action(f'{Node.name}:{Node.outports[0]}',
                       f'{self.name}:{inport}')


class JackSystemOutNode(JackBaseNode):
    def __init__(self, name) -> None:
        super().__init__(
            name,
            inports=['playback_1', 'playback_2'])

    def launch(self):
        pass

    def _connect(self, Node, action):
        for num in range(len(self.inports)):
            if isinstance(Node, JackPluginNode):
                action(f'{Node.name}:{Node.outports[num]}',
                       f'{self.name}:{self.inports[num]}')
            if isinstance(Node, JackSequencerNode):
                # self.client.connect(
                #   f"{name}:output", "ZynMidiRouter:step_in")
                action(f'{Node.name}:{Node.outports[1]}',
                       f'{self.name}:{self.inports[num]}')
