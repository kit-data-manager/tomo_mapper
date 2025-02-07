from typing import List

from pydantic import BaseModel

from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.codegen.SchemaClasses import GenericMetadata, AcquisitionMain
from src.model.SchemaConcepts.codegen.SchemaClasses import Acquisition as Acquisition_gen


class Acquisition(Schema_Concept, BaseModel):

    genericMetadata: GenericMetadata = None
    dataset_template: Dataset = None #use this if you create a dataset template for all datasets but cannot derive the individual datasets from metadata
    datasets: List[Dataset] = None

    def as_schema_class(self) -> AcquisitionMain:
        dataset_schemas = [x.as_schema_class() for x in self.datasets]
        acquisition_schema = Acquisition_gen(genericMetadata=self.genericMetadata, dataset=dataset_schemas)
        main_schema = AcquisitionMain(acquisition=acquisition_schema)
        return main_schema