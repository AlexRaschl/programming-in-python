"""ex3.py
Author: Alexander Raschl
Matr.Nr.: K01556188
Exercise 3
"""

from PIL import Image
import numpy as np
from tqdm import tqdm
from pathlib import Path


class ImageNormalizer:
    def __init__(self, input_dir: str):
        self.file_names = self.__fetch_names(input_dir)

    # retrieve mean and std for all images
    def get_stats(self):
        stats = np.array([self.__get_img_stats(file) for file in tqdm(self.file_names)], dtype=np.float64)
        return np.array(stats[:, 0]), np.array(stats[:, 1])

    # Fetch all filenames from dir
    def __fetch_names(self, input_dir):
        return sorted(Path.glob(Path(input_dir), pattern='*.jpg'))

    # Get mean and std for an image
    def __get_img_stats(self, filename):
        img = np.asarray(Image.open(filename))
        return img.mean(), img.std()

    # Return Generator of normalized image data
    def get_images(self):
        for idx, file in enumerate(self.file_names):
            img = np.asarray(Image.open(file), np.float32)
            yield (img - img.mean()) / img.std()


if __name__ == '__main__':
    img_norm = ImageNormalizer("H:/Datasets/python2/Dataset/dataset_out_1")
    for img in img_norm.get_images():
        print(img.mean())
        print(img.var())
