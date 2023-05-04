import time
from .logger import LoggerFactory
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from oscpy.parser import MidiTuple

logger, ln = LoggerFactory(__name__)


class OSCConnectionError(Exception):
    def __init__(self, address):
        self.SERVERERROR = 'OSC server cannot be reached'
        logger.error(f'{address} {self.SERVERERROR}')
        super().__init__(self.SERVERERROR)


class OSCController:
    def __init__(self):
        self.address = "localhost"
        self.port_midi = 8000
        self.prefix_midi = '/MIDI'
        self.midi_client = OSCClient(self.address, self.port_midi)
        self.cmdNoteOn = 0x90
        self.cmdNoteOff = 0x80
        self.connected = None

    def init(self):
        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=12102,
            default=True,
        )
        server.bind(b'/message', self.display_message)
        try:
            # raise FileNotFoundError
            logger.info(f'{ln}sending data to {self.address}...')
            self.midi_client.send_message(b"/midi", [])
        except:
            self.connected = False
            raise OSCConnectionError(self.address)

    def send_ctrl_note(self, note):
        logger.info(f'{ln}sending Control note message "{id}"')
        self.midi_client.send_message(
            b"/midi", [MidiTuple(100, note, 0x9F, 0)])

    def send_note(self, vel, note, state='on', channel=0):
        state = self.cmdNoteOn if state else self.cmdNoteOff
        logger.info(f'{ln}sending midi note {note} {vel} {state} {channel}')
        self.midi_client.send_message(
            b"/midi", [MidiTuple(vel, note, state, channel)])

    def send(self, typ, msg):
        if typ == 'ctrlnote':
            try:
                self.send_ctrl_note(msg)
            except:
                raise OSCConnectionError(self.address)
        if typ == 'note':
            try:
                self.send_note(msg[0], msg[1], state=msg[2], channel=msg[3])
            except:
                raise OSCConnectionError(self.address)

    def test_midi(self):
        logger.info(f'{ln}Testing MIDI (note on / note off)')
        self.send_note(100, 63)
        time.sleep(1)
        self.send_note(100, 63, state='off')

    def display_message(self, message):
        if self.root:
            self.root.ids.label.text += '{}\n'.format(message.decode('utf8'))
        else:
            logger.info(f"{ln}incoming OSC: {message.decode('utf8')}")
