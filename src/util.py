import configparser
import json
import logging
import re
from json import JSONDecodeError
from typing import Optional

import xmltodict
from xml.parsers.expat import ExpatError

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
                config.optionxform = configparser_keep_keystring #do this if you do not want to read in data as lowercase
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
        
def configparser_keep_keystring(optionstr: str) -> str:
    '''
    normally the configparser would convert keys to lowercase
    we override this default function by a function that leaves the keys untouched
    :param optionstr: 
    :return: 
    '''
    return optionstr