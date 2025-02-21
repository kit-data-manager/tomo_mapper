import os
from datetime import datetime

from pydantic import BeforeValidator, BaseModel, computed_field
from typing_extensions import Annotated

from src.config import MappingConfig
from src.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses import Identifier, Stage, Vacuum, TemperatureDetails, \
    CurrentDetails, SEMFIBTomographyAcquisitionImageSchema


class TOMO_Image(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated SEMFIBTomographyAcquisitionImageSchema,
    but replaced by a custom class for easier use
    """

    localPath: str
    #TODO: creation time is only validated on init, not if set later. Should likely be changed
    creationTime: Annotated[datetime, BeforeValidator(parse_datetime)] = None
    entryID: Identifier = None
    fileLink: Identifier = None
    definition: str = "acquisition_image"
    stage: Stage = None
    vacuum: Vacuum = None
    temperature: TemperatureDetails = None
    specimenCurrent: CurrentDetails = None

    @computed_field
    def fileName(self) -> str:
        return os.path.basename(self.localPath)

    @computed_field
    def filePath(self) -> str:
        return os.path.normpath(self.absolutePath().replace(MappingConfig.get_working_dir(), ""))

    def absolutePath(self):
        if not self.localPath: return None
        if not os.path.isabs(self.localPath):
            workdir = MappingConfig.get_working_dir()
            return os.path.join(workdir, self.localPath)
        return self.localPath

    def folderName(self):
        return os.path.dirname(self.localPath)

    def as_tomo_dict(self):
        return {"fileName": self.fileName(), **self.asdict(), }

    def as_schema_class(self) -> SEMFIBTomographyAcquisitionImageSchema:
        return SEMFIBTomographyAcquisitionImageSchema(**self.model_dump())

    def match_by_path(self, other):
        #TODO: we may want to do this more robustely with the help of the working dir?
        if not self.localPath: return False
        if not other.localPath: return False
        if not os.path.exists(self.absolutePath()): return False
        if not os.path.exists(other.absolutePath()): return False
        return os.path.samefile(self.absolutePath(), other.absolutePath())