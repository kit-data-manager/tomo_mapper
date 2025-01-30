import os
from dataclasses import dataclass
from datetime import datetime

from pydantic.dataclasses import dataclass
from pydantic.v1 import validate_arguments
from src.model.Schema_Concept import Schema_Concept
#from dataclasses_json import dataclass_json

@validate_arguments
@dataclass
class TOMO_Image(Schema_Concept):

    filePath: str = None
    generic_metadata: dict = None
    dataset_metadata: dict = None
    image_metadata: dict = None


    def get_acquisition_info(self):
        return self.generic_metadata

    def get_dataset_info(self):
        return self.dataset_metadata

    def fileName(self):
        return os.path.basename(self.filePath)

    def folderName(self):
        return os.path.dirname(self.filePath)

    def to_schema_dict(self):
        pass

    def as_tomo_dict(self):
        return {"fileName": self.fileName(), **self.image_metadata, }