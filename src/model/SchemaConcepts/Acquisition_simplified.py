from typing import List

from pydantic import BaseModel

from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.codegen.SchemaClasses import GenericMetadata

class Acquisition(Schema_Concept, BaseModel):

    genericMetadata: GenericMetadata = None
    dataset_template: Dataset = None #use this if you create a dataset template for all datasets but cannot derive the individual datasets from metadata
    datasets: List[Dataset] = None

    def to_schema_dict(self):
        baseDict = self.__dict__
        datasetList = baseDict.pop("datasets")
        genericMetadata = {k: v for k, v in baseDict.items() if v is not None}
        datasets = [x.__dict__ for x in datasetList]
        schema_dict = {"genericMetadata": genericMetadata, "datasets": datasets}
        return schema_dict