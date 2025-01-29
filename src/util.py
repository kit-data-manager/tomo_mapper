import json
import logging
import os
import shutil
import tempfile
import time

import requests
import zipfile

def load_json(source):
    """
    Load JSON data from a local file path or a web URL.

    :param source: A string representing either a local file path or a web URL.
    :return: Parsed JSON data.
    """
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    else:
        with open(source, 'r') as file:
            return json.load(file)

def is_zipfile(filepath):
    return zipfile.is_zipfile(filepath)

def extract_zip_file(zip_file_path):
    """
    extracts files of zip to a temporary directory
    :param zip_file_path: local file path to zip file
    :return: (path to contained emxml file, path to tmp dir) or (None, None) if no emxml file was found
    """
    temp_dir = tempfile.mkdtemp()

    start_time = time.time()  # Start time
    logging.info(f"Extracting {zip_file_path}...")

    target_dir = None

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        total_items = len(zip_ref.namelist())

        for index, file_name in enumerate(zip_ref.namelist(), start=1):
            # if index%10 == 0:
            #     print(f"Extracting file {index}/{total_items}...")
            file_path = os.path.join(temp_dir, file_name)
            zip_ref.extract(file_name, temp_dir)

    end_time = time.time()  # End time
    total_time = end_time - start_time

    logging.info(f"Total time taken to process: {total_time:.2f} seconds.")
    return temp_dir

def strip_workdir_from_path(workdirpath, fullpath):
    if fullpath.startswith(workdirpath):
        return fullpath.replace(workdirpath, ".", 1)
    logging.debug("Unable to remove working directory from given path. Returning unchanged path")
    return fullpath