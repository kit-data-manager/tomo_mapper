import json
import logging
from collections import defaultdict
from pprint import pprint
from typing import List

from pydantic import ValidationError

from src.IO.MappingAbortionError import MappingAbortionError
from src.model.ImageMD import ImageMD
from src.model.RunMD import RunMD
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import AcquisitionMain
from src.model.SetupMD import SetupMD
from deepmerge import always_merger, conservative_merger


class OutputWriter:

    @staticmethod
    def stitch_together(setupMD: SetupMD, runMD: RunMD, imageMD: List[ImageMD]):

        acquisitionModel = dict()
        predefined_ds = dict()
        ds_template = None

        #add the base info about the acquisition from metadata files
        if setupMD and setupMD.acquisition_metadata:
            if setupMD.acquisition_metadata.datasets:

                predefined_ds = dict([(x.datasetType, x) for x in setupMD.acquisition_metadata.datasets])
                setupMD.acquisition_metadata.datasets = None
            if setupMD.acquisition_metadata.dataset_template:
                ds_template = setupMD.acquisition_metadata.dataset_template
            always_merger.merge(acquisitionModel, setupMD.acquisition_metadata.to_schema_dict())

        dsDict = {}

        if runMD:
            if runMD.acquisition_metadata:
                always_merger.merge(acquisitionModel, runMD.acquisition_metadata.to_schema_dict())
            dsDict = dict([(x, Dataset(datasetType=x)) for x in runMD.get_datasetTypes()])

        dsinfo_from_images = defaultdict(dict)

        for img in imageMD:
            if not img.image_metadata:
                logging.warning("No image metadata extracted from image {}. Omitting from output".format(img.fileName()))
                continue

            if not runMD:
                dt = img.determine_dstype()
            else:
                dt = runMD.get_datasetType_for_image(img.image_metadata)
            if not dt:
                logging.warning("Dataset Type for image {} cannot be determined. Omitting from output".format(img.fileName()))
                continue
            if not dsDict.get(dt):
                dsDict[dt] = Dataset(datasetType=dt)
            if dsDict[dt].images:
                dsDict[dt].images.append(img.image_metadata)
            else: dsDict[dt].images = [img.image_metadata]

            if img.acquisition_info:
                always_merger.merge(acquisitionModel, img.acquisition_info.to_schema_dict())
            if img.dataset_metadata:
                conservative_merger.merge(dsinfo_from_images[dt], img.dataset_metadata.to_schema_dict())

        for k, v in dsDict.items():
            if not v.images:
                logging.warning("No images successfully extracted for {}. Omitting from output".format(v.datasetType))
                continue
            v_dict = v.to_schema_dict()
            if predefined_ds and predefined_ds.get(k):
                conservative_merger.merge(v_dict, predefined_ds[k].to_schema_dict())
            acquisitionModel["acquisition"]["dataset"].append(v_dict)
            conservative_merger.merge(v_dict, dsinfo_from_images[k])

            if ds_template:
                conservative_merger.merge(v_dict, ds_template.to_schema_dict())

        #since we operated on dicts a lot in this output writer, we do a final conversion to the class model to ensure schema compliance
        try:
            AcquisitionMain(**acquisitionModel)
        except ValidationError as e:
            raise MappingAbortionError("Final check for schema compliance failed")
        return acquisitionModel

    @staticmethod
    def writeOutput(outputDict, fp):
        with open(fp, "w") as f:
            json.dump(outputDict, f, indent=4, ensure_ascii=False)


