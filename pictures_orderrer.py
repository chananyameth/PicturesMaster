import os
from os.path import join

from consts import *
from regex_stuff import find_abnormal_file_names, get_matching_re_date
from file_operations import *


def process_new_photos(path):
    if not get_all_extensions(path).issubset(all_extensions):
        raise Exception("extensions {!r} are unknown!".format(get_all_extensions(path).difference()))
    normalize_extensions(path)

    matching_files = get_matching_re_date(path=path)
    write_to_file(matching_files, 'data/_Matching files.txt', mode='a')
    handle_files_known_date(matching_files)

    non_matching_files = find_abnormal_file_names(path=path)
    if non_matching_files:
        print('Unsortable files found!')
        if input('Print their names? (y/n)').lower() == 'y':
            print(non_matching_files)
        if input('Try to handle them anyway by metadata? (y/n)').lower() == 'y':
            handle_files_unknown_date(non_matching_files)
        else:
            write_to_file(non_matching_files, '_Unable to sort these files.txt', mode='a')

    remove_empty_directories(path=path)


def make_hardlink(target_file):
    link = "new link"
    cmd_line = "mklink /H '{}' '{}'".format(link, target_file)


def main():
    # create_md5s_file(mode='w')
    # create_md5s_file(path=pictures_library, mode='w', file_name='data/pictures_library_md5.txt')
    # get_duplicates('md5s.txt')
    # find_synced_folders(root_path, 'data/pictures_library_md5.txt')
    # get_extensions()
    # print(cfo(r"C:\Users\Chananya\Desktop\pics vacation 2020\vids\20180118_001444A.mp4", "C:/a/20200812_121444A.mp4"))
    # write_to_file(find_abnormal_file_names(), 'non-match.txt')
    # write_to_file(get_matching_re_date(), 'match.txt')
    # handle_files_known_date([(r'C:\Users\Chananya\Pictures\Untitled.png', 123, 45, 6)])
    # handle_files_unknown_date([r'C:\Users\Chananya\Pictures\Untitled.png'])

    for path in sys.argv[1:]:
        process_new_photos(path)


if __name__ == '__main__':
    main()
    input('Press enter to finish')
