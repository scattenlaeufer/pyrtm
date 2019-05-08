#!/usr/bin/env python3

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, NumericProperty, OptionProperty
import os
import random

# from jnius import autoclass


test_difficulties = [
    ["Trivial", 60],
    ["Elementary", 50],
    ["Simple", 40],
    ["Easy", 30],
    ["Routine", 20],
    ["Ordinary", 10],
    ["Challenging", 0],
    ["Difficult", -10],
    ["Hard", -20],
    ["Very Hard", -30],
    ["Arduous", -40],
    ["Punishing", -50],
    ["Hellish", -60],
]

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
        "ciphers": {"Roque Trader": "t"},
        "charm": "+10",
        "command": "+10",
        "commerce": "t",
        "common_lore": {"Imperium": "t", "Rogue Trader": "t"},
        "dodge": "t",
        "evaluate": "t",
        "inquiry": "t",
        "literacy": "+10",
        "pilot": {"Space Craft": "t"},
        "scholastic_lore": {"Astromancy": "t"},
        "secret_tongue": {"Rogue Trader": "t"},
        "speak_language": {"High Gothic": "+10", "Low Gothic": "t", "Trader Cant": "t"},
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
    ],
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
        self.ids["skill_box"].height = 0
        bg = True
        self.skill_box_dict = {}
        for key, skill in self.data["skills"].items():
            if skill["skill_group"]:
                skill_group_box_dict = {}
                if key in self.character["skills"]:
                    for skill_group, status in self.character["skills"][key].items():
                        box = SkillBox(
                            skill,
                            self.data["characteristics"][skill["characteristic"]][
                                "short"
                            ],
                            self.character["characteristics"][skill["characteristic"]][
                                0
                            ],
                            status,
                            bg,
                            name="{} ({})".format(skill["name"], skill_group),
                        )
                        bg = not bg
                        self.ids["skill_box"].height += box.height
                        self.ids["skill_box"].add_widget(box)
                        skill_group_box_dict[skill_group] = box
                else:
                    box = SkillBox(
                        skill,
                        self.data["characteristics"][skill["characteristic"]]["short"],
                        self.character["characteristics"][skill["characteristic"]][0],
                        None,
                        bg,
                        name="{} ()".format(skill["name"]),
                    )
                    bg = not bg
                    self.ids["skill_box"].height += box.height
                    self.ids["skill_box"].add_widget(box)
                self.skill_box_dict[key] = skill_group_box_dict
            else:
                box = SkillBox(
                    skill,
                    self.data["characteristics"][skill["characteristic"]]["short"],
                    self.character["characteristics"][skill["characteristic"]][0],
                    self.character["skills"][key]
                    if key in self.character["skills"].keys()
                    else None,
                    bg,
                )
                bg = not bg
                self.ids["skill_box"].height += box.height
                self.ids["skill_box"].add_widget(box)
                self.skill_box_dict[key] = box

    def characteristics_test(self, instance):
        InfoPopup("test", instance.text).open()

    def skill_info(self, instance):
        SkillInfoPopup(self.data["skills"][instance.skill_key])


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


class CharacteristicButton(Button):

    _text = ""
    value = 0

    def set_text(self, characteristic):
        self.value = characteristic[0]
        self.text = self._text.format(
            int(self.font_size * 2), characteristic[0], characteristic[1]
        )


class SkillBox(BoxLayout):

    bg = BooleanProperty()
    skill_value = NumericProperty()

    def __init__(
        self,
        skill,
        characteristic,
        characteristic_value,
        status,
        bg,
        name=None,
        **kwargs
    ):
        super(SkillBox, self).__init__(**kwargs)
        self.bg = bg
        self.skill = skill
        if name:
            self.ids["button_info"].text = name
        else:
            self.ids["button_info"].text = skill["name"]
        self.ids["characteristic"].text = "({})".format(characteristic)
        if status:
            self.ids["status"].text = status.upper()
            if status == "t":
                self.skill_value = characteristic_value
            elif status == "+10":
                self.skill_value = characteristic_value + 10
            elif status == "+20":
                self.skill_value = characteristic_value + 20
        elif skill["basic"]:
            self.ids["status"].text = "B"
            self.skill_value = characteristic_value // 2
        else:
            self.ids["button_test"].disabled = True
            self.ids["button_test"].opacity = 0

    def skill_info(self):
        SkillInfoPopup(self.skill)

    def on_skill_value(self, instance, value):
        self.ids["button_test"].text = str(value)

    def do_test(self):
        TestPopup(self.ids["button_info"].text, self.skill_value)


