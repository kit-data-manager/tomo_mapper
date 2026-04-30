from typing import Generic, Any

from pydantic import BaseModel

from mappingservice_plugincore.mappingservice_plugincore.model.types import ImageMetadataT

class ImageMD(BaseModel, Generic[ImageMetadataT]):
    """
    Generic ImageMD that doesn't know about specific schemas.
    """
    filePath: str
    acquisition_info: Any = None  # Plugin-specific Acquisition type
    dataset_metadata: Any = None  # Plugin-specific Dataset type
    image_metadata: ImageMetadataT = None

    def fileName(self) -> str:
        import os
        return os.path.basename(self.filePath)

    def folderName(self) -> str:
        import os
        return os.path.basename(os.path.dirname(self.filePath))