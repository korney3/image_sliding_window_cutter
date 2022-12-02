import os
import shutil
from math import floor
from typing import Tuple, Union, List

import cv2
import numpy as np


def split(image_path: str, window_size: Union[Tuple[int, int], Tuple[float, float]],
          use_percent: bool = False,
          x_shift: int = 0, y_shift: int = 0,
          result_dir: str = "./split_image"):
    '''
    Скрипт split принимает на вход картинку,
    размер (h, w) окна в пикселях или процентах,
    смещение по x и y, и нарезает
    изображения sliding window подходом.

    Arguments:
        image_path (str): path to image to split
        window_size (Tuple[int, int] or Tuple[float, float]): width
                                    and height of sliding window
                                    in pixels of percent
        use_percent (bool) = False: if window size is given is percent
        x_shift (int) = 0: shift of start of cutting x-coordinate
        y_shift (int) = 0: shift of start of cutting y-coordinate
        result_dir (str) = "./split_image": directory to store image's pieces
    Returns:
        Path to cut image
    '''

    image = read_image(image_path)
    window_height, window_width = get_window_size_in_pixels(image, window_size, use_percent)
    check_shift_values(image, x_shift, y_shift)
    result_dir = make_directory(image_path, result_dir)

    for (x, y, window) in split_generator(image, window_height, window_width, x_shift, y_shift):
        image_name = get_image_name(x, y, image.shape[0], image.shape[1], window_height, window_width, x_shift, y_shift)
        save_image(window, result_dir, image_name)
    return result_dir


def read_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError('Image can\'t be open')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def get_window_size_in_pixels(image: np.array,
                              window_size: Union[Tuple[int, int], Tuple[float, float]],
                              use_percent: bool) -> Tuple[int, int]:
    image_width = image.shape[1]
    image_height = image.shape[0]
    if use_percent:
        window_height = image_height * window_size[0] / 100
        window_height = floor(image_height * window_size[0] / 100)
        window_width = floor(image_width * window_size[1] / 100)
    else:
        window_height = window_size[0]
        window_width = window_size[1]
        if type(window_height) != int or type(window_width) != int:
            raise TypeError('Window sizes in pixels should be int')
    if window_height <= 0 or window_width <= 0:
        raise ValueError('Window sizes in pixels should be bigger than 0')
    return window_height, window_width


def check_shift_values(image: np.ndarray, x_shift: int = 0, y_shift: int = 0) -> int:
    if x_shift < 0 or y_shift < 0:
        raise ValueError('Shifts in pixels should be bigger than 0')
    if x_shift >= image.shape[1] or y_shift >= image.shape[1]:
        raise ValueError('Shifts in pixels should be less than image sizes')
    return 0


def make_directory(image_path: str, result_dir: str) -> str:
    _, image_name = os.path.split(image_path)
    image_name = image_name.split(".")[0]
    result_path = os.path.join(result_dir, image_name)
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.makedirs(os.path.join(result_dir, image_name))
    return os.path.join(result_dir, image_name)


def split_generator(image: np.ndarray, window_height: int, window_width: int, x_shift: int, y_shift: int) -> Tuple[
    int, int, np.ndarray]:
    for y in range(y_shift, image.shape[0], window_height):
        for x in range(x_shift, image.shape[1], window_width):
            yield x, y, image[y:y + window_height, x:x + window_width]


def get_image_name(x: int, y: int, image_height: int, image_width: int, window_height: int, window_width: int,
                   x_shift: int = 0, y_shift: int = 0):
    return f"x_{x}_y_{y}_windowheight_{window_height}_windowwidth_{window_width}_xshift_{x_shift}_yshift_{y_shift}_" \
           f"imagewidth_{image_width}_imageheight_{image_height}.png"


def save_image(image_array: np.ndarray, result_dir: str, image_name: str):
    image = image_array.astype(np.float32)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(os.path.join(result_dir, image_name), image)
    return os.path.abspath(os.path.join(result_dir, image_name))
