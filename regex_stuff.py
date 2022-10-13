import os
import re
from os.path import join

from consts import *

VALID_SUFFIX_RE = '(?:' + '|'.join(ext.strip('.').lower() for ext in photos_extensions + videos_extensions) + ')'
IGNORED_SUFFIX_RE = '(?:' + '|'.join(ext.strip('.').lower() for ext in other_extensions) + ')'

PREFIXES = (r'IMG',
            r'img',
            r'VID',
            r'PANO',
            r'Screenshot',
            r'WIN')
POSTFIXES = (r'',
             r'ANIMATION',
             r'\d{3}',
             r'WA\d{4}',
             r'Pro',
             r' \(\d+\)',
             r'\d+',
             r'timelapse_\ds',
             r'A',
             r'\d{3}\.PHOTOSPHERE')

DELIMITER_RE = r'(?:[-_/\\\.]*)?'
HEXADECIMAL_RE = r'(?:[0-9A-Fa-f])'
PREFIX_RE = r'(?:' + '|'.join(PREFIXES) + r')'
POSTFIX_RE = r'(?:' + '|'.join(POSTFIXES) + r')'

YEAR_RE = r'((?:20|19)\d{2})'  # capturing group
MONTH_RE = r'([0][0-9]|1[012])'  # capturing group
DAY_RE = r'([012][0-9]|3[01])'  # capturing group
HOUR_RE = r'(?:[01][0-9]|2[0-3])'
MINUTE_RE = r'(?:[0-5][0-9])'
SECOND_RE = MINUTE_RE
YEAR_MONTH_DAY_RE = rf'(?:{YEAR_RE}{DELIMITER_RE}{MONTH_RE}{DELIMITER_RE}{DAY_RE})'
HOUR_MINUTE_SECOND_RE = rf'(?:{HOUR_RE}{DELIMITER_RE}{MINUTE_RE}{DELIMITER_RE}{SECOND_RE})'

NAME_FORMAT_COMMON = re.compile(rf'(?:{PREFIX_RE}{DELIMITER_RE})?'
                                rf'(?:{YEAR_MONTH_DAY_RE})'
                                rf'(?:{DELIMITER_RE})?'
                                rf'(?:{HOUR_MINUTE_SECOND_RE})?'
                                rf'(?:{DELIMITER_RE}{POSTFIX_RE})?'
                                rf'(?:\.{VALID_SUFFIX_RE})')
WIN_BG_IMAGE_RE = re.compile(rf'(?:{HEXADECIMAL_RE}{{64}}\.{VALID_SUFFIX_RE})')
IGNORE_THESE_FILES = re.compile(rf'(?:.*\.{IGNORED_SUFFIX_RE})')


def get_non_matching_re(path=root_path, regexes=(NAME_FORMAT_COMMON,), skip_sorted_files=True):
    mismatches = []
    for root, dirs, files in os.walk(path):
        for file in files:
            for regex in regexes:
                if skip_sorted_files and re.search(YEAR_MONTH_DAY_RE, root):
                    break
                if regex.match(file) or re.search(YEAR_MONTH_DAY_RE, root):
                    break
            else:
                mismatches.append(join(root, file))
    return mismatches


def get_matching_re_date(path=root_path, regexes=(NAME_FORMAT_COMMON,), skip_sorted_files=True):
    """List of (path, year, month, day) for each matching file name"""
    matches = []
    for root, dirs, files in os.walk(path):
        for file in files:
            for regex in regexes:
                if skip_sorted_files and re.search(YEAR_MONTH_DAY_RE, root):
                    break
                if regex.match(file):
                    path = join(root, file)
                    year, month, day = regex.match(file).groups()
                    matches.append((path, year, month, day))
                    break
    return matches


def find_abnormal_file_names(path=root_path):
    normal_files = (NAME_FORMAT_COMMON, WIN_BG_IMAGE_RE, IGNORE_THESE_FILES)
    return get_non_matching_re(path=path, regexes=normal_files)
