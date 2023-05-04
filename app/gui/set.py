from app.config import PATH_DATA
from app.io.process import get_files
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

Builder.load_file("set.kv")


class Set(GridLayout):
    def __init__(self, **kwargs):
        self.cols = 4
        super().__init__(**kwargs)
        self.get_data()
        self.add_button_group()

    def shorten_item(self, item):
        name = item
        if len(item) > 4 and item[:3].isnumeric() and item[3] == '-':
            name = item[4:]
        name = name.split('.')[0]
        return name if len(name) < 15 else name[:14] + '\n' + name[14:]
        # return name if len(name) < 10 else name[:10] + '..'

    def add_button_group(self):
        data = self.files['zss'] + self.files['xrns']
        for pad_number in range(20):
            item = data[pad_number] if pad_number < len(data) else None
            if item:
                button = Button(text=self.shorten_item(item))
            else:
                button = Button(text='?')

            self.add_widget(button)

    def get_data(self):
        self.files = {}
        for item in ['zss', 'xrns']:
            self.files[item] = get_files(f'{PATH_DATA}/{item}', item)
