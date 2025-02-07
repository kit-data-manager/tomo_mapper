from typing import List

from pydantic import BaseModel

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses import DatasetType, IdentifierModel, \
    UserDescription, Program, InstrumentDetails

class Dataset(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated SEMFIBTomographyAcquisitionDatasetSchema,
    but replaced by a custom class for easier use
    """
    entryID: IdentifierModel = None
    definition: str = "acquisition_schema"
    user: UserDescription = None
    program: Program = None
    instrument: InstrumentDetails = None
    datasetType: DatasetType = None
    numberOfItems: int = None
    rows: int = None
    columns: int = None
    tileColumn: int = None
    tileRow: int = None
    images: List[TOMO_Image] = None

