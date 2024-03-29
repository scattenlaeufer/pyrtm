#!/usr/bin/env python3

import os
import random
import math
import enum
import pathlib
from kivy.app import App
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import BooleanProperty, NumericProperty, OptionProperty
import utils


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
    "exp": [11500, 300],
    "status": {
        "wounds": {"max": 13, "current": 13, "critical": 0, "critical_effects": []},
        "fatigue": 0,
        "corruption": {"points": 1, "degree": 0, "malignancies": []},
        "insanity": {"points": 6, "degree": 0, "disorders": []},
        "fate": {"max": 4, "current": 4},
    },
    "characteristics": {
        "ws": [48, 2],
        "bs": [45, 1],
        "s": [35, 0],
        "t": [41, 1],
        "ag": [43, 1],
        "int": [42, 0],
        "per": [43, 1],
        "wp": [35, 1],
        "fel": [60, 2],
    },
    "skills": {
        "awareness": "t",
        "ciphers": {"Roque Trader": "t"},
        "charm": "+20",
        "command": "+10",
        "commerce": "t",
        "common_lore": {"Imperium": "t", "Koronos Expanse": "t", "Rogue Trader": "t"},
        "dodge": "t",
        "evaluate": "t",
        "inquiry": "t",
        "literacy": "+10",
        "pilot": {"Flyers": "t", "Space Craft": "t"},
        "scholastic_lore": {"Astromancy": "t"},
        "secret_tongue": {"Rogue Trader": "t"},
        "speak_language": {"High Gothic": "+10", "Low Gothic": "t", "Trader Cant": "t"},
        "tech-use": "t",
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
        ["two-weapon_wielder", "Melee", "Balistic"],
        ["sound_constitution", "3"],
        "quick_draw",
        "jaded",
        "iron_discipline",
        "leap_up",
        ["resistance", "Fear"],
    ],
    "implants": [
        {"key": "auger_arrays", "quality": "good", "on": False},
        {"key": "vitae_supplacement", "quality": "best", "on": True},
    ],
    "mutations": [],
    "weapons": [
        {"key": "plasma_pistol", "clip": 10, "clips": 5},
        {"key": "power_sword"},
    ],
    "armour": {
        "HEAD": 6,
        "RIGHT_ARM": 6,
        "LEFT_ARM": 6,
        "BODY": 6,
        "RIGHT_LEG": 6,
        "LEFT_LEG": 6,
    },
}


class DoSAlgorithm(enum.IntFlag):
    ROGUE_TRADER = enum.auto()
    MIXED = enum.auto()
    DARK_HERESY_2 = enum.auto()


class TestType(enum.IntFlag):
    FIGHT = enum.auto()
    OTHER = enum.auto()


data = {}
config = None
CHARACTER = None
default_config = {"dos_algorithm": DoSAlgorithm.ROGUE_TRADER.value}


