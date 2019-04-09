#!/usr/bin/env python3

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
# from jnius import autoclass
import os


class MainBox(BoxLayout):

    data = {}

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        data_json = JsonStore(
            os.path.join("data/rogue_trader_data.json")
        )
        for key in data_json.keys():
            self.data[key] = data_json[key]
        start_layout = StartLayout(self.data)
        self.ids['all_talents'].add_widget(start_layout)
        self.ids['blubb'].text = App.get_running_app().user_data_dir


class StartLayout(GridLayout):
    def __init__(self, data, **kwargs):
        super(StartLayout, self).__init__(**kwargs)
        self.data = data
        for key, value in self.data['talents'].items():
            button = Button()
            button.text = value['name']
            button.talent_key = key
            button.bind(on_press=self.give_talent_info)
            self.add_widget(button)

    def give_talent_info(self, instance):
        TalentInfoPopup(self.data['talents'][instance.talent_key])

    def info_test(self):
        InfoPopup(
            "Test",
            "Das ist [b]fetter[/b] Text\nUnd das ist [color=#00ff00]grün[/color]\nUnd das ist [color=ff0000]rot[/color]",
        )
        TalentInfoPopup(self.data["talents"]["air_of_authority"])


class InfoPopup(Popup):
    def __init__(self, title, info, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title = title
        self.ids["label_info"].text = info
        self.open()


class TalentInfoPopup(InfoPopup):
    def __init__(self, talent, **kwargs):

        prerequisits = []
        if len(talent['prerequisits']['characteristics']) > 0:
            for key, value in talent['prerequisits']['characteristics'].items():
                prerequisits.append("{}: {}".format(key, value))
        if len(talent['prerequisits']['skills']) > 0:
            for value in talent['prerequisits']['skills']:
                prerequisits.append(value)
        if len(talent['prerequisits']['talents']) > 0:
            for value in talent['prerequisits']['talents']:
                prerequisits.append(value)
        if len(talent['prerequisits']['other']) > 0:
            for value in talent['prerequisits']['other']:
                prerequisits.append(value)
        if len(prerequisits) == 0:
            prerequisits.append("None")

        talent_group = ""
        if talent['talent_group']:
            talent_group = "[b]Talent Groups[/b]: " + ", ".join(talent['talent_group']) + "\n\n"
        info_text = "{}\n\n[b]Prerequisits:[/b] {}\n\n{}{}".format(talent['short_text'], ", ".join(prerequisits), talent_group, talent['text'])
        super(TalentInfoPopup, self).__init__(talent['name'], info_text, **kwargs)


class RogueTraderApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    RogueTraderApp().run()
