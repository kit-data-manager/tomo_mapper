from typing import List

from pydantic import BaseModel, computed_field

from tomo_mapper.model.SchemaConcepts.Schema_Concept import Schema_Concept
from tomo_mapper.model.SchemaConcepts.TOMO_Image import TOMO_Image
from tomo_mapper.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType, IdentifierModel, \
    UserDescription, Program, InstrumentDetails, SEMFIBTomographyAcquisitionDatasetSchema

class Dataset(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated SEMFIBTomographyAcquisitionDatasetSchema,
    but replaced by a custom class for easier use
    """
    entryID: IdentifierModel = None
    definition: str = "acquisition_dataset"
    user: UserDescription = None
    program: Program = None
    instrument: InstrumentDetails = None
    datasetType: DatasetType = None
    rows: int = None
    columns: int = None
    tileColumn: int = None
    tileRow: int = None
    images: List[TOMO_Image] = None

    @computed_field
    def numberOfItems(self) -> int:
        if self.images:
            return len(self.images)
        return 0

    def as_schema_class(self) -> SEMFIBTomographyAcquisitionDatasetSchema:
        return SEMFIBTomographyAcquisitionDatasetSchema(**self.model_dump())

