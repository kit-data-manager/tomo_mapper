import os
from datetime import datetime

from pydantic import BeforeValidator, BaseModel
from typing_extensions import Annotated

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses import Identifier, Stage, Vacuum, TemperatureDetails, \
    CurrentDetails, SEMFIBTomographyAcquisitionImageSchema


class TOMO_Image(Schema_Concept, BaseModel):

    filePath: str = None
    #TODO: creation time is only validated on init, not if set later. Should likely be changed
    creationTime: Annotated[datetime, BeforeValidator(parse_datetime)] = None
    entryID: Identifier = None
    fileLink: Identifier = None
    definition: str = "acquisiton_image"
    stage: Stage = None
    vacuum: Vacuum = None
    temperature: TemperatureDetails = None
    specimenCurrent: CurrentDetails = None

    def fileName(self):
        return os.path.basename(self.filePath)

    def folderName(self):
        return os.path.dirname(self.filePath)

    def as_tomo_dict(self):
        return {"fileName": self.fileName(), **self.asdict(), }

    def as_schema_class(self) -> SEMFIBTomographyAcquisitionImageSchema:
        return SEMFIBTomographyAcquisitionImageSchema(**self.model_dump())