class MainBox(BoxLayout):

    data = {}

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        data_json = JsonStore(os.path.join("data/rogue_trader_data.json"))
        for key in data_json.keys():
            self.data[key] = data_json[key]
        global data
        data = self.data
        user_dir = pathlib.Path(App.get_running_app().user_data_dir)

        # Load config
        global config
        config = JsonStore(user_dir / "config.json")
        if not config.exists("config"):
            config.put("config", **default_config)

        dos_algorithm = DoSAlgorithm(config.get("config")["dos_algorithm"])
        if dos_algorithm == DoSAlgorithm.ROGUE_TRADER:
            self.ids["dos_rt"].state = "down"
        elif dos_algorithm == DoSAlgorithm.MIXED:
            self.ids["dos_mixed"].state = "down"
        else:
            self.ids["dos_dh2"].state = "down"

        self.ids["dos_rt"].algorithm = DoSAlgorithm.ROGUE_TRADER
        self.ids["dos_mixed"].algorithm = DoSAlgorithm.MIXED
        self.ids["dos_dh2"].algorithm = DoSAlgorithm.DARK_HERESY_2

        # load character
        global CHARACTER
        CHARACTER = JsonStore(user_dir / "character.json")
        if not CHARACTER.exists("character"):
            CHARACTER.put("character", **default_character)
        # CHARACTER.put("character", **default_character)
        self.character = CHARACTER.get("character")
        start_layout = StartLayout(self.data)
        self.ids["all_talents"].add_widget(start_layout)

        # set characteristics
        for key in characteristics.keys():
            self.ids[key].set_text(self.character["characteristics"][key])
            self.ids[key].key = self.data["characteristics"][key]["name"]
            self.ids[key].value = self.character["characteristics"][key][0]
            self.ids[key].bind(on_press=lambda inst: TestPopup(inst.key, inst.value))

        # add skills to the charakter screen
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

        # add talents to the character screen
        for talent in self.character["talents"]:
            if type(talent) == list:
                key = talent[0]
                groups = talent[1:]
            else:
                key = talent
                groups = []
            button = TalentButton(
                key=key,
                text=f'{self.data["talents"][key]["name"]}'
                if len(groups) == 0
                else f'{self.data["talents"][key]["name"]} ({", ".join(groups)})',
            )
            button.bind(on_press=lambda b: TalentInfoPopup(self.data["talents"][b.key]))
            self.ids["talents_box"].add_widget(button)
            self.ids["talents_box"].height += button.height

            # handle talented
            if key == "talented":
                for skill in groups:
                    for skill_key, skill_data in self.data["skills"].items():
                        if skill_data["name"] == skill:
                            break
                    self.skill_box_dict[skill_key].skill_value += 10
                    self.skill_box_dict[skill_key].modifier_list.append(
                        {
                            "name": f"Talented ({skill})",
                            "bonus": 10,
                            "type": "talent",
                            "on": True,
                        }
                    )
        self.ids["talents_box"].children.sort()

        # add implants to the character srceen
        self.ids["implants_box"].height = 0
        for implant in self.character["implants"]:
            modifier_list = []
            for modifier in self.data["implants"][implant["key"]]["bonus"]:
                modifier_list.append([self.skill_box_dict[modifier[0]], modifier[1]])
            implant_box = ImplantBox(
                self.data["implants"][implant["key"]],
                implant["on"],
                implant["quality"],
                modifier_list,
            )
            self.ids["implants_box"].add_widget(implant_box)
            self.ids["implants_box"].height += implant_box.height

        # add weapons to the battle screen
        for weapon in self.character["weapons"]:
            weapon_box = WeaponBox(
                weapon,
                self.character["characteristics"]["ws"][0],
                self.character["characteristics"]["bs"][0],
                self.character["characteristics"]["s"][0],
                self.skill_box_dict["dodge"].skill_value,
            )
            self.ids["weapon_box"].add_widget(weapon_box)
            self.ids["weapon_box"].height += weapon_box.height

        # set wounds
        self.ids["wounds_max"].text = str(self.character["status"]["wounds"]["max"])
        self.ids["wounds_current"].text = str(
            self.character["status"]["wounds"]["current"]
        )
        self.ids["wounds_critical"].text = str(
            self.character["status"]["wounds"]["critical"]
        )
        self.ids["button_take_damage"].bind(on_press=lambda _: TakeDamagePopup(self))
        self.ids["button_heal"].bind(on_press=lambda _: HealDamagePopup(self))

        # set fatigue
        self.ids["fatigue_current"].text = str(self.character["status"]["fatigue"])
        self.ids["fatigue_max"].text = str(
            self.character["characteristics"]["t"][0] // 10
        )

        # set fate points
        self.ids["fate_max"].text = str(self.character["status"]["fate"]["max"])
        self.ids["fate_current"].text = str(self.character["status"]["fate"]["current"])

    def characteristics_test(self, instance):
        print(instance.text)
        InfoPopup("test", instance.text).open()

    def skill_info(self, instance):
        SkillInfoPopup(self.data["skills"][instance.skill_key])

    def add_fatigue(self):
        char = CHARACTER.get("character")
        char["status"]["fatigue"] += 1
        tb = char["characteristics"]["t"][0] // 10
        if char["status"]["fatigue"] > tb:
            NotificationPopup(f"{char['name']} is unconscious for {10-tb} minutes")
            char["status"]["fatigue"] = tb
        self.ids["fatigue_current"].text = str(char["status"]["fatigue"])
        CHARACTER.put("character", **char)

    def remove_fatigue(self):
        char = CHARACTER.get("character")
        if char["status"]["fatigue"] > 0:
            char["status"]["fatigue"] -= 1
            self.ids["fatigue_current"].text = str(char["status"]["fatigue"])
            CHARACTER.put("character", **char)


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


