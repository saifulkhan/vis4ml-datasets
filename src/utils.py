import json
import matplotlib.pyplot as plt
import numpy as np
import cv2


def read_config(file):
    with open(file, "r") as file:
        config = json.load(file)
    return config


def read_distribution(file):
    config = read_config(file)
    return {
        "shapes": config["shapes"],
        "scales": config["scales"],
        "orientation": config["orientation"],
        "position_scales": config["position_scales"],
    }


def read_metadata(file):
    config = read_config(file)
    return {
        "output_dir": config["output_dir"],
        "num_images": config["num_images"],
        "image_size": config["image_size"],
        "color": config["color"],
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
