from dataclasses import dataclass

from typing import List

from src.model.Dataset import Dataset
from src.model.Schema_Concept import Schema_Concept

@dataclass
class Acquisition(Schema_Concept):

    generic_metadata: dict = None
    dataset_template: Dataset = None #use this if you create a dataset template for all datasets but cannot derive the individual datasets from metadata
    datasets: List[Dataset] = None

    def to_schema_dict(self):
        baseDict = self.__dict__
        datasetList = baseDict.pop("datasets")
        genericMetadata = {k: v for k, v in baseDict.items() if v is not None}
        datasets = [x.to_schema_dict() for x in datasetList]
        schema_dict = {"genericMetadata": genericMetadata, "datasets": datasets}
        return schema_dict