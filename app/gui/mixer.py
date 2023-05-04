from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label


class Channel(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        super().__init__(**kwargs)
        slider = Slider()
        slider.orientation = 'vertical'
        self.add_widget(slider)
        self.add_widget(Label(text='01', size_hint_y='0.2'))


class Mixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        row = {}
        track_names = [
            'drum', 'bass', 'pad', 'lead', '', 'mast'
        ]
        for slider in range(11):
            channel = Channel()
            # slider = Slider()
            # slider.orientation = 'vertical'
            self.add_widget(channel)
        self.row = row
