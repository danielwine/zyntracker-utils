from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

Builder.load_file("pad.kv")


class Pad(GridLayout):
    def __init__(self, **kwargs):
        self.cols = 5
        super().__init__(**kwargs)
        for pad in range(25):
            button = Button(text='PAD')
            self.add_widget(button)
