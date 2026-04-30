from collections import defaultdict
from typing import List, Optional

from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType

from mappingservice_plugincore.mappingservice_plugincore.model.RunMD import RunMD as GenericRunMD

class RunMD(GenericRunMD[DatasetType, TOMO_Image]):
    """
    contains metadata derived from file(s) describing the experiment run or results
    MUST contain lookup for datasetType - image
    MAY contain some acquisition metadata
    """
    def __init__(self):
        super().__init__(dataset_type_class=DatasetType)

        self.acquisition_metadata: Acquisition | None = None

    def get_datasetType_for_image(self, image: TOMO_Image) -> Optional[DatasetType]:
        for k, v in self.images_by_datasets.items():
            for i in v:
                if i.match_by_path(image): return k