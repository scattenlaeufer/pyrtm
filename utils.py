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


def get_hit_location(roll):
    location_value = int(f"{roll:02}"[::-1])
    return location_value


class HitLocation(enum.Enum):
    HEAD = [i for i in range(1, 11)]
    RIGHT_ARM = [i for i in range(11, 21)]
    LEFT_ARM = [i for i in range(21, 31)]
    BODY = [i for i in range(31, 71)]
    RIGHT_LEG = [i for i in range(71, 86)]
    LEFT_LEG = [i for i in range(86, 101)]

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
            if value == 100:
                location_value = 100
            else:
                location_value = int(f"{value:02}"[::-1])
            for location in cls.__members__.values():
                if location_value in location.value:
                    return location
            raise ValueError(f"{value} is not a hit location")
        else:
            raise TypeError(f"value must be of type int, not {type(value)}")

    def label(self):
        return self.__class__.__labels__.get(self.name, self.name)
