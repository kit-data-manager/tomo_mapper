from typing import List, Optional

from pydantic import BaseModel

from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import GenericMetadata, AcquisitionMain
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import Acquisition as Acquisition_gen


class Acquisition(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated Acqusition,
    but replaced by a custom class for easier use
    """

    genericMetadata: Optional[GenericMetadata] = None
    dataset_template: Optional[Dataset] = None #use this if you create a dataset template for all datasets but cannot derive the individual datasets from metadata
    datasets: Optional[List[Dataset]] = None

    def as_schema_class(self) -> AcquisitionMain:
        dataset_schemas = [x.as_schema_class() for x in self.datasets] if self.datasets else []
        acquisition_schema = Acquisition_gen(genericMetadata=self.genericMetadata, dataset=dataset_schemas)
        main_schema = AcquisitionMain(acquisition=acquisition_schema)
        return main_schema