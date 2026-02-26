from abc import abstractmethod

from src.model.SetupMD import SetupMD
from mappingservice_plugincore.mappingservice_plugincore.parser.MetadataParser import MetadataParser


class SetupMD_Parser(MetadataParser):

    @staticmethod
    @abstractmethod
    def retrievable_datasets() -> bool:
        """
        :param self:
        :return: true if the metadata in question provides information about the datasets, false otherwise
        """
        pass
    
    # TODO: currently all parse_setup methods are duplicates, because the real work is done in the internal creation methods. Move method implementation to here
    @abstractmethod
    def parse_setup(self, payload) -> SetupMD:
        """
        derives a basic acquisition object from the payload
        :param payload:
        :return:
        """
        pass