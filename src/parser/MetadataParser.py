from abc import ABC, abstractmethod
from typing import List, Optional
from io import StringIO

import xmltodict
import json
import logging

import configparser
#from configparser import ConfigParser, NoInterpolation

class MetadataParser(ABC):

    @staticmethod
    @abstractmethod
    def expected_input_format() -> str:
        pass

    @staticmethod
    @abstractmethod
    def supported_input_sources() -> List[str]:
        """
        Provides informative output about the input sources that are supported by implementation of this parser.
        The output is not specified and should only be used for informative reasons (such as logging and printing)
        :return:
        """
        pass
    
    def _read_input(self, payload) -> Optional[dict]:
        """
        creates metadata dictionary from payload
        :param payload: input String
        :return: metadata dict
        """
        if self.expected_input_format() == "text/xml":
            self.parsed_data = xmltodict.parse(payload)
            return self.parsed_data
        if self.expected_input_format() == "application/json":
            self.parsed_data = json.loads(payload)
            return self.parsed_data
        if self.expected_input_format() == "text/plain":
            
            def keep_keystring(optionstr: str) -> str:
                '''
                normally the configparser would convert keys to lowercase
                we override this default function by a function that leaves the keys untouched
                :param optionstr: 
                :return: 
                '''
                return optionstr
            
            self.parsed_data = {}
            config = configparser.ConfigParser(interpolation=configparser.Interpolation()) # disables interpolation explicitly
            config.optionxform = keep_keystring # do this if you do not want to read in data as lowercase
            config.read_string(payload)
            for section in config.sections():
                items = config.items(section)
                self.parsed_data[section] = dict(items)
            return self.parsed_data
        logging.error("Parsing of input format not implemented: {}",format(self.expected_input_format()))
        return None