class TalentButton(Button):

    key = ""

    def __init__(self, key=None, **kwargs):
        self.key = key
        super().__init__(**kwargs)

    def __lt__(self, other):
        return other.text < self.text


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
        **kwargs,
    ):
        super(SkillBox, self).__init__(**kwargs)
        self.modifier_list = []
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
        TestPopup(self.ids["button_info"].text, self.skill_value, self.modifier_list)


class ImplantBox(BoxLayout):
    def __init__(self, implant, status, quality, modifier_list, **kwargs):
        super(ImplantBox, self).__init__(**kwargs)
        self.implant = implant
        self.modifier_list = modifier_list
        for skill_box, bonus in self.modifier_list:
            skill_box.modifier_list.append(
                {
                    "name": self.implant["name"],
                    "bonus": bonus,
                    "type": "implant",
                    "on": self,
                }
            )
        self.ids["button_name"].text = implant["name"]
        self.ids["label_quality"].text = quality
        self.ids["switch_on"].bind(active=self.switch_implant)
        self.ids["switch_on"].active = status

    def button_info_press(self):
        ItemInfoPopup(self.implant)

    def switch_implant(self, instance, on):
        if on:
            for modifier in self.modifier_list:
                modifier[0].skill_value += modifier[1]
        else:
            for modifier in self.modifier_list:
                modifier[0].skill_value -= modifier[1]


