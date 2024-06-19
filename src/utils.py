import array
from importlib.metadata import distribution
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
import copy


def read_config(file):
    with open(file, "r") as file:
        config = json.load(file)
    return config


def read_distribution(file):
    config = read_config(file)
    conf = {
        "shape": config["shape"],
        "scale": config["scale"],
        "nsp_scale": config["nsp_scale"],
        "pos_x": config["pos_x"],
        "nsp_pos_x": config["nsp_pos_x"],
        "pos_y": config["pos_y"],
        "nsp_pos_y": config["nsp_pos_y"],
        "rotation": config["rotation"],
        "nsp_rotation": config["nsp_rotation"],
        "grey": config["grey"],
        "nsp_grey": config["nsp_grey"],
    }

    conf["scale"] = draw_fixed_numbers(conf["scale"], conf["nsp_scale"])
    conf["pos_x"] = draw_fixed_numbers(conf["pos_x"], conf["nsp_pos_x"])
    conf["pos_y"] = draw_fixed_numbers(conf["pos_y"], conf["nsp_pos_y"])
    conf["rotation"] = draw_fixed_numbers(conf["rotation"], conf["nsp_rotation"])

    return conf


def read_metadata(file):
    config = read_config(file)
    return {
        "num_images": config["num_images"],
        "num_shapes": config["num_shapes"],
        "output_dir": config["output_dir"],
        "output_prefix": config["output_prefix"],
        "output_type": config["output_type"],
        "output_digit": config["output_digit"],
        "image_width": config["image_width"],
        "image_height": config["image_height"],
        "color_type": config["color_type"],
        "background": config["background"],
        "color_background": config["color_background"],
        "shape_overlapping": config["shape_overlapping"],
        "shape_cropping": config["shape_cropping"],
    }


def show_sample(images, labels, num_samples=5):
    plt.figure(figsize=(10, 2))
    for i in range(num_samples):
        plt.subplot(1, num_samples, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(f"{labels[i][0]['shape']}")
        plt.axis("off")
    plt.show()


def show(image):
    plt.figure(figsize=(3, 3))
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.show()


def draw_fixed_numbers(arr, n):
    """
    Draws n fixed numbers from a given range [min, max] using NumPy.

    Parameters:
    min (float or int): The minimum value of the range.
    max (float or int): The maximum value of the range.
    n (int): The number of values to draw.

    Returns:
    np.ndarray: An array of n unique numbers drawn from the specified range.
    """

    [min, max] = arr

    if isinstance(min, int) and isinstance(max, int):
        if n > (max - min + 1):
            raise ValueError("n is larger than the range of unique numbers available.")
        return np.random.choice(np.arange(min, max + 1), n, replace=False)
    elif isinstance(min, float) or isinstance(max, float):
        return np.round(np.random.uniform(min, max, n), 4)

    else:
        raise TypeError("min and max must be both integers or both floats.")


def draw_sample(array, sample_size=1):
    """
    Draws a random sample from the given array.

    Parameters:
    array (np.ndarray): The array to sample from.
    sample_size (int): The number of elements to sample.

    Returns:
    np.ndarray: The random sample drawn from the array.
    """
    if sample_size > len(array):
        raise ValueError("Sample size cannot be larger than the array size")

    return np.random.choice(array, sample_size, replace=False)
