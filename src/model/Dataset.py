from dataclasses import dataclass
from pydantic import validate_arguments

from src.model.Schema_Concept import Schema_Concept
#TODO: use https://github.com/cwacek/python-jsonschema-objects ?

@validate_arguments
@dataclass
class Dataset(Schema_Concept):

    type = "acquisition_schema"
    datasetType: str = None
    #name: str = None
    path: str = None
    images = []
    user_info: dict = None
    instrument_info: dict = None
    program_info: dict = None
    rows: int = None
    columns: int = None
    tileRow: int = None
    tileColumn: int = None

    def to_schema_dict(self):
        baseDict = self.__dict__
        baseDict["numberOfItems"] = len(self.images)
        #baseDict.pop("name")
        return {k: v for k, v in baseDict.items() if v is not None}

