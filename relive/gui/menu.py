from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from .pad import Pad
from .mixer import Mixer

Builder.load_file("menu.kv")


class Test(TabbedPanel):
    pass
