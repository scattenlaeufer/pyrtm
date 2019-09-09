import unittest

from utils import calculate_dos_rt, calculate_dos_dh2


class DoSRTTests(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(0, calculate_dos_rt(35, 35))
        self.assertEqual(0, calculate_dos_rt(35, 34))
        self.assertEqual(1, calculate_dos_rt(35, 45))
        self.assertEqual(1, calculate_dos_rt(35, 25))


class DoSDH2Tests(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(1, calculate_dos_dh2(35, 35))
        self.assertEqual(2, calculate_dos_dh2(35, 40))
        self.assertEqual(1, calculate_dos_dh2(35, 34))
        self.assertEqual(2, calculate_dos_dh2(35, 29))
