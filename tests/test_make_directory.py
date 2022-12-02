import os
import unittest
import cv2
import numpy as np

from split import make_directory


class TestMakeDirectory(unittest.TestCase):
    image_path_with_directory = "./images/testdir.jpg"
    image_path_name = "test"

    result_dir = "./results"

    def test_make_directory(self):
        result = make_directory(self.image_path_with_directory, self.result_dir)
        self.assertTrue(os.path.isdir("./results/testdir/"))

        result = make_directory(self.image_path_name, self.result_dir)
        self.assertTrue(os.path.isdir("./results/test/"))

    def test_make_duplicated_directory(self):
        result = make_directory(self.image_path_with_directory, self.result_dir)
        self.assertTrue(os.path.isdir("./results/testdir/"))

        with open(os.path.join(result, "file"), "w") as f:
            f.write("text")
        self.assertTrue(os.path.exists("./results/testdir/file"))

        result = make_directory(self.image_path_with_directory, self.result_dir)
        self.assertFalse(os.path.exists("./results/testdir/file"))


if __name__ == '__main__':
    unittest.main()
