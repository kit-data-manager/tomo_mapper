from abc import abstractmethod

from src.model.RunMD import RunMD
from src.parser.MetadataParser import MetadataParser


class RunMD_Parser(MetadataParser):

    @abstractmethod
    def parse_run(self, payload) -> (RunMD, str):
        pass