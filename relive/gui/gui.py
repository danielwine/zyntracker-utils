from relive.audio.audio import AudioManager
from kivy.config import ConfigParser
from relive.config import isRaspberry
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.app import App
from kivy.core.window import Window
from .menu import Test
from .pad import Pad
from .pattern import TextGrid
from .settings import settings_json
from kivy.config import Config
Config.read('config.ini')
Window.show_cursor = not isRaspberry


class Status(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data = {'File': 'noname.zip', 'BPM': 120}
        for key, value in data.items():
            label = Label(text=f'{key}: {value}', color='grey')
            self.add_widget(label)


class Content(BoxLayout):
    pass


class Screen(BoxLayout):
    pass


class ReliveApp(App):
    def add_engine(self, audio):
        self.audio = audio

    def build(self):
        self.scale = 2
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        self.audio.initialize()
        self.seq = self.audio.seq
        self.audio.start()
        return Screen()

    def build_config(self, config):
        config.setdefaults('appearance', {'fullscreen': 0})
        config.setdefaults('network', {'serverip': 'http://192.168.1.1'})
        config.setdefaults('MIDI', {'looperbasenote': 64, 'switch': 0})
        config.setdefaults(
            'storage', {'userdir': 'application', 'customdir': ''})

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=settings_json)

    def on_stop(self):
        # print('Stopping...')
        Config.write()


audio = AudioManager(init_delay=0.2, verbose=False)
app = ReliveApp()
app.add_engine(audio)
app.run()
audio.stop()