class WeaponBox(BoxLayout):
    def __init__(self, weapon, ws, bs, st, dodge, bonus={}, **kwargs):
        super(WeaponBox, self).__init__(**kwargs)
        self.weapon = weapon
        self.ws = ws
        self.bs = bs
        self.st = st
        self.dodge = dodge
        self.bonus = bonus

        info_text = ""
        info_text += "**Class**: {}\n\n".format(data["weapons"][weapon["key"]]["class"])

        self.ids["name"].text = data["weapons"][weapon["key"]]["name"]
        self.ids["label_class"].text = "Class: {}".format(
            data["weapons"][weapon["key"]]["class"]
        )
        self.ids["label_pen"].text = "Pen: {}".format(
            data["weapons"][weapon["key"]]["pen"]
        )
        damage_list = []
        if data["weapons"][weapon["key"]]["damage"]["d5"]:
            damage_list.append(
                str(data["weapons"][weapon["key"]]["damage"]["d5"]) + "d5"
            )
        if data["weapons"][weapon["key"]]["damage"]["d10"]:
            damage_list.append(
                str(data["weapons"][weapon["key"]]["damage"]["d10"]) + "d10"
            )
        damage_list += [
            data["weapons"][weapon["key"]]["damage"]["+"],
            data["weapons"][weapon["key"]]["damage"]["type"],
        ]
        self.ids["label_damage"].text = "Dam: {}+{} {}".format(*damage_list)
        self.ids["label_weight"].text = "Weight: {}kg".format(
            data["weapons"][weapon["key"]]["weight"]
        )
        # self.ids["label_availability"].text = "({})".format(
        #     data["weapons"][weapon["key"]]["availability"]
        # )
        if not data["weapons"][weapon["key"]]["class"] in ["Melee"]:
            self.ids["label_range"].text = "Range: {}m".format(
                data["weapons"][weapon["key"]]["range"]
            )
            self.ids["label_rof"].text = "RoF: {} / {} / {}".format(
                *data["weapons"][weapon["key"]]["rof"]
            )
            self.ids["label_reload"].text = "Reload: {}".format(
                data["weapons"][weapon["key"]]["reload"]
            )
            self.ids["label_clip"].text = "Clip: {} / {}".format(
                weapon["clip"], data["weapons"][weapon["key"]]["clip"]
            )
        if not (
            data["weapons"][weapon["key"]]["class"] in ["Melee"]
            or "Unwieldy" in data["weapons"][weapon["key"]]["special"]
        ):
            self.ids["button_parry"].disabled = True
            self.ids["button_parry"].opacity = 0
        special_list = []
        for special in data["weapons"][weapon["key"]]["special"]:
            button = Factory.WeaponBoxButton(text=special)
            button.bind(
                on_press=lambda inst: InfoPopup(
                    inst.text, data["weapons"]["special_qualities"][inst.text]
                )
            )
            special_list.append(button)
        special_list.sort(key=lambda a: a.text)
        for special in special_list:
            self.ids["special_box"].add_widget(special)
        self.height = self.ids["name"].font_size * (
            9
            + 2.5
            * math.ceil(
                len(self.ids["special_box"].children) / self.ids["special_box"].cols
            )
        )
        info_text += "**Weight**: {}kg\n\n".format(
            data["weapons"][weapon["key"]]["weight"]
        )
        info_text += "**Availability**: {}\n\n".format(
            data["weapons"][weapon["key"]]["availability"]
        )
        info_text += "{}\n\n----\n\n**{}**\n\n{}".format(
            data["weapons"][self.weapon["key"]]["text"],
            data["weapons"][self.weapon["key"]]["type"],
            data["weapons"]["general"][data["weapons"][self.weapon["key"]]["type"]],
        )
        self.ids["name"].bind(
            on_press=lambda inst: InfoPopup(
                data["weapons"][self.weapon["key"]]["name"], info_text
            )
        )

    def attack_test(self):
        if data["weapons"][self.weapon["key"]]["class"] in ["Melee"]:
            test_popup = TestPopup(
                "Weapon Skill",
                self.ws,
                test_type=TestType.FIGHT,
                damage=data["weapons"][self.weapon["key"]]["damage"],
                damage_bonus=self.st // 10,
            )
        else:
            test_popup = TestPopup(
                "Ballistic Skill",
                self.bs,
                test_type=TestType.FIGHT,
                damage=data["weapons"][self.weapon["key"]]["damage"],
            )

    def dodge_test(self):
        TestPopup("Dodge", self.dodge, test_type=TestType.FIGHT)

    def parry_test(self):
        bonus_list = []
        bonus = 0
        if "Balanced" in data["weapons"][self.weapon["key"]]["special"]:
            bonus_list.append(
                {"name": "Balanced", "bonus": 10, "type": "other", "on": True}
            ),
            bonus += 10
        if "Mordian-pattern" in data["weapons"][self.weapon["key"]]["name"]:
            bonus_list.append(
                {"name": "Mordian-pattern", "bonus": 5, "type": "other", "on": True}
            )
            bonus += 5
        print(bonus)
        TestPopup("Parry", self.ws + bonus, bonus_list, test_type=TestType.FIGHT)


class ModifierBox(BoxLayout):
    def __init__(self, modifier, **kwargs):
        super(ModifierBox, self).__init__(**kwargs)
        self.bonus = modifier["bonus"]
        self.ids["label_name"].text = modifier["name"]
        if modifier["type"] == "implant":
            self.ids["checkbox_on"].active = modifier["on"].ids["switch_on"].active
        else:
            self.ids["checkbox_on"].active = modifier["on"]


