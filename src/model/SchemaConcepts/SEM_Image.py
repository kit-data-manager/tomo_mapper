from pydantic import BaseModel

from src.model.SchemaConcepts.Schema_Concept import Schema_Concept
from src.model.SchemaConcepts.codegen.SchemaClasses_SEM import Entry, Sem


class SEM_Image(Schema_Concept, BaseModel):

    entry: Entry = None

    def as_schema_class(self):
        return Sem(**self.model_dump())