import unittest
import numpy as np

from split import get_window_size_in_pixels


class TestWindowSize(unittest.TestCase):
    image = np.random.rand(50, 30, 3)

    def test_window_size_pixels_integer(self):
        window_height, window_width = get_window_size_in_pixels(self.image, window_size=(5, 3), use_percent=False)
        self.assertTrue(type(window_height) == int)
        self.assertTrue(type(window_width) == int)
        self.assertTrue(window_height == 5)
        self.assertTrue(window_width == 3)

    def test_window_size_pixels_float(self):
        with self.assertRaises(TypeError):
            window_height, window_width = get_window_size_in_pixels(self.image, window_size=(5.5, 3.0),
                                                                    use_percent=False)

    def test_window_size_percent_integer(self):
        window_height, window_width = get_window_size_in_pixels(self.image, window_size=(50, 10),
                                                                use_percent=True)
        self.assertTrue(type(window_height) == int)
        self.assertTrue(type(window_width) == int)
        self.assertTrue(window_height == 25)
        self.assertTrue(window_width == 3)

        window_height, window_width = get_window_size_in_pixels(self.image, window_size=(13, 9),
                                                                use_percent=True)
        self.assertTrue(type(window_height) == int)
        self.assertTrue(type(window_width) == int)
        self.assertTrue(window_height == 6)
        self.assertTrue(window_width == 2)

    def test_window_size_percent_float(self):
        window_height, window_width = get_window_size_in_pixels(self.image, window_size=(12.1, 7.8),
                                                                use_percent=True)
        self.assertTrue(type(window_height) == int)
        self.assertTrue(type(window_width) == int)
        self.assertTrue(window_height == 6)
        self.assertTrue(window_width == 2)

    def test_window_size_negative(self):
        with self.assertRaises(ValueError):
            window_height, window_width = get_window_size_in_pixels(self.image, window_size=(-3, 4),
                                                                use_percent=False)

        with self.assertRaises(ValueError):
            window_height, window_width = get_window_size_in_pixels(self.image, window_size=(-3.1, 4),
                                                                    use_percent=True)


if __name__ == '__main__':
    unittest.main()
