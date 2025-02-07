import os
from datetime import datetime

from pydantic import BeforeValidator, BaseModel
from typing_extensions import Annotated

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses import Identifier, Stage, Vacuum, TemperatureDetails, CurrentDetails

class TOMO_Image(Schema_Concept, BaseModel):

    filePath: str = None
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

    def to_schema_dict(self):
        pass

    def as_tomo_dict(self):
        return {"fileName": self.fileName(), **self.asdict(), }