class TestPopup(Popup):

    current_value = NumericProperty()
    success = OptionProperty("none", options=["none", "yes", "no"])

    def __init__(
        self,
        title,
        base_value,
        modifier=[],
        test_type=TestType.OTHER,
        damage=None,
        damage_bonus=0,
        **kwargs,
    ):
        super(TestPopup, self).__init__(**kwargs)
        self.title = "{} Test".format(title)
        self.base_value = base_value
        self.difficulty = 0
        self.misc_mod = 0
        self.roll = 0
        self.current_value = self.base_value
        self.modifier = modifier.copy()
        self.test_type = test_type
        self.damage = damage
        self.damage_bonus = damage_bonus
        self.difficulty_dropdown = DropDown()
        for difficulty in test_difficulties:
            button = DropdownButton(*difficulty)
            button.bind(
                on_release=lambda btn: self.difficulty_dropdown.select(
                    [btn.text, btn.modifier]
                )
            )
            self.difficulty_dropdown.add_widget(button)
        self.ids["button_difficulty"].bind(on_release=self.difficulty_dropdown.open)
        self.difficulty_dropdown.bind(on_select=self.set_difficulty)
        self.ids["modifier_box"].height = 0
        fatigue_mod = {"name": "Fatigue", "bonus": -10, "type": "status"}
        char = CHARACTER.get("character")
        if char["status"]["fatigue"] > 0:
            fatigue_mod["on"] = True
            self.current_value += fatigue_mod["bonus"]
        else:
            fatigue_mod["on"] = False
        self.modifier.append(fatigue_mod)
        for mod in self.modifier:
            modifier_box = ModifierBox(mod)
            modifier_box.ids["checkbox_on"].bind(active=self.modify_current_value)
            self.ids["modifier_box"].add_widget(modifier_box)
            self.ids["modifier_box"].height += modifier_box.height

        dos_config = DoSAlgorithm(config.get("config")["dos_algorithm"])
        if dos_config == DoSAlgorithm.DARK_HERESY_2:
            self.dos_func = utils.calculate_dos_dh2
        elif dos_config == DoSAlgorithm.ROGUE_TRADER:
            self.dos_func = utils.calculate_dos_rt
        if dos_config == DoSAlgorithm.MIXED and test_type == TestType.OTHER:
            self.dos_func = utils.calculate_dos_rt
        if dos_config == DoSAlgorithm.MIXED and test_type == TestType.FIGHT:
            self.dos_func = utils.calculate_dos_dh2

        if test_type == TestType.FIGHT:
            self.ids["button_damage"].on_press = self.roll_damage
        self.open()

    def set_difficulty(self, button, difficulty):
        self.ids["button_difficulty"].text = difficulty[0]
        difficulty_change = difficulty[1] - self.difficulty
        self.difficulty = difficulty[1]
        self.current_value += difficulty_change

    def set_misc_modifier(self, textinput, misc_mod):
        try:
            misc_mod = int(misc_mod)
        except ValueError:
            misc_mod = 0
        misc_mod_diff = misc_mod - self.misc_mod
        self.misc_mod = misc_mod
        self.current_value += misc_mod_diff

    def modify_current_value(self, instance, on):
        if on:
            self.current_value += instance.parent.bonus
        else:
            self.current_value -= instance.parent.bonus

    def roll_test(self):
        self.roll = random.randint(1, 100)
        if self.roll <= self.current_value:
            self.success = "yes"
        else:
            self.success = "no"
        self.ids["label_result"].text = str(self.roll)
        degrees = self.dos_func(self.current_value, self.roll)
        self.ids["label_degrees"].text = "{} {}".format(
            degrees, "Degree" if degrees == 1 else "Degrees"
        )

    def roll_damage(self):
        DamagePopup(utils.HitLocation.get(self.roll), self.damage, self.damage_bonus)

    def on_current_value(self, instance, value):
        self.ids["label_current_value"].text = str(value)

    def on_success(self, instance, value):
        if self.test_type == TestType.FIGHT and value == "yes":
            self.ids["button_damage"].disabled = False
            self.ids["button_damage"].opacity = 1.0
        else:
            self.ids["button_damage"].disabled = True
            self.ids["button_damage"].opacity = 0


class DamagePopup(Popup):
    def __init__(self, hit_location, damage, bonus=0, **kwargs):
        super().__init__(**kwargs)
        self.ids["label_hit_location"].text = hit_location.label()
        self.damage = damage
        print(f"bonus: {bonus} | +: {damage['+']}")
        damage_value = bonus + damage["+"]
        for _ in range(self.damage["d5"]):
            roll = random.randint(1, 5)
            print(roll)
            damage_value += roll
        for _ in range(self.damage["d10"]):
            roll = random.randint(1, 10)
            print(roll)
            if roll == 10:
                self.ids["label_rf"].text = "YES!"
            damage_value += roll
        self.ids["label_damage"].text = str(damage_value)
        self.open()


