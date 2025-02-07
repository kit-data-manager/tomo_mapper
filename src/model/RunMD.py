from typing import List


class RunMD:
    """
    contains metadata derived from file(s) describing the experiment run or results
    MUST contain lookup for datasetType - image
    MAY contain some acquisition metadata
    """

    def get_images_for_datasetType(self, datasetType):
        pass

    def get_datasetTypes(self):
        pass

    def get_acquisition_metadata(self):
        pass

    def add_image(self, img, datasetType):
        pass