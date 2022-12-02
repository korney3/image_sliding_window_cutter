import os
import unittest

import numpy as np

from split import read_image, get_image_name, save_image


class TestImageReadWrite(unittest.TestCase):
    empty_image_path = "./non_existing_image.jpg"
    image_path = "./images/test.jpg"
    black_image_path = "./images/black.png"

    image = np.random.randint(low=0, high=255, size=(20, 30, 3))

    def test_read_empty_image(self):
        with self.assertRaises(ValueError):
            read_image(self.empty_image_path)

    def test_read_black_image(self):
        image = read_image(self.black_image_path)
        black = np.zeros((128, 128, 3))
        self.assertTrue((image == black).all())

    def test_creating_image_name(self):
        x = 5
        y = 2
        window_height = 10
        window_width = 15
        x_shift = 3
        y_shift = 2
        result = get_image_name(x, y, self.image.shape[0], self.image.shape[1], window_height, window_width, x_shift,
                                y_shift)
        expected = "x_5_y_2_windowheight_10_windowwidth_15_xshift_3_yshift_2_imagewidth_30_imageheight_20.png"

        self.assertTrue(expected == result)

    def test_image_save(self):
        x = 5
        y = 2
        window_height = 10
        window_width = 15
        x_shift = 3
        y_shift = 2
        image_name = get_image_name(x, y, self.image.shape[0], self.image.shape[1], window_height, window_width,
                                    x_shift, y_shift)
        result = save_image(self.image, "./results/test", image_name)
        self.assertTrue(os.path.exists(result))

        image = read_image(result)
        self.assertTrue((image == self.image).all())


if __name__ == '__main__':
    unittest.main()
