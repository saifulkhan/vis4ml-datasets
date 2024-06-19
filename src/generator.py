import os
import json
import numpy as np
from PIL import Image
from tqdm import tqdm

from .utils import draw_fixed_numbers, draw_sample, read_distribution, read_metadata
from .shape import (
    circle,
    square,
    triangle,
    combine_shapes,
    check_overlapping,
    check_cropping,
)

shape_functions = {"circle": circle, "square": square, "triangle": triangle}


def generate_images(metadata, distribution):
    """
    Args:
        metadata (_type_): _description_
        distribution (_type_): _description_
    """

    images = []
    labels = []

    pass

    # for _ in range(metadata["num_images"]):
    for _ in tqdm(range(metadata["num_images"])):
        image, label = generate_image(metadata, distribution)
        images.append(image)
        labels.append(label)

    # save images and metadata
    output_dir = f"{metadata['output_dir']}/{metadata['output_prefix']}"
    os.makedirs(output_dir, exist_ok=True)

    for i, (image, label) in enumerate(zip(images, labels)):
        img_pil = Image.fromarray((image * 255).astype(np.uint8))
        img_filename = os.path.join(output_dir, f"image_{i}.png")
        img_pil.save(img_filename)

        label_filename = os.path.join(output_dir, f"label_{i}.json")
        with open(label_filename, "w") as f:
            json.dump(label, f, indent=2)


def generate_image(metadata, distribution):
    """
    Function for shapes and checks are same as provided earlier
    Args:
        metadata (_type_): _description_
        distribution (_type_): _description_

    Returns:
        _type_: _description_
    """
    image_size = (metadata["image_height"], metadata["image_width"])

    # Create output directory if not exists
    # os.makedirs(metadata["output_dir"], exist_ok=True)

    images = []
    label = []

    for _ in range(metadata["num_shapes"]):
        while True:
            shape = draw_sample(distribution["shape"], 1)[0]
            scale = draw_sample(distribution["scale"], 1)[0]
            pos_x = draw_sample(distribution["pos_x"], 1)[0]
            pos_y = draw_sample(distribution["pos_y"], 1)[0]
            rotation = draw_sample(distribution["rotation"], 1)[0]
            position_scale = (pos_x, pos_y)

            shape_img = shape_functions[shape](
                image_size, scale, rotation, position_scale
            )

            if metadata["shape_cropping"] != check_cropping(shape_img):
                continue
            # debug
            # print(f"{metadata['shape_cropping']} {check_cropping(shape_img)}")

            # TODO this does not work when shape_overlapping: true
            overlapped = False
            for existing_shape in images:
                overlapped = check_overlapping(existing_shape, shape_img)
                if metadata["shape_overlapping"] != overlapped:
                    break
            # print(metadata["shape_overlapping"], occluded)

            # continue the while loop
            if metadata["shape_overlapping"] != overlapped:
                continue
            # print(metadata["shape_overlapping"], overlapped)

            label.append(
                {
                    "shape": shape,
                    "scale": scale.item(),
                    "pos_x": pos_x.item(),
                    "pos_y": pos_y.item(),
                    "rotation": rotation.item(),
                }
            )
            images.append(shape_img)

            break

    final_image = combine_shapes(image_size, images)

    if metadata["color_type"] == "grey":
        final_image = final_image * np.random.randint(
            distribution["grey"][0], distribution["grey"][1]
        )

    # final_image = np.clip(final_image, 0, 255).astype(np.uint8)
    # final_image = cv2.cvtColor(final_image, cv2.COLOR_GRAY2BGR)
    # file_name = f"{metadata['output_prefix']}{str(i).zfill(metadata['output_digit'])}.{metadata['output_type']}"
    # output_path = os.path.join(metadata["output_dir"], file_name)
    # cv2.imwrite(output_path, final_image)

    return final_image, label
