import os
import unittest
from math import ceil

import cv2
import numpy as np

from merge import get_dictionary_with_image_coordinates_and_names, get_split_parameters, merge
from split import split, read_image, get_image_name, save_image, make_directory


class TestSplit(unittest.TestCase):
    image_path = "./images/test.jpg"

    window_size = (10, 13)
    use_percent = True
    x_shift = 5
    y_shift = 10

    result_dir = "./results"

    def test_split(self):
        image = read_image(self.image_path)

        result_dir = split(self.image_path, self.window_size, self.use_percent, self.x_shift, self.y_shift, self.result_dir)
        parameters = get_split_parameters(result_dir)
        image_merged = merge(result_dir)

        save_image(image_merged, "./images", "merged.jpg")

        x_shift = parameters["xshift"]
        y_shift = parameters["yshift"]
        self.assertTrue((image[y_shift:, x_shift:]==image_merged).all())

    def test_read_images_splits_errors(self):
        with self.assertRaises(ValueError):
            get_dictionary_with_image_coordinates_and_names("./results/split")

        result_dir = make_directory("split", "./results")
        with self.assertRaises(ValueError):
            get_dictionary_with_image_coordinates_and_names(result_dir)

    def test_read_images_splits(self):
        result_dir = split(self.image_path, self.window_size, self.use_percent, self.x_shift, self.y_shift,
                           self.result_dir)
        names = get_dictionary_with_image_coordinates_and_names(result_dir)
        self.assertTrue(len(names)!=0)

    def test_read_images_split_parameters(self):
        result_dir = make_directory("test_images", "./results")
        name = "x_5_y_2_windowheight_10_windowwidth_15_xshift_3_yshift_2_imagewidth_30_imageheight_20.png"

        with open(os.path.join(result_dir, name), "w") as f:
            f.write("text")
        parameters = get_split_parameters(result_dir)
        self.assertTrue(parameters["windowheight"] == 10)
        self.assertTrue(parameters["windowwidth"] == 15)
        self.assertTrue(parameters["xshift"] == 3)
        self.assertTrue(parameters["yshift"] == 2)
        self.assertTrue(parameters["imagewidth"] == 30)
        self.assertTrue(parameters["imageheight"] == 20)


if __name__ == '__main__':
    unittest.main()