class InfoPopup(Popup):
    def __init__(self, title, info, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title = title
        self.ids["label_info"].text = info
        self.open()


class NotificationPopup(Popup):
    def __init__(self, notification, title="Notification", **kwargs):
        super().__init__(title=title)
        self.ids["notification_label"].text = notification
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
        prerequisites = []
        if len(talent["prerequisites"]["characteristics"]) > 0:
            for key, value in talent["prerequisites"]["characteristics"].items():
                prerequisites.append("{}: {}".format(characteristics[key], value))
        if len(talent["prerequisites"]["skills"]) > 0:
            for value in talent["prerequisites"]["skills"]:
                prerequisites.append(value)
        if len(talent["prerequisites"]["talents"]) > 0:
            for value in talent["prerequisites"]["talents"]:
                prerequisites.append(value)
        if len(talent["prerequisites"]["other"]) > 0:
            for value in talent["prerequisites"]["other"]:
                prerequisites.append(value)
        if len(prerequisites) == 0:
            prerequisites.append("None")

        talent_group = ""
        if talent["talent_group"]:
            talent_group = (
                "[b]Talent Groups[/b]: "
                + ", ".join(talent["talent_group"])
                + "\n\n----\n\n"
            )
        info_text = "{}\n\n----\n\n[b]Prerequisites:[/b] {}\n\n----\n\n{}{}".format(
            talent["short_text"], ", ".join(prerequisites), talent_group, talent["text"]
        )
        super(TalentInfoPopup, self).__init__(talent["name"], info_text, **kwargs)


class ItemInfoPopup(InfoPopup):
    def __init__(self, item, **kwargs):
        info_text = "Availability: {}\n\n----\n\n{}".format(
            item["availability"], item["text"]
        )
        super(ItemInfoPopup, self).__init__(item["name"], info_text, **kwargs)


class TakeDamagePopup(Popup):
    def __init__(self, instance, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.hit_location = utils.HitLocation.BODY
        self.hit_location_dropdown = DropDown()
        for hit_location in utils.HitLocation.__members__.values():
            button = HitLocationButton(hit_location)
            button.bind(
                on_release=lambda btn: self.hit_location_dropdown.select(btn.location)
            )
            self.hit_location_dropdown.add_widget(button)
        self.ids["button_hit_location"].bind(on_release=self.hit_location_dropdown.open)
        self.hit_location_dropdown.bind(on_select=self.set_hit_location)
        self.open()

    def ok(self):
        damage_raw = (
            int(self.ids["input_damage"].text) if self.ids["input_damage"].text else 0
        )
        damage = damage_raw
        char = CHARACTER.get("character")
        reduction = 0
        toughness = char["characteristics"]["t"][0] // 10
        if self.ids["damage_toughness"].active:
            reduction += toughness
        pen = int(self.ids["input_pen"].text) if self.ids["input_pen"].text else 0
        armour = char["armour"][self.hit_location.name]
        if self.ids["damage_armour"].active:
            reduction += armour - pen if armour > pen else 0
        damage = damage - reduction if damage_raw > reduction else 0
        char["status"]["wounds"]["current"] -= damage
        CHARACTER.put("character", **char)
        self.instance.ids["wounds_current"].text = str(
            char["status"]["wounds"]["current"]
        )
        self.dismiss()

    def set_hit_location(self, _, hit_location):
        self.hit_location = hit_location
        self.ids["button_hit_location"].text = self.hit_location.label()


class HealDamagePopup(Popup):
    def __init__(self, instance, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.open()

    def ok(self):
        heal = int(self.ids["input_value"].text) if self.ids["input_value"].text else 0
        char = CHARACTER.get("character")
        char["status"]["wounds"]["current"] += heal
        if char["status"]["wounds"]["current"] > char["status"]["wounds"]["max"]:
            char["status"]["wounds"]["current"] = char["status"]["wounds"]["max"]
        CHARACTER.put("character", **char)
        self.instance.ids["wounds_current"].text = str(
            char["status"]["wounds"]["current"]
        )
        self.dismiss()


class DropdownButton(Button):
    def __init__(self, difficulty, modifier, **kwargs):
        super(DropdownButton, self).__init__(**kwargs)
        self.text = "{0} ({1:+d})".format(difficulty, modifier)
        self.modifier = modifier


class HitLocationButton(Button):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.text = location.label()
        self.location = location


class ConfigButton(ToggleButton):
    def config_action(self):
        config.put("config", dos_algorithm=self.algorithm.value)


class RogueTraderApp(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    RogueTraderApp().run()
