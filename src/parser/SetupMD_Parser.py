from abc import ABC, abstractmethod
import logging
from typing import Tuple

from src.model.SetupMD import SetupMD
from src.parser.MetadataParser import MetadataParser


class SetupMD_Parser(MetadataParser):

    @staticmethod
    @abstractmethod
    def retrievable_datasets():
        """
        :param self:
        :return: true if the metadata in question provides information about the datasets, false otherwise
        """
        pass

    @abstractmethod
    def parse_setup(self, payload) -> Tuple[SetupMD, dict]:
        """
        derives a basic acquisition object from the payload
        :param payload:
        :return:
        """
        pass