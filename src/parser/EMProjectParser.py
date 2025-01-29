from typing import List

from src.model.Acquisition import Acquisition
from src.model.Dataset import Dataset
from src.parser.MetadataParser import MetadataParser


class EMProjectParser(MetadataParser):

    def parse(self, payload) -> Acquisition:
        parsed = self._read_input(payload)
        acquisition = self._create_acquisition(parsed)
        return acquisition

    def _create_acquisition(self, metadata_dict) -> Acquisition:
        program = {"programName": metadata_dict["EMProject"]["ApplicationName"], "progamVersion": metadata_dict["EMProject"]["ApplicationVersion"]}
        applicationID = {"identifierValue": metadata_dict["EMProject"]["ApplicationId"]}
        fileVersion = metadata_dict["EMProject"]["FileVersion"]
        projectName = metadata_dict["EMProject"]["ProjectName"]
        zCutSpacing = {"value": metadata_dict["EMProject"]["ZCutSpacing"]}
        numberOfCuts = metadata_dict["EMProject"]["Datasets"]["Dataset"][0]["NumberOfCuts"]
        acquisition = Acquisition(program=program, applicationID=applicationID, fileVersion=fileVersion, projectName=projectName, zCutSpacing=zCutSpacing, numberOfCuts=numberOfCuts)
        datasets = self._create_datasets(metadata_dict)
        acquisition.datasets = datasets
        return acquisition

    def _create_datasets(self, metadata_dict) -> list:
        datasets = []
        for ds in metadata_dict["EMProject"]["Datasets"]["Dataset"]:
            datasets.append(self._create_dataset(ds))
        return datasets

    def _create_dataset(self, ds_dict) -> Dataset:
        datasetType = ds_dict.get("Name")
        rows = ds_dict.get("Rows")
        columns = ds_dict.get("Columns")
        tileColumn = ds_dict["LiveAcquisition"].get("TileColumn")
        tileRow = ds_dict["LiveAcquisition"].get("TileRow")

        ds = Dataset(datasetType=datasetType, rows=rows, columns=columns, tileColumn=tileColumn, tileRow=tileRow)
        return ds


    @staticmethod
    def retrievable_datasets():
        return True

    @staticmethod
    def expected_input_format():
        return "xml"



