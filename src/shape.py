import numpy as np
import cv2


def circle(image_size, scale, orientation, position_scale):
    img = np.zeros(image_size, dtype=np.float32)
    x_scale = position_scale[0]
    y_scale = position_scale[1]

    # calculate the radius and center of the circle
    radius = int(scale * min(image_size) / 2)
    center_x = int(x_scale * image_size[1])
    center_y = int(y_scale * image_size[0])
    # draw the circle
    cv2.circle(img, (center_x, center_y), radius, (1,), -1)
    # rotate the image if orientation is not zero
    if orientation != 0:
        rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), orientation, 1)
        img = cv2.warpAffine(img, rotation_matrix, (image_size[1], image_size[0]))

    return img


def square(image_size, scale, orientation, position_scale):
    img = np.zeros(image_size, dtype=np.float32)
    x_scale = position_scale[0]
    y_scale = position_scale[1]

    # calculate the half-length of the side
    side = int(scale * min(image_size) / 2)
    start_x = int(x_scale * image_size[1] - side / 2)
    start_y = int(y_scale * image_size[0] - side / 2)
    end_x = start_x + side
    end_y = start_y + side
    # draw the square
    cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (1,), -1)
    # rotate the image if orientation is not zero
    if orientation != 0:
        center_x = int(x_scale * image_size[1])
        center_y = int(y_scale * image_size[0])
        rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), orientation, 1)
        img = cv2.warpAffine(img, rotation_matrix, (image_size[1], image_size[0]))

    return img


def triangle(image_size, scale, orientation, position_scale):
    img = np.zeros(image_size, dtype=np.float32)
    x_scale = position_scale[0]
    y_scale = position_scale[1]

    # calculate the half-length of the side of the triangle
    side = int(scale * min(image_size) / 2)
    half_side = side // 2
    start_x = int(x_scale * image_size[1])
    start_y = int(y_scale * image_size[0])
    # define the vertices of the triangle
    vertices = np.array(
        [
            [start_x, start_y - half_side],
            [start_x - half_side, start_y + half_side],
            [start_x + half_side, start_y + half_side],
        ],
        np.int32,
    )
    vertices = vertices.reshape((-1, 1, 2))
    # draw the triangle
    cv2.fillPoly(img, [vertices], (1,))
    # rotate the image if orientation is not zero
    if orientation != 0:
        center_x = int(x_scale * image_size[1])
        center_y = int(y_scale * image_size[0])
        rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), orientation, 1)
        img = cv2.warpAffine(img, rotation_matrix, (image_size[1], image_size[0]))

    return img


def combine_shapes(image_size, shape_images):
    canvas = np.zeros(image_size, dtype=np.float32)
    for shape in shape_images:
        canvas = np.maximum(canvas, shape)

    return canvas


def check_overlapping(shape_image1, shape_image2):
    overlap = np.logical_and(shape_image1 > 0, shape_image2 > 0)
    return np.any(overlap)


def check_cropping(shape_image):
    height, width = shape_image.shape

    # check top, bottom, left, and right boundaries for any non-zero pixels
    if (
        np.any(shape_image[0, :] != 0)
        or np.any(shape_image[height - 1, :] != 0)
        or np.any(shape_image[:, 0] != 0)
        or np.any(shape_image[:, width - 1] != 0)
    ):
        return True
    return False
