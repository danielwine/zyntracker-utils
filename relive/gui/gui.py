from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.config import Config
from relive.config import isRaspberry
from kivy.core.window import Window
Window.show_cursor = not isRaspberry
Config.read('relive.ini')


class Screen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="ReLive GUI is running."))


class ReliveApp(App):
    def add_engine(self, audio):
        self.audio = audio

    def build(self):
        self.scale = 2
        # self.audio.check_services()
        # self.audio.start_engines()
        # self.audio.connect_all()
        return Screen()
