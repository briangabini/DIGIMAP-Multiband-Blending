import imageio
import numpy as np

import implementation


def read_image(path) -> np.ndarray:
    data = imageio.imread(path)
    return np.array(data) / 255


def read_mask(path) -> np.ndarray:
    image = read_image(path)
    return image.mean(axis=2)


def write_image(image: np.ndarray, path):
    image = (image - image.min()) / (image.max() - image.min())
    image = image * 255
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    imageio.imwrite(path, image)


def compute_num_levels(image: np.ndarray):
    h, w, c = image.shape
    return int(np.floor(np.log2(min(h, w))))


if __name__ == "__main__":
    target = read_image("target.jpg")
    source = read_image("source.jpg")
    mask = read_mask("mask.jpg")

    blender = implementation.MultiBandBlending(num_levels=compute_num_levels(target))
    composite = blender(target, source, mask)
    write_image(composite, "multiband.jpg")

    blender = implementation.NaiveBlending()
    composite = blender(target, source, mask)
    write_image(composite, "naive.jpg")
