from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.parser.MetadataParser import MetadataParser

class Atlas3dParser(MetadataParser):

    def parse(self, payload) -> Acquisition:
        parsed = self._read_input(payload)
        acquisition = self._create_acquisition(parsed)
        return acquisition

    def _create_acquisition(self, metadata_dict) -> Acquisition:
        acquisition = Acquisition()
        return acquisition

    @staticmethod
    def retrievable_datasets():
        return False

    @staticmethod
    def expected_input_format():
        return "xml"



