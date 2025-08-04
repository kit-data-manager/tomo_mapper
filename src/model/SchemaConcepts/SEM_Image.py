from datetime import datetime
from typing import Optional

from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses_SEM import Entry, Sem

class CustomizedEntry(Schema_Concept, BaseModel):

    startTime: Optional[Annotated[datetime, BeforeValidator(parse_datetime)]] = None
    endTime: Optional[Annotated[datetime, BeforeValidator(parse_datetime)]] = None

    def as_schema_class(self):
        return Entry(**self.model_dump())

class SEM_Image(Schema_Concept, BaseModel):

    entry: Optional[CustomizedEntry] = None

    def as_schema_class(self):
        return Sem(**self.model_dump())