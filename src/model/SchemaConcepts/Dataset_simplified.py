from typing import List, Optional

from pydantic import BaseModel, computed_field

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType, IdentifierModel, \
    UserDescription, Program, InstrumentDetails, SEMFIBTomographyAcquisitionDatasetSchema

class Dataset(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated SEMFIBTomographyAcquisitionDatasetSchema,
    but replaced by a custom class for easier use
    """
    entryID: Optional[IdentifierModel] = None
    definition: str = "acquisition_dataset"
    user: Optional[UserDescription] = None
    program: Optional[Program] = None
    instrument: Optional[InstrumentDetails] = None
    datasetType: Optional[DatasetType] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    tileColumn: Optional[int] = None
    tileRow: Optional[int] = None
    images: Optional[List[TOMO_Image]] = None

    @computed_field
    def numberOfItems(self) -> int:
        if self.images:
            return len(self.images)
        return 0

    def as_schema_class(self) -> SEMFIBTomographyAcquisitionDatasetSchema:
        return SEMFIBTomographyAcquisitionDatasetSchema(**self.model_dump())

