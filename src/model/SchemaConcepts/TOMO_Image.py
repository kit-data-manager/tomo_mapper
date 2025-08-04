import os
from datetime import datetime
from typing import Optional, Self

from pydantic import BeforeValidator, BaseModel, computed_field, model_validator
from typing_extensions import Annotated

from src.config import MappingConfig
from src.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import Identifier, Stage, Vacuum, TemperatureDetails, \
    CurrentDetails, SEMFIBTomographyAcquisitionImageSchema


class TOMO_Image(Schema_Concept, BaseModel):
    """
    basically interchangable with codegenerated SEMFIBTomographyAcquisitionImageSchema,
    but replaced by a custom class for easier use
    """

    localPath: Optional[str] = None
    #TODO: creation time is only validated on init, not if set later. Should likely be changed
    creationTime: Optional[Annotated[datetime, BeforeValidator(parse_datetime)]] = None
    entryID: Optional[Identifier] = None
    fileLink: Optional[Identifier] = None
    definition: str = "acquisition_image"
    stage: Optional[Stage] = None
    vacuum: Optional[Vacuum] = None
    temperature: Optional[TemperatureDetails] = None
    specimenCurrent: Optional[CurrentDetails] = None

    @computed_field
    def fileName(self) -> Optional[str]:
        if self.localPath:
            return os.path.basename(self.localPath)

    @computed_field
    @property #added for pyright to accept usage as field
    def filePath(self) -> Optional[str]:
        absPath = self.absolutePath()
        workDir = MappingConfig.get_working_dir()
        if workDir and absPath:
            return os.path.normpath(absPath.replace(workDir, ""))

    def absolutePath(self) -> Optional[str]:
        if self.localPath:
            workdir = MappingConfig.get_working_dir()
            if not os.path.isabs(self.localPath) and workdir:
                return os.path.join(workdir, self.localPath)
        return self.localPath

    def folderName(self) -> Optional[str]:
        if self.localPath:
            return os.path.dirname(self.localPath)

    def as_schema_class(self) -> SEMFIBTomographyAcquisitionImageSchema:
        return SEMFIBTomographyAcquisitionImageSchema(**self.model_dump())

    def match_by_path(self, other) -> bool:
        #TODO: we may want to do this more robustely with the help of the working dir?
        absPath = self.absolutePath()
        if not self.localPath: return False
        if not other.localPath: return False
        if not absPath: return False
        if not os.path.exists(absPath): return False
        if not os.path.exists(other.absolutePath()): return False
        return os.path.samefile(absPath, other.absolutePath())
    
    @model_validator(mode="after")
    def set_fileLink(self: "TOMO_Image") -> "TOMO_Image": #type hint needs to be in string because it is used in class with the same name. will not be defined otherwise
        # Automatically populate fileLink from filePath if not set.
        if not self.fileLink and self.localPath:
            self.fileLink = Identifier(identifierValue=self.filePath)
        return self