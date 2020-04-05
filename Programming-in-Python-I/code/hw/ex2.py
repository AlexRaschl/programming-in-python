"""ex2.py
Author: Alexander Raschl
Matr.Nr.: K01556188
Exercise 2
"""
from PIL import Image
import os
from glob import glob
import numpy as np
import shutil
from tqdm import tqdm
from joblib import hash


def verify_files(input_dir: str, output_dir: str, logfile: str) -> int:
    if not os.path.isdir(input_dir):
        return -1
    os.makedirs(output_dir, exist_ok=True)
    if os.path.dirname(logfile):
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
    hashes = []
    serial = [1]

    log_handle = open(logfile, 'w')

    def write_log(filename: str, err: int):
        log_handle.write(f"{os.path.relpath(filename, os.path.abspath(input_dir))};{err}\n")

    # Check if file has the specified properties
    def process_file(filename):
        if os.path.splitext(filename)[1] not in ('.jpg', '.jpeg', '.JPEG', '.JPG'):
            return write_log(filename, 1)
        if os.path.getsize(filename) <= 10e3:
            return write_log(filename, 2)
        try:
            img = np.asarray(Image.open(filename))
            if img.var() <= 0:
                return write_log(filename, 4)
            if len(img.shape) != 2 and img.shape <= (100, 100):
                return write_log(filename, 5)

            img_hash = hash(bytes(img))
            if img_hash not in hashes:
                hashes.append(img_hash)
                shutil.copy(filename, os.path.join(output_dir, "{serial:06d}.jpg".format(serial=serial[0])))
                serial[0] += 1
            else:
                return write_log(filename, 6)

        except IOError:
            return write_log(filename, 3)

    # For all files in directory call process function
    for name in tqdm(sorted(glob(os.path.join(input_dir, "**/*"), recursive=True))):
        if os.path.isfile(name):
            process_file(name)

    if not log_handle.closed:
        log_handle.close()


if __name__ == '__main__':
    in_dir = "H:/Datasets/python2/Dataset/dataset_part_1"
    out_dir = "H:/Datasets/python2/Dataset/dataset_out_1"
    verify_files(in_dir, out_dir, 'log.txt')
