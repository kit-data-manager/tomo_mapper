from datetime import datetime

from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator

from tomo_mapper.model.SchemaConcepts.Schema_Concept import Schema_Concept, parse_datetime
from tomo_mapper.model.SchemaConcepts.codegen.SchemaClasses_SEM import Entry, Sem

class CustomizedEntry(Schema_Concept, Entry):

    startTime: Annotated[datetime, BeforeValidator(parse_datetime)] = None
    endTime: Annotated[datetime, BeforeValidator(parse_datetime)] = None

    def as_schema_class(self):
        return Entry(**self.model_dump())

class SEM_Image(Schema_Concept, BaseModel):

    entry: CustomizedEntry = None

    def as_schema_class(self):
        return Sem(**self.model_dump())