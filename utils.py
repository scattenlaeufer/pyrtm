"""
Collection of utility functions
"""

import enum


def calculate_dos_rt(value, roll):
    """
    Calculate degrees of success based on Rogue Trader

    :param value int: Value against which the test is rolled
    :param roll int: Result of the roll
    """
    return abs(roll - value) // 10


def calculate_dos_dh2(value, roll):
    """
    Calculate degrees of success based on Dark Heresy 2

    :param value int: Value against which the test is rolled
    :param roll int: Result of the roll
    """
    return 1 + abs(roll // 10 - value // 10)


def get_hit_location(role):
    location_value = int(str(role)[::-1])
    return location_value


class HitLocation(enum.Enum):
    HEAD = [i for i in range(1, 10)]
    RIGHT_ARM = [i for i in range(11, 20)]
    LEFT_ARM = [i for i in range(21, 30)]
    BODY = [i for i in range(31, 70)]
    RIGHT_LEG = [i for i in range(71, 85)]
    LEFT_LEG = [i for i in range(86, 99)].append(0)

    __labels__ = {
        "HEAD": "Head",
        "RIGHT_ARM": "Right Arm",
        "LEFT_ARM": "Left Arm",
        "BODY": "Body",
        "RIGHT_LEG": "Right Leg",
        "LEFT_LEG": "Left Leg",
    }

    @classmethod
    def get(cls, value, *args, **kwargs):
        if isinstance(value, int):
            for location in cls.__members__.values():
                if value in location.value:
                    return location
            raise ValueError(f"{value} is not a hit location")
        else:
            raise TypeError(f"value must be of type int, not {type(value)}")

    def label(self):
        return self.__class__.__labels__.get(self.name, self.name)
