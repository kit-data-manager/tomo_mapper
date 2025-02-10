from abc import ABC, abstractmethod
import xmltodict
import json
import logging

class MetadataParser(ABC):

    @staticmethod
    @abstractmethod
    def expected_input_format():
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