#!/usr/bin/env python3

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import os

# from jnius import autoclass

characteristics = {
    "ws": "Weapon Skill",
    "bs": "Balistic Skill",
    "s": "Strength",
    "t": "Toughness",
    "ag": "Agility",
    "int": "Intelligence",
    "per": "Perception",
    "wp": "Willpower",
    "fel": "Fellowship",
}


default_character = {
    "name": "Siegmund Falckenhain",
    "kia": False,
    "player": "Björn Guth",
    "career_path": "Rogue Trader",
    "home_world": "Noble Born",
    "motivation": "Prestige",
    "dascription": "blubb",
    "exp": [7000, 0],
    "characteristics": {
        "ws": [48, 2],
        "bs": [40, 0],
        "s": [35, 0],
        "t": [36, 0],
        "ag": [43, 1],
        "int": [42, 0],
        "per": [43, 1],
        "wp": [30, 0],
        "fel": [60, 2],
    },
    "skills": {
        "awareness": "t",
        "ciphers": {
            "Roque Trader": "t",
        },
        "charm": "+10",
        "command": "+10",
        "commerce": "t",
        "common_lore": {
            "Imperium": "t",
            "Rogue Trader": "t",
        },
        "dodge": "t",
        "evaluate": "t",
        "inquiry": "t",
        "literacy": "+10",
        "pilot": {
            "Space Craft": "t",
        },
        "scholastic_lore": {
            "Astromancy": "t",
        },
        "secret_tongue": {
            "Rogue Trader": 't',
        },
        "speak_language": {
            "High Gothic": "+10",
            "Low Gothic": "t",
            "Trader Cant": "t",
        },
    },
    "talents": [
        "paranoia",
        ["enemy", "Ecchlesiachy"],
        "forsight",
        "decadence",
        "etiquette",
        ["peer", "Nobels", "Military", "Adminstratum"],
        ["talented", "Command"],
        ["pistol_weapon_training", "Universal"],
        ["melee_weapon_training", "Universal"],
        "air_of_authority",
        "ambidextrous",
        "renowned_warrant",
    ]
}


class MainBox(BoxLayout):

    data = {}

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        data_json = JsonStore(os.path.join("data/rogue_trader_data.json"))
        for key in data_json.keys():
            self.data[key] = data_json[key]
        self.character = default_character
        start_layout = StartLayout(self.data)
        self.ids["all_talents"].add_widget(start_layout)
        self.ids["blubb"].text = str(self.ids["skill_box"].parent.height)
        for key in characteristics.keys():
            self.ids[key].set_text(default_character["characteristics"][key])
        for key, skill in self.data["skills"].items():
            if skill["skill_group"]:
                if key in self.character['skills']:
                    for skill_group, status in self.character['skills'][key].items():
                        button = Button()
                        button.text = "{} ({})".format(skill['name'], skill_group)
                        self.ids['skill_box'].add_widget(button)
                else:
                    button = Button()
                    button.text = "{} ()".format(skill['name'])
                    self.ids['skill_box'].add_widget(button)
            else:
                button = Button()
                button.text = skill["name"]
                self.ids['skill_box'].add_widget(button)

    def characteristics_test(self, instance):
        InfoPopup("test", instance.text).open()


class StartLayout(GridLayout):
    def __init__(self, data, **kwargs):
        super(StartLayout, self).__init__(**kwargs)
        self.data = data
        for key, value in self.data["talents"].items():
            button = Button()
            button.text = value["name"]
            button.talent_key = key
            button.bind(on_press=self.give_talent_info)
            self.add_widget(button)

    def give_talent_info(self, instance):
        TalentInfoPopup(self.data["talents"][instance.talent_key])

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


class CharacteristicButton(Button):

    _text = ""
    value = 0

    # def __init__(self, short, characteristic, **kwargs):
    #     super(CharacteristicButton, self).__init__(**kwargs)
    #     self.text = "{}\n{}\n{}\n●".format(characteristics[short], short.capitalize(), characteristic[0])
    #     self.font_name = "Body"
    #     print(self.text)
    #     print(self.font_name)

    def set_text(self, characteristic):
        self.value = characteristic[0]
        self.text = self._text.format(int(self.font_size*2), characteristic[0], characteristic[1])


class TalentInfoPopup(InfoPopup):
    def __init__(self, talent, **kwargs):

        prerequisits = []
        if len(talent["prerequisits"]["characteristics"]) > 0:
            for key, value in talent["prerequisits"]["characteristics"].items():
                prerequisits.append("{}: {}".format(characteristics[key], value))
        if len(talent["prerequisits"]["skills"]) > 0:
            for value in talent["prerequisits"]["skills"]:
                prerequisits.append(value)
        if len(talent["prerequisits"]["talents"]) > 0:
            for value in talent["prerequisits"]["talents"]:
                prerequisits.append(value)
        if len(talent["prerequisits"]["other"]) > 0:
            for value in talent["prerequisits"]["other"]:
                prerequisits.append(value)
        if len(prerequisits) == 0:
            prerequisits.append("None")

        talent_group = ""
        if talent["talent_group"]:
            talent_group = (
                "[b]Talent Groups[/b]: " + ", ".join(talent["talent_group"]) + "\n\n"
            )
        info_text = "{}\n\n[b]Prerequisits:[/b] {}\n\n{}{}".format(
            talent["short_text"], ", ".join(prerequisits), talent_group, talent["text"]
        )
        super(TalentInfoPopup, self).__init__(talent["name"], info_text, **kwargs)


class RogueTraderApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    RogueTraderApp().run()
