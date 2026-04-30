# Generic type variables
from typing import TypeVar

DatasetTypeT = TypeVar('DatasetTypeT')  # Can be any DatasetType enum
ImageMetadataT = TypeVar('ImageMetadataT')
AcquisitionT = TypeVar('AcquisitionT')