from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.core.window import Window


class TextGrid(GridLayout):
    def __init__(self, **kwargs):
        super(TextGrid, self).__init__(**kwargs)
        self.cols = 4
        self.rows = 20
        self.padding = ['50dp', '3dp']
        # self.bind(padding=self.setter('10dp'))
        for i in range(80):
            label = Label(text=str(i), font_size="13sp")
            self.COLOR_INITIAL = (0.5, 0.5, 0.5, 1)
            label.color = self.COLOR_INITIAL
            label.bind(size=label.setter('text_size'))
            self.add_widget(label)
        self.selected_label = None
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.selected_col = 0
        self.selected_row = 0
        self.select_label()
        Logger.info(str(self.selected_label.text))

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        Logger.info(f'KEYDOWN {text} - {keycode}')
        code, key = keycode
        if self.selected_label is not None:
            if text:
                # Update the text of the selected label
                self.selected_label.text = text
            elif keycode[0] == 8:
                # Delete the text of the selected label
                self.selected_label.text = ""
            elif key == 'up' and self.selected_row > 0:
                # Move up one row
                self.selected_row -= 1
                self.select_label()
            elif key == 'down' and  self.selected_row < self.rows - 1:
                # Move down one row
                self.selected_row += 1
                self.select_label()
            elif key == 'right' and self.selected_col > 0:
                # Move left one column
                self.selected_col -= 1
                self.select_label()
            elif key == 'left' and self.selected_col < self.cols - 1:
                # Move right one column
                self.selected_col += 1
                self.select_label()

    def on_touch_down(self, touch):
        Logger.info('TOUCHDOWN')
        # Find the label that was clicked on and select it
        for widget in self.walk():
            if widget.collide_point(*touch.pos):
                self.selected_label = widget
                self.selected_col = self.children.index(widget) % self.cols
                self.selected_row = self.rows - 1 - \
                    self.children.index(widget) // self.cols
                break
        super(TextGrid, self).on_touch_down(touch)

    def select_label(self):
        # Deselect the current label
        if self.selected_label is not None:
            self.selected_label.color = self.COLOR_INITIAL
        # Select the new label
        index = (self.rows - 1 - self.selected_row) * \
            self.cols + self.selected_col
        print(index)
        self.selected_label = self.children[index]
        self.selected_label.color = (1, 255, 1, 1)

