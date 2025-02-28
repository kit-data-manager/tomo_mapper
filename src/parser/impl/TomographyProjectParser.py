from typing import List

from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SetupMD import SetupMD
from src.parser.SetupMD_Parser import SetupMD_Parser
from src.parser.mapping_util import map_a_dict
from src.resources.maps.mapping import setup_tescan
from src.util import input_to_dict


class TomographyProjectParser(SetupMD_Parser):

    @staticmethod
    def supported_input_sources() -> List[str]:
        return ['Tescan Solaris']

    def __init__(self):
        self.internal_mapping = input_to_dict(setup_tescan.read_text())

    def parse_setup(self, payload) -> tuple[SetupMD, dict]:
        parsed = self._read_input(payload)

        mapping_dict = self.internal_mapping
        ac_md = map_a_dict(parsed, mapping_dict)
        acquisition = self._create_acquisition(ac_md)
        datasets = self._create_datasets(ac_md)
        if not datasets:
            return acquisition, parsed

        if len(datasets) == 1:
            acquisition.dataset_template = datasets[0]
        else:
            acquisition.datasets = datasets
        return SetupMD(acquisition_metadata=acquisition), parsed

    def _create_acquisition(self, ac_md) -> Acquisition:

        ac_md_format = {
            "genericMetadata": ac_md["genericMetadata"]
        }

        acquisition = Acquisition(**ac_md_format)
        #datasets = self._create_datasets(metadata_dict)
        #acquisition.datasets = datasets
        return acquisition

    def _create_datasets(self, ac_md) -> list:
        datasets = []
        for ds in ac_md["dataset"]:
            datasets.append(self._create_dataset(ds))
        return datasets

    def _create_dataset(self, ds_dict) -> Dataset:
        ds = Dataset(**ds_dict)
        return ds


    @staticmethod
    def retrievable_datasets():
        return True

    @staticmethod
    def expected_input_format():
        return "xml"



