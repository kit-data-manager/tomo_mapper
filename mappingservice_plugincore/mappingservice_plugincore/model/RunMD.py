from abc import ABC
from collections import defaultdict
from typing import Generic, Dict, List

from mappingservice_plugincore.mappingservice_plugincore.model.types import DatasetTypeT, ImageMetadataT, AcquisitionT

class RunMD(Generic[DatasetTypeT, ImageMetadataT], ABC):
    """
    Generic RunMD that works with ANY DatasetType enum.
    Plugins inject their specific types at instantiation.
    """

    def __init__(self, dataset_type_class: type):
        """
        Args:
            dataset_type_class: The specific DatasetType enum for this schema
        """
        self.dataset_type_class = dataset_type_class
        self.acquisition_metadata: AcquisitionT = None
        self.images_by_datasets: Dict[DatasetTypeT, List[ImageMetadataT]] = defaultdict(list)

    def add_image(self, img: ImageMetadataT, datasetType: DatasetTypeT):
        if datasetType not in self.images_by_datasets:
            self.images_by_datasets[datasetType] = []
        self.images_by_datasets[datasetType].append(img)

    def get_images_for_datasetType(self, datasetType: DatasetTypeT) -> List[ImageMetadataT]:
        return self.images_by_datasets.get(datasetType, [])

    def get_datasetTypes(self) -> List[DatasetTypeT]:
        return [k for k, v in self.images_by_datasets.items() if v]

    def get_datasets(self) -> Dict[DatasetTypeT, List[ImageMetadataT]]:
        return {k: v for k, v in self.images_by_datasets.items() if v}