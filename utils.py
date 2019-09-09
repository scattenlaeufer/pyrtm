def calculate_dos_rt(value, roll):
    return abs(roll - value) // 10


def calculate_dos_dh2(value, roll):
    return 1 + abs(roll // 10 - value // 10)
