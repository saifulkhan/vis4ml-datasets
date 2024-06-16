import os
import json
import numpy as np
from itertools import combinations
from PIL import Image

from .utils import read_distribution, read_metadata
from .shape import (
    circle,
    square,
    triangle,
    combine_shapes,
    check_occlusion,
    check_clipping,
)


def generate_images(metadata_file, distribution_file):
    distribution = read_distribution(distribution_file)
    metadata = read_metadata(metadata_file)

    images = []
    labels = []

    for _ in range(metadata["num_images"]):
        image, label = generate_image(metadata["image_size"], distribution)
        images.append(image)
        labels.append(label)

    # save images and metadata
    output_dir = metadata["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    for i, (image, label) in enumerate(zip(images, labels)):
        img_pil = Image.fromarray((image * 255).astype(np.uint8))
        img_filename = os.path.join(output_dir, f"image_{i}.png")
        img_pil.save(img_filename)

        label_filename = os.path.join(output_dir, f"label_{i}.json")
        with open(label_filename, "w") as f:
            json.dump(label, f, indent=2)

    return images, labels


def generate_image(image_size, distribution):

    num_shapes = np.random.randint(1, len(distribution["shapes"]) + 1)
    images = []
    label = {"shapes": [], "occluded": False}

    for _ in range(num_shapes):
        shape = np.random.choice(distribution["shapes"])
        scale = np.random.uniform(*distribution["scales"])
        orientation = np.random.uniform(*distribution["orientation"])
        position_scale = [
            np.random.uniform(*distribution["position_scales"]),
            np.random.uniform(*distribution["position_scales"]),
        ]

        if shape == "circle":
            image = circle(image_size, scale, orientation, position_scale)
            label["shapes"].append({"type": "circle", "clipped": check_clipping(image)})
        elif shape == "square":
            image = square(image_size, scale, orientation, position_scale)
            label["shapes"].append({"type": "square", "clipped": check_clipping(image)})
        elif shape == "triangle":
            image = triangle(image_size, scale, orientation, position_scale)
            label["shapes"].append(
                {"type": "triangle", "clipped": check_clipping(image)}
            )

        images.append(image)

    # create combinations of two pairs
    combinations_of_two = list(combinations(images, 2))
    for pair in combinations_of_two:
        if check_occlusion(*pair):
            label["occluded"] = True
            break

    combined_image = combine_shapes(image_size, images)

    return combined_image, label