class TestPopup(Popup):

    current_value = NumericProperty()
    success = OptionProperty("none", options=["none", "yes", "no"])

    def __init__(self, title, base_value, modifier=[], **kwargs):
        super(TestPopup, self).__init__(**kwargs)
        self.title = "{} Test".format(title)
        self.base_value = base_value
        self.difficulty = 0
        self.current_value = self.base_value
        self.modifier = modifier
        self.difficulty_dropdown = DropDown()
        for difficulty in test_difficulties:
            button = DropdownButton(*difficulty)
            button.bind(
                on_release=lambda btn: self.difficulty_dropdown.select([btn.text, btn.modifier])
            )
            self.difficulty_dropdown.add_widget(button)
        self.ids["button_difficulty"].bind(on_release=self.difficulty_dropdown.open)
        self.difficulty_dropdown.bind(on_select=self.set_difficulty)
        self.open()

    def set_difficulty(self, button, difficulty):
        self.ids["button_difficulty"].text = difficulty[0]
        self.difficulty = difficulty[1]
        self.modify_current_value()

    def modify_current_value(self):
        self.current_value = self.base_value + self.difficulty

    def roll_test(self):
        roll = random.randint(1,100)
        if roll <= self.current_value:
            self.success = "yes"
        else:
            self.success = "no"
        self.ids["label_result"].text = str(roll)
        degrees = abs(self.current_value-roll) // 10
        self.ids["label_degrees"].text = "{} {}".format(degrees, "Degree" if degrees==1 else "Degrees")

    def on_current_value(self, instance, value):
        self.ids["label_current_value"].text = str(value)


class InfoPopup(Popup):
    def __init__(self, title, info, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title = title
        self.ids["label_info"].text = info
        self.open()


class SkillInfoPopup(InfoPopup):
    def __init__(self, skill, **kwargs):
        info_text = []
        if skill["basic"]:
            basic_list = ["Basic"]
        else:
            basic_list = ["Advanced"]
        if skill["descriptor"]:
            basic_list.append(skill["descriptor"])
        info_text.append("({})".format(", ".join(basic_list)))
        info_text.append(
            "[b]Characteristic:[/b] {}".format(characteristics[skill["characteristic"]])
        )
        if skill["skill_group"]:
            info_text.append(
                "[b]Skill Groups:[/b] {}".format(", ".join(skill["skill_group"]))
            )
        info_text.append(
            "{}\n\n[b]Skill Use:[/b] {}".format(skill["text"], skill["skill_use"])
        )
        if skill["special_use"]:
            special_use_list = []
            special_use_list.append("[b]Special Use:[/b]")
            for key, value in skill["special_use"].items():
                special_use_list.append(
                    "{}\n  {}".format(key, "\n\n  ".join(value.split("\n\n")))
                )
            info_text.append("\n\n".join(special_use_list))
        super(SkillInfoPopup, self).__init__(
            skill["name"], "\n\n----\n\n".join(info_text), **kwargs
        )


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
                "[b]Talent Groups[/b]: "
                + ", ".join(talent["talent_group"])
                + "\n\n----\n\n"
            )
        info_text = "{}\n\n----\n\n[b]Prerequisits:[/b] {}\n\n----\n\n{}{}".format(
            talent["short_text"], ", ".join(prerequisits), talent_group, talent["text"]
        )
        super(TalentInfoPopup, self).__init__(talent["name"], info_text, **kwargs)


class DropdownButton(Button):
    def __init__(self, difficulty, modifier, **kwargs):
        super(DropdownButton, self).__init__(**kwargs)
        self.text = "{0} ({1:+d})".format(difficulty, modifier)
        self.modifier = modifier


class RogueTraderApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    RogueTraderApp().run()
