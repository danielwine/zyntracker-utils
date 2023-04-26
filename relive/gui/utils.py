from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

Builder.load_file("utils.kv")


class ConfirmLayout(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super().__init__(**kwargs)

    def on_answer(self, *args):
        pass


def popup(title, content):
    popup = Popup(
        title=title,
        content=Label(text=content),
        size_hint=(None, None), size=(400, 400))
    popup.open()


def popup_confirm(
        question='Are you sure?', on_yes=lambda x: x, params=[]):
    def _on_answer(instance, answer):
        if answer == 'yes':
            on_yes()
        popup.dismiss()

    layout = ConfirmLayout(text=question)
    layout.bind(on_answer=_on_answer)
    popup = Popup(title='Confirmation',
                  content=layout,
                  size_hint=(None, None), size=(400, 400))
    popup.open()
