import logging
import os
from typing import Union

from pydantic import BaseModel

from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.SEM_Image import SEM_Image
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType


class ImageMD(BaseModel):

    filePath: str
    acquisition_info: Acquisition = None
    dataset_metadata: Dataset = None
    image_metadata: Union[TOMO_Image, SEM_Image] = None

    def fileName(self):
        return os.path.basename(self.filePath)

    def folderName(self):
        return os.path.basename(os.path.dirname(self.filePath))

    def determine_dstype(self) -> DatasetType:
        if self.dataset_metadata is not None and self.dataset_metadata.datasetType is not None:
            return self.dataset_metadata.datasetType

        if self.folderName() is not None and self.folderName() in DatasetType:
            return DatasetType(self.folderName())

        logging.warning("Cannot determine dataset type for image metadata")
        return None