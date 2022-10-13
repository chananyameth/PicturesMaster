import datetime
import hashlib
import glob
import pathlib
import os
import re
import shutil
import sys
import time
from collections.abc import Iterable
from os.path import join, getsize
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

from consts import *


def write_to_file(what, file_name, mode='w'):
    with open(file_name, mode, encoding='utf8') as file:
        if isinstance(what, Iterable):
            for line in what:
                file.write('{!r}'.format(line))
                file.write('\n')
        else:
            file.write(what)


def walking(path=root_path):
    """walk through dir, get full path"""
    for root, dirs, files in os.walk(path):
        # size = sum(getsize(join(root, name)) for name in files)
        # num = len(files)
        # print(f'{root} consumes {size} bytes in {num} non-directory files')
        # if 'CVS' in dirs:
        #    dirs.remove('CVS')  # don't visit CVS directories
        for file in files:
            yield join(root, file)


def get_md5(path):
    """calculate md5 of a file"""
    with open(path, 'rb') as file:
        md5_hash = hashlib.md5()
        content = file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        return digest


def create_photos_md5_file(path=root_path, mode='a', output_file_name='md5s.txt'):
    with open(output_file_name, mode, encoding='utf8') as output:
        for a_path in walking(path):
            if pathlib.Path(a_path).suffix not in photos_extensions:
                continue

            output.write('{},{}\n'.format(get_md5(a_path), a_path))


def get_duplicates(path):
    """Search a file for duplicate lines, and return them"""
    duplicates = []
    exist = []
    with open(path, 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            if line.split(',')[0] in exist:
                duplicates.append(line)
            else:
                exist.append(line.split(',')[0])
    return duplicates


def get_all_extensions(root=pictures_library):
    extensions = set()
    for path in walking(root):
        extensions.add(pathlib.Path(path).suffix)

    return extensions


def normalize_extensions(root=pictures_library):
    """Run over all files in root, and lower-case every extension"""
    for path in walking(root):
        suff = pathlib.Path(path).suffix
        if not suff.islower():
            os.renames(path, path[:-len(suff)] + suff.lower())


def create_extensions_file():
    write_to_file(get_all_extensions(), 'extensions.txt')


def find_synced_directorys(path_to_check, path_to_check_against_md5s):
    exist_md5s = []

    with open(path_to_check_against_md5s, 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            exist_md5s.append(line.split(',')[0])

    missing = []
    for root, dirs, files in os.walk(path_to_check, topdown=False):
        exist = 0
        for file in files:
            if get_md5(join(root, file)) in exist_md5s:
                exist += 1
            else:
                missing.append(join(root, file))
        print('{}/{} files already exist in {}'.format(exist, len(files), root))
    for item in missing:
        print(item)


def get_earliest_exif_time(file):
    im = Image.open(file)
    exif = im.getexif()
    # DateTime, DateTimeOriginal, DateTimeDigitized
    dates_keys = [306, 36867, 36868]

    times = [datetime.datetime(2500, 1, 1)]
    for key in dates_keys:
        if exif.get(key):
            ints = map(lambda x: int(x), re.findall(r'(\d+)', exif.get(key)))
            times.append(datetime.datetime(*ints))
    return min(times)


def handle_files_unknown_date(all_files):
    """in: list of paths of files with unknown date"""
    try:
        files = []
        for file in all_files:
            creation_time = time.gmtime(os.path.getctime(file))
            modification_time = time.gmtime(os.path.getmtime(file))
            exif_time = get_earliest_exif_time(file).timetuple()

            t = min(creation_time, modification_time, exif_time)
            files.append((file, t.tm_year, t.tm_mon, t.tm_mday))

        handle_files_known_date(files)
    except Exception as e:
        print('Error in handle_files_unknown_date!')
        input(e)


def handle_files_known_date(path_date):
    """in: list of tuples (path, year, month, day) of files with known date"""
    for path, year, month, day in path_date:
        dst_dir = join(destination_pictures_directory, str(year).zfill(2), str(month).zfill(2), str(day).zfill(2))
        if not os.path.isdir(dst_dir):
            pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)
        Path(path).rename(Path(dst_dir, Path(path).name))
        # copy2(path, Path(dst_dir, Path(path).name))


def remove_empty_directories(path, remove_root=True):
    if not os.path.isdir(path):
        return

    # remove empty subdirectories
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_directories(fullpath)

    # if directory empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        os.rmdir(path)
