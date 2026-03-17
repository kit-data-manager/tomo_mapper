from datetime import datetime
from typing import Optional, List

from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator

from mappingservice_plugincore.model.Schema_Concept import Schema_Concept, parse_datetime
from src.model.SchemaConcepts.codegen.SchemaClasses_SEM import Entry, Sem, MeasurementPurpose, Parent, Identifier, \
    Program, Revision, User, InstrumentDetails

class CustomizedEntry(Schema_Concept, BaseModel):

    startTime: Optional[Annotated[datetime, BeforeValidator(parse_datetime)]] = None
    endTime: Optional[Annotated[datetime, BeforeValidator(parse_datetime)]] = None

    #TODO: This is an ugly workaround to not break inheritance and to still customize the date fields
    #all properties following are directly copied from Entry. May break on schema changes :(
    technique: Optional[str] = None
    measurementPurpose: Optional[MeasurementPurpose] = None
    measurementDescription: Optional[str] = None
    equipment: Optional[str] = None
    consumables: Optional[List[str]] = None
    parents: Optional[List[Parent]] = None
    entryID: Optional[Identifier] = None
    title: Optional[str] = None
    program: Optional[Program] = None
    revision: Optional[Revision] = None
    user: Optional[User] = None
    instrument: Optional[InstrumentDetails] = None

    def as_schema_class(self):
        return Entry(**self.model_dump())

class SEM_Image(Schema_Concept, BaseModel):

    entry: Optional[CustomizedEntry] = None

    def as_schema_class(self):
        return Sem(**self.model_dump())