import hashlib
import logging
import os
import pathlib

from .consts import *

logger = logging.getLogger(__name__)


def _walking(path=root_path):
    """walk through dir, get full path"""
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


def get_md5(path):
    """calculate md5 of a file"""
    with open(path, 'rb') as file:
        md5_hash = hashlib.md5()
        content = file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return digest


def create_photos_md5_file(path=root_path, mode='a'):
    output_filename = os.path.join('md5', os.path.normpath(path).replace(os.sep, '_'), '.md5.txt')

    with open(output_filename, mode, encoding='utf8') as output_file:
        for image_path in _walking(path):
            if pathlib.Path(image_path).suffix not in photos_extensions:
                logger.info(f"md5: Skipped file for unknown extension: {image_path}")
                continue

            output_file.write('{},{}\n'.format(get_md5(image_path), image_path))


def get_duplicate_md5s(md5_file_path):
    """
    Search an .md5.txt file for duplicate md5s
    return list of (md5, path) duplicates
    """
    duplicates = []
    exist = set()

    with open(md5_file_path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            md5, path = line.split(',')[0]
            if md5 in exist:
                duplicates.append((md5, path))
            else:
                exist.add(md5)

    return duplicates
