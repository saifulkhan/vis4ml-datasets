import os
import json
import numpy as np
from PIL import Image
from tqdm import tqdm
import concurrent.futures

from .utils import draw_fixed_numbers, draw_sample, read_distribution, read_metadata
import time
from itertools import combinations
from .shape import (
    circle,
    square,
    triangle,
    combine_shapes,
    check_overlapping,
    check_cropping,
)

shape_functions = {"circle": circle, "square": square, "triangle": triangle}


class Generator:
    def __init__(self, metadata, distribution):
        self.metadata = metadata
        self.distribution = distribution
        print("Generator initialized with the following parameters:")
        print(f"distribution: {distribution}")
        print(f"metadata: {metadata}")

        self.output_dir = (
            f"{self.metadata['output_dir']}/{self.metadata['output_prefix']}"
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_images(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            start_time = time.time()

            for i in tqdm(range(self.metadata["num_images"])):
                future = executor.submit(self.generate_image)
                futures.append(future)
                # print(f"{i=}")

            for i, future in enumerate(
                tqdm(
                    concurrent.futures.as_completed(futures),
                    total=self.metadata["num_images"],
                )
            ):
                try:
                    image, label = future.result()
                    self.save(i, image, label)
                except Exception as e:
                    print(f"Error occurred while processing image {i}: {str(e)}")

            # print(f".{i=}")
            end_time = time.time()
            total_time = end_time - start_time
            print(
                f"Total time taken: {total_time} seconds for {self.metadata['num_images']} images."
            )

    def generate_image(self):
        image_size = (self.metadata["image_height"], self.metadata["image_width"])

        images = []
        label = []

        for _ in range(self.metadata["num_shapes"]):
            while True:
                shape = draw_sample(self.distribution["shape"], 1)[0]
                scale = draw_sample(self.distribution["scale"], 1)[0]
                pos_x = draw_sample(self.distribution["pos_x"], 1)[0]
                pos_y = draw_sample(self.distribution["pos_y"], 1)[0]
                rotation = draw_sample(self.distribution["rotation"], 1)[0]
                position_scale = (pos_x, pos_y)

                shape_img = shape_functions[shape](
                    image_size, scale, rotation, position_scale
                )

                if self.metadata["shape_cropping"] != check_cropping(shape_img):
                    continue

                # TODO this does not work when shape_overlapping: true. This hangs the code.
                # overlapped = False
                # for existing_shape in images:
                #     overlapped = check_overlapping(existing_shape, shape_img)
                #     if self.metadata["shape_overlapping"] != overlapped:
                #         break

                # if self.metadata["shape_overlapping"] != overlapped:
                #     continue

                label.append(
                    {
                        "shape": shape,
                        "scale": scale.item(),
                        "pos_x": pos_x.item(),
                        "pos_y": pos_y.item(),
                        "rotation": rotation.item(),
                        "shape_cropping": self.metadata["shape_cropping"],
                    }
                )
                images.append(shape_img)

                break

        # for img1, img2 in combinations(images, 2):
        #     shape_overlapping = check_overlapping(img1, img2)
        #     if shape_overlapping is True:
        #         label.append({"shape_overlapping": True})
        #         break
        # else:
        #     label.append({"shape_overlapping": False})

        final_image = combine_shapes(image_size, images)

        if self.metadata["color_type"] == "grey":
            final_image = final_image * np.random.randint(
                self.distribution["grey"][0], self.distribution["grey"][1]
            )

        return final_image, label

    def save(self, idx, image, label):

        img_pil = Image.fromarray((image * 255).astype(np.uint8))
        img_filename = os.path.join(self.output_dir, f"image_{idx}.png")
        img_pil.save(img_filename)

        label_filename = os.path.join(self.output_dir, f"label_{idx}.json")
        with open(label_filename, "w") as f:
            json.dump(label, f, indent=2)
