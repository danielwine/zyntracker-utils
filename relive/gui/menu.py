from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from .set import Set
from .pad import Pad
from .control import Control
from .mixer import Mixer

Builder.load_file("menu.kv")


class Test(TabbedPanel):
    tab_panel = ObjectProperty(None)
    home_tab = ObjectProperty(None)
    
    def on_close_settings(self, settings):
        pass
