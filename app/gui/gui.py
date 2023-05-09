from .settings import settings_json
from .pattern import TextGrid
from .menu import Test
from .models import Status
from .utils import popup, popup_confirm
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from app.io.os import isRaspberry
from app.audio.audio import AudioManager
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

Window.show_cursor = not isRaspberry


class Status(BoxLayout):
    data = ObjectProperty()
    test = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {'File': 'noname.zip', 'BPM': 120}
        for key, value in self.data.items():
            label = Label(text=f'{key}: {value}', color='grey')
            self.add_widget(label)
        self.label = Label(text=self.test, color='grey')
        self.add_widget(self.label)


class Content(BoxLayout):
    pass


class Screen(BoxLayout):
    status = ObjectProperty()
    content = ObjectProperty()

    def on_enter(self):
        print('SCREEN on enter ', self.root.ids)


class TrackerApp(App):
    def add_engine(self, audio):
        self.audio = audio

    def build(self):
        self.title = 'ZynTracker'
        Window.bind(on_request_close=self.on_request_close)
        self.scale = 2
        self.use_kivy_settings = False
        self.settings_opened = False
        self.settings_cls = SettingsWithSidebar
        self.audio.initialize()
        self.seq = self.audio.seq
        self.audio.start()
        return Screen()

    def open_my_settings(self, button):
        self.settings_opened = True
        self.open_settings()

    def build_config(self, config):
        config.setdefaults('appearance', {'fullscreen': 0})
        config.setdefaults('network', {'serverip': 'http://192.168.1.1'})
        config.setdefaults('MIDI', {'looperbasenote': 64, 'switch': 0})
        config.setdefaults(
            'storage', {'userdir': 'application', 'customdir': ''})

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=settings_json)
        settings.bind(on_close=self.on_settings_close)

    def on_enter(self):
        print('ON ENTER ', self.root.ids)

    def on_start(self):
        print('on_start ', self.root.ids)
        # print('on_start ', self.screen.ids)
        if hasattr(self, 'audio'):
            if not self.audio.is_jack_running:
                popup('Warning',
                      'Jack server is not running.\n' +
                      'Please run it manually or configure it to \n' +
                      'start automatically at startup.')

            if not audio.is_running('linuxsampler'):
                popup('Warning',
                      'Linuxsampler is not running.\n' +
                      'Please install it / compile it from source.')
        else:
            popup('Error',
                  'AudioManager is not running.\n' +
                  'App won\'t work properly.')

    def close_settings(self, settings=None):
        if self.settings_opened:
            self.settings_opened = False
            self.on_settings_close()
        super().close_settings(settings)

    def on_settings_close(self, *args):
        pass
        # app = App.get_running_app()
        # print(self.root.ids)
        # self.tab_panel.switch_to(self.home_tab)
        # popup('Closed', 'Settings closed!')

    def on_request_close(self, *source):
        popup_confirm(
            on_yes=self.exit, params=('msg'))
        return True

    def exit(self):
        self.stop()

    def on_stop(self):
        # print('Stopping...')
        Config.write()


audio = AudioManager(init_delay=0.2, verbose=False)
app = TrackerApp()
app.add_engine(audio)
app.run()
audio.stop()
