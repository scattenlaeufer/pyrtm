#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class MainBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        start_layout = StartLayout()
        self.add_widget(start_layout)


class StartLayout(GridLayout):
    def __init__(self, **kwargs):
        super(StartLayout, self).__init__(**kwargs)


class RogueTraderApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    RogueTraderApp().run()
