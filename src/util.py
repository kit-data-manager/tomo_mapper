import json
import logging
from pathlib import Path

from magika import Magika
import os
import tempfile
import time
from json import JSONDecodeError
from typing import Optional
import configparser

import requests
import zipfile

import xmltodict
from xml.parsers.expat import ExpatError

from src.IO.MappingAbortionError import MappingAbortionError
import re

def robust_textfile_read(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding="latin1") as file:
                return file.read()
        except UnicodeDecodeError:
            logging.error("Unable to determine file encoding. Aborting.")
            #TODO: since it is not clear who calls this function for what, it may make more sense to raise a unified error to handle instead of error for exit
            raise MappingAbortionError("File loading failed due to encoding.")

def load_json(source) -> dict:
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
        return json.loads(robust_textfile_read(source))

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

def input_to_dict(stringPayload, stick_to_wellformed=False) -> Optional[dict]:
    """
    best effort parsing of usual input formats. extend if needed
    :param stringPayload: string to parse
    :return: dict on success, None otherwise
    """
    if type(stringPayload) is not str:
        return None
    try:
        if stringPayload.startswith("<"):
            try:  # XML
                return xmltodict.parse(stringPayload)
            except ExpatError:
                logging.debug("Reading in input as xml not successful")
        if stringPayload.startswith("{"):
            try: #JSON
                return json.loads(stringPayload)
            except JSONDecodeError:
                logging.debug("Reading input as json not successful")
        if stringPayload.startswith("["): #could still be json, but would not create a dict so not a valid input anyway
            try: #INI
                dict_from_ini = {}
                config = configparser.ConfigParser()
                config.optionxform = str #do this if you do not want to read in data as lowercase
                config.read_string(stringPayload)
                for section in config.sections():
                    items = config.items(section)
                    dict_from_ini[section] = dict(items)
                return dict_from_ini
            except (configparser.NoSectionError, configparser.NoOptionError):
                logging.debug("Reading input as INI not successful")
        if stringPayload.startswith("$"):  # Check if the input starts with "$"
            try: #TXT
                dict_from_txt = {}
                lines = stringPayload.strip().split("\n") # Split the input into lines and process them
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    match = re.match(r"^(\${1,2}[\w_]+)\s+(.*)", line) # Use regex to extract key-value pairs from lines starting with $ or $$
                    if match:
                        key, value = match.groups()
                        dict_from_txt[key] = value.strip()  # Store key-value pairs in dictionary
                return dict_from_txt
            except Exception as e:
                logging.debug(f"Reading input as txt not successful: {e}")
        if not stick_to_wellformed and "\n" in stringPayload: #We try our best, but if this is not wanted, please stick to wellformed formats instead
            output_dict = {}
            data = stringPayload.replace("\r", "")
            lines = data.split("\n")
            for l in lines:
                if "=" in l:
                    k, v = l.split("=", 1)
                    output_dict[k.strip().replace(".", "")] = v.strip()
                else:
                    if ":" in l:
                        k, v = l.split(":", 1)
                        output_dict[k.strip().replace(".", "")] = v.strip()
            if output_dict: return output_dict
        logging.warning("Best effort input reading failed. Necessary reader not implemented?")
    except Exception as e:
        logging.warning("Best effort input reading failed with unexpected error. Input malformed?")
        logging.error(e)

def normalize_path(pathString):
    if "\\" in pathString: return os.path.join(*pathString.split("\\"))
    return pathString

def get_filetype_with_magica(filepath):
    m = Magika()
    res = m.identify_path(Path(filepath))
    return res.output.mime_type
