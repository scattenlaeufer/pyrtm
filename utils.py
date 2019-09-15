"""
Collection of utility functions
"""


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
