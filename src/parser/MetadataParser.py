from abc import ABC, abstractmethod
import xmltodict
import json
import logging

from src.model.Acquisition import Acquisition


class MetadataParser(ABC):

    def __init__(self):
        self.parsed_data = None

    def get_parsed_data(self):
        return self.parsed_data

    @staticmethod
    @abstractmethod
    def expected_input_format():
        pass

    @staticmethod
    @abstractmethod
    def retrievable_datasets():
        """
        :param self:
        :return: true if the metadata in question provides information about the datasets, false otherwise
        """
        pass

    def _read_input(self, payload):
        """
        creates metadata dictionary from payload
        :param payload: input String
        :return: metadata dict
        """
        if self.expected_input_format() == "xml":
            self.parsed_data = xmltodict.parse(payload)
            return self.parsed_data
        if self.expected_input_format() == "json":
            self.parsed_data = json.loads(payload)
            return self.parsed_data
        logging.error("Parsing of input format not implemented: {}",format(self.expected_input_format()))
        return None

    @abstractmethod
    def parse(self, payload) -> (Acquisition, str):
        """
        derives a basic acquisition object from the payload
        :param payload:
        :return:
        """
        pass