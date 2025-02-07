import os

from pydantic import BaseModel

from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image

class ImageMD(BaseModel):

    filePath: str = None
    acquisition_info: Acquisition = None
    dataset_metadata: Dataset = None
    image_metadata: TOMO_Image = None

    def fileName(self):
        return os.path.basename(self.filePath)

    def folderName(self):
        return os.path.dirname(self.filePath)

    def as_tomo_dict(self):
        return {"fileName": self.fileName(), **self.image_metadata.__dict__, }