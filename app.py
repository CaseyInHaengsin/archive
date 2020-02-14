import os
import glob
import shutil
import sys
import time
import logbook

# absolute path
location = '//'
app_log = logbook.Logger('app')


def main():
    # File extensions that you would like to archive
    file_extensions = ['xlsx', 'csv', 'zip', 'xml', 'html', 'json', 'pdf', 'pptx']

    filename = 'auto-archive.txt'
    init_logging(filename)

    archive_location = make_archive_folder()
    #get_files_to_archive_files(location, file_extensions)
    files_to_move = get_files_to_archive_files(location, file_extensions)
    folders_to_move = identify_folders(location)
    all_things_to_move = combine_lists(files_to_move, folders_to_move)
    move_files(archive_location, all_things_to_move)
    move_log(archive_location, filename)
    wrap_up(archive_location)


def move_log(archive_location, log_file):
    """
    This function is used to move the log file into the archive location
    param1: archive_location
    param2: log_file

    """
    try:
        shutil.move(log_file, archive_location)
    except Exception as e:
        app_log.warn(e)
    finally:
        msg = f"moved log file to {archive_location}"
        app_log.notice(msg)


def wrap_up(archive_location):
    """
    This function creates a zip and deletes the uncompressed folder
    """
    try:
        shutil.make_archive(f"{archive_location}",
                            'zip', f"{archive_location}")
        shutil.rmtree(f'{archive_location}')
    except Exception as x:
        print(x)
    finally:
        msg = 'Archiving completed'
        app_log.notice(msg)


def make_archive_folder():
    """
    This function creates an archive folder
    return: archive location
    """
    try:
        place_to_archive = f'{location}{time.asctime()}_archive'
        os.mkdir(place_to_archive)
    except Exception as x:
        # TODO - Log exception
        app_log.warn(x)
    finally:
        return place_to_archive


def get_files_to_archive_files(location, file_extensions):
    """
    This function will look for files with the extensions provided in the file_extensions list
    param1: location
    param2: file extensions
    return: all_files_to_move

    """
    all_files_to_move = []

    try:
        for x in file_extensions:
            items_to_move = f"{location}/*.{x}"
            try:
                for item in glob.glob(items_to_move):
                    all_files_to_move.append(item)
            except Exception as x:
                app_log.warn(x)
                continue
    except Exception as x:
        app_log.warn(x)
    finally:
        app_log.notice(
            f'Completed getting all files. Files found include {all_files_to_move}')
        return all_files_to_move


def identify_folders(location):
    """
    This function looks for folders where string values contain a value
    param1: location
    return: folders
    """
    get_all_folders = [f.path for f in os.scandir(location) if f.is_dir()]
    folders_to_move = []
    try:
        for fol in get_all_folders:
            if fol.__contains__('provision'):
                folders_to_move.append(fol)
            elif fol.__contains__('data'):
                folders_to_move.append(fol)
            elif fol.__contains__('transfer'):
                folders_to_move.append(fol)
            elif fol.__contains__('untitled'):
                folders_to_move.append(fol)
            elif fol.__contains__('test'):
                folders_to_move.append(fol)
            else:
                msg = f'No folders to archive.'
                app_log.notice(msg)
    except Exception as x:
        app_log.warn(x)
    finally:
        msg = f"Finished searching folders. The following were found. {folders_to_move}"
        app_log.notice(msg)
        return folders_to_move


def combine_lists(*list_arr):
    """
    This function combines the folders and files
    param1: list_arr
    """
    try:
        all_to_archive = [y for x in list_arr for y in x]
    except Exception as x:
        app_log.warn(x)
    finally:
        msg = f"Finished combining list. The following found: {all_to_archive}"
        return all_to_archive


def move_files(archive_path, arr_move):
    try:
        for item in arr_move:
            shutil.move(item, archive_path)
        #shutil.move(files_arr, archive_path)
    except Exception as x:
        # TODO - Add logging here
        app_log.warn(x)
    finally:
        msg = 'moving files completed'
        app_log.notice(msg)


def init_logging(filename: str = None):
    level = logbook.TRACE
    if filename:
        logbook.TimedRotatingFileHandler(
            filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    # TODO - Add start message
    msg = 'Logging initialized, level: {}, mode: {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename
    )
    logger = logbook.Logger('Startup')
    logger.notice(msg)


if __name__ == '__main__':
    main()
