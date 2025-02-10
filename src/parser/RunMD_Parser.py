from abc import abstractmethod

from src.model.RunMD import RunMD
from src.parser.MetadataParser import MetadataParser


class RunMD_Parser(MetadataParser):

    @staticmethod
    @abstractmethod
    def parse_run(self, payload) -> tuple[RunMD, dict]:
        """
        derives setup md from metadata file
        :param self:
        :param payload:
        :return:
        """
        pass