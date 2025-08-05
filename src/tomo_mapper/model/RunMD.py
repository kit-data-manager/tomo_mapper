from collections import defaultdict
from typing import List

from tomo_mapper.model.SchemaConcepts.Acquisition_simplified import Acquisition
from tomo_mapper.model.SchemaConcepts import TOMO_Image
from tomo_mapper.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType


class RunMD:
    """
    contains metadata derived from file(s) describing the experiment run or results
    MUST contain lookup for datasetType - image
    MAY contain some acquisition metadata
    """

    acquisition_metadata: Acquisition = None
    images_by_datasets = defaultdict(list,{ DatasetType(k):[] for k in [e.value for e in DatasetType] })

    def get_images_for_datasetType(self, datasetType: DatasetType) -> List[TOMO_Image]:
        return self.images_by_datasets[datasetType]

    def get_datasetType_for_image(self, image: TOMO_Image) -> DatasetType:
        for k, v in self.images_by_datasets.items():
            for i in v:
                if i.match_by_path(image): return k

    def get_datasetTypes(self) -> List[DatasetType]:
        """
        Returns list of datasetTypes that have any images assigned
        :return: list of used datasetTypes
        """
        return [k for k in self.images_by_datasets.keys() if self.images_by_datasets[k]]

    def get_datasets(self) -> dict:
        """
        Returns dict of datasets that have any images assigned
        :return: (datasetType, List[TOMO_Image]) dict
        """
        return dict([x for x in self.images_by_datasets.items() if x[1]])

    def add_image(self, img: TOMO_Image, datasetType: DatasetType):
        self.images_by_datasets[datasetType].append(img)