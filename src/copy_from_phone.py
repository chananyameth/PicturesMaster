import subprocess
import logging
import os

from src.file_operations import walking, normalize_extensions
from src.global_config import LOCAL_ROOT_FOLDER, TEMP_FOLDER
from src.status_history import StatusHistory
from src.file_utils.consts import PHONE_PICTURES_PATH

logger = logging.getLogger(__name__)

TEMP_FOLDER_FROM_PHONE = os.path.join(TEMP_FOLDER, "from_phone")
StatusHistory.add_on_update_handler_newly_added(logger.info)

def get_phone_list() -> set:
    """Get filename of all pictures in phone's main pictures folder"""
    commands = [f"ls -1 {PHONE_PICTURES_PATH}\n"]
    output = subprocess.check_output([r"C:\Chananya\Software\adb\adb.exe", "shell", *commands])
    return {line.decode("utf-8") for line in output.split(b'\r\n')}


def get_local_list(folder: str = LOCAL_ROOT_FOLDER) -> set:
    """Get filename of all pictures in local pictures folder & sub-folders"""
    return set(walking(folder, full_path=False))


def get_files_to_copy(phone_list: set, local_list: set) -> set:
    return phone_list - local_list


def copy_diff(files_to_copy: set, dest: str = TEMP_FOLDER_FROM_PHONE) -> None:
    for filename in files_to_copy:
        if not filename or filename.endswith('/'):
            continue
        # TODO: make sure copy into folder, not overriding
        subprocess.check_output([r"C:\Chananya\Software\adb\adb.exe", "pull",
                                 f'{PHONE_PICTURES_PATH}/{filename}',
                                 dest])


def standardize_names(folder: str = TEMP_FOLDER_FROM_PHONE) -> None:
    normalize_extensions(folder)


def copy_from_phone():
    phone_list = get_phone_list()
    StatusHistory.add_record(f'Got phone list, len={len(phone_list)}')

    local_list = get_local_list()
    StatusHistory.add_record(f'Got local list, len={len(local_list)}')

    files_to_copy = get_files_to_copy(phone_list, local_list)
    StatusHistory.add_record(f'Copying diff files, len={len(files_to_copy)}')
    copy_diff(files_to_copy)

    StatusHistory.add_record('standardizing names')
    standardize_names()
    # flat_to_tree()
    subprocess.Popen(f'explorer {TEMP_FOLDER_FROM_PHONE}')
