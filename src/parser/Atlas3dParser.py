from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.parser.SetupMD_Parser import SetupMD_Parser

class Atlas3dParser(SetupMD_Parser):

    def parse_setup(self, payload) -> Acquisition:
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



