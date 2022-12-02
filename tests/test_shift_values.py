import unittest
import numpy as np

from split import check_shift_values


class TestShiftValues(unittest.TestCase):
    image = np.random.rand(50, 30, 3)

    def test_shift_values(self):
        result = check_shift_values(self.image, x_shift=10, y_shift=15)
        self.assertTrue(result == 0)

    def test_negative_shift_values(self):
        with self.assertRaises(ValueError):
            result = check_shift_values(self.image, x_shift=-10, y_shift=-15)

    def test_large_shift_values(self):
        with self.assertRaises(ValueError):
            result = check_shift_values(self.image, x_shift=100, y_shift=15)


if __name__ == '__main__':
    unittest.main()
