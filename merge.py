import os
import shutil
from math import floor
from typing import Tuple, Union, List

import cv2
import numpy as np

from split import get_image_name, read_image, save_image


def merge(image_dir: str) -> np.ndarray:
    '''
    Скрипт merge принимает на вход папку
    с нарезанными картинками и из них собирает
    оригинальную.

    Arguments:
        image_dir (str): path to directory with splitted images
    Returns:
        Numpy array with merged image
    '''

    image_rows = []

    images_dict = get_dictionary_with_image_coordinates_and_names(image_dir)
    parameters = get_split_parameters(image_dir)

    y_shift = parameters["yshift"]
    x_shift = parameters["xshift"]

    window_height = parameters["windowheight"]
    window_width = parameters["windowwidth"]

    image_height = parameters["imageheight"]
    image_width = parameters["imagewidth"]

    for y in range(y_shift, image_height, window_height):
        image_row = []
        for x in range(x_shift, image_width, window_width):
            image_name = get_image_name(x, y, image_height, image_width, window_height, window_width, x_shift, y_shift)
            window = read_image(os.path.join(image_dir, image_name))
            image_row.append(window)
        image_rows.append(np.concatenate(image_row, axis=1))
    image = np.concatenate(image_rows, axis=0)
    return image


def get_split_parameters(image_dir: str):
    images = os.listdir(image_dir)
    image_name = images[0].split(".")[0]
    parameters_name = image_name.split("_")
    parameters = {}
    for i in range(len(parameters_name) // 2):
        name = parameters_name[2 * i]
        value = parameters_name[2 * i + 1]
        if name == "x" or name == "y":
            continue
        parameters[name] = int(value)
    return parameters


def check_directory(image_dir: str):
    if (not os.path.isdir(image_dir)):
        raise ValueError("Directory doesn't exists")


def get_dictionary_with_image_coordinates_and_names(image_dir: str):
    check_directory(image_dir)
    images = os.listdir(image_dir)
    if len(images) == 0:
        raise ValueError("Directory is empty")
    images_dict = dict([((image.split("_")[1], image.split("_")[3]), image) for image in images])
    return images_dict
