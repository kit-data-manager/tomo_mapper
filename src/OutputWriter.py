import json
import logging
from pprint import pprint
from typing import List

from src.model.ImageMD import ImageMD
from src.model.RunMD import RunMD
from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SetupMD import SetupMD
from deepmerge import always_merger, conservative_merger


class OutputWriter:

    @staticmethod
    def stitch_together(setupMD: SetupMD, runMD: RunMD, imageMD: List[ImageMD]):

        acquisitionModel = dict()
        predefined_ds = dict()

        #add the base info about the acquisition from metadata files
        if setupMD and setupMD.acquisition_metadata:

            predefined_ds = dict([(x.datasetType, x) for x in setupMD.acquisition_metadata.datasets])
            setupMD.acquisition_metadata.datasets = None
            always_merger.merge(acquisitionModel, setupMD.acquisition_metadata.to_schema_dict())

        dsDict = {}

        if runMD:
            if runMD.acquisition_metadata:
                always_merger.merge(acquisitionModel, runMD.acquisition_metadata.to_schema_dict())
            dsDict = dict([(x, Dataset(datasetType=x)) for x in runMD.get_datasetTypes()])

        for img in imageMD:
            if not img.image_metadata:
                logging.warning("No image metadata extracted from image {}. Omitting from output".format(img.filename))
                continue

            if not runMD:
                dt = img.determine_dstype()
                if not dt:
                    logging.warning("Dataset Type for image cannot be determined. Omitting from output".format(img.filename))
                    continue
            else:
                dt = runMD.get_datasetType_for_image(img.image_metadata)
            if dsDict[dt].images:
                dsDict[dt].images.append(img.image_metadata)
            else: dsDict[dt].images = [img.image_metadata]

            if img.acquisition_info:
                always_merger.merge(acquisitionModel, img.acquisition_info.to_schema_dict())

        for k, v in dsDict.items():
            if not v.images:
                logging.warning("No images successfully extracted for {}. Omitting from output".format(v.datasetType))
                continue
            v_dict = v.to_schema_dict()
            if predefined_ds and predefined_ds.get(k):
                conservative_merger.merge(v_dict, predefined_ds[k].to_schema_dict())
            acquisitionModel["acquisition"]["dataset"].append(v_dict)

        print(json.dumps(acquisitionModel, indent=4))
        return acquisitionModel

