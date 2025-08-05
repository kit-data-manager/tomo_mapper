from abc import abstractmethod
from typing import Tuple

from src.model.RunMD import RunMD
from src.parser.MetadataParser import MetadataParser


class RunMD_Parser(MetadataParser):

    @abstractmethod
    def parse_run(self, payload) -> RunMD:
        """
        derives setup md from metadata file
        :param self:
        :param payload:
        :return:
        """
        pass