from typing import List

from src.model.RunMD import RunMD
from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.parser.RunMD_Parser import RunMD_Parser
from src.parser.SetupMD_Parser import SetupMD_Parser
from src.model.SetupMD import SetupMD
from src.parser.mapping_util import map_a_dict
from src.Preprocessor import Preprocessor
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.resources.maps.mapping import setup_zeiss
from src.util import normalize_path, input_to_dict
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
import re


class Atlas3dParser(SetupMD_Parser, RunMD_Parser):

    @staticmethod
    def supported_input_sources() -> List[str]:
        return ["Zeiss Auriga"]

    def __init__(self):
        self.internal_mapping = input_to_dict(setup_zeiss.read_text())

    def parse_run(self, payload) -> tuple[RunMD, str]:
        parsed = self._read_input(payload)

        resultMD = parsed["ATLAS3D-Job"]["ATLAS3D-Run"]

        runMD = RunMD()

        pattern_to_DatasetType = r"^Filename(?:[A-Z])?$"

        for imgmd in resultMD["Image"]:
            image_fields = list(imgmd.keys())
            #print("===image_fields===>",image_fields)
            matchingFilenames = [elem for elem in image_fields if re.match(pattern_to_DatasetType, elem)]
            #print("==matchingFilenames==>",matchingFilenames)
            if len(matchingFilenames) != 0:
                for field in matchingFilenames:

                    if imgmd.get(field) and imgmd.get(field).split("\\")[0] in DatasetType:
                        fp = normalize_path(imgmd.get(field))
                        img = TOMO_Image(localPath=fp)
                        runMD.add_image(img, DatasetType(imgmd.get(field).split("\\")[0]))

        return runMD, parsed


    def parse_setup(self, payload) -> tuple[SetupMD, dict]:
        parsed = self._read_input(payload)

        mapping_dict = self.internal_mapping
        ac_md = map_a_dict(parsed, mapping_dict)

        Preprocessor.normalize_all_units(ac_md)

        acquisition = self._create_acquisition(ac_md)

        # Ensure datasets is always a list
        datasets = self._create_datasets(ac_md)
        #print(datasets)

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
        # Ensure instrument.eBeam.apertureSetting.size is properly formatted
        #if "instrument" in ds_dict and "eBeam" in ds_dict["instrument"]:
            #eBeam = ds_dict["instrument"]["eBeam"]
            #if "apertureSetting" in eBeam and "size" in eBeam["apertureSetting"]:
                #size_value = eBeam["apertureSetting"]["size"]
                #if isinstance(size_value, str):  # Convert only if it's a string
                    #eBeam["apertureSetting"]["size"] = self._parse_aperture_size(size_value)

        # Create the Dataset object with validated data
        ds = Dataset(**ds_dict)
        return ds

    def _parse_aperture_size(self, size_str):
        """
        Converts apertureSetting mapped value '[1] 30 µm (5.0 kV)' into a dictionary with value and unit.
        """
        apertureSetting_size_pattern = r"\[\d+\]\s*(\d+)\s*(µm|mm|nm)\s*(?:\[.*?\])?\s*\(([\d\.]+)\s*kV\)"
        match = re.match(apertureSetting_size_pattern, size_str)
        if match:
            return {
                "value": int(match.group(1)),
                "unit": "um"
            }
        return size_str

    @staticmethod
    def retrievable_datasets():
        return False

    @staticmethod
    def expected_input_format():
        return "text/xml"