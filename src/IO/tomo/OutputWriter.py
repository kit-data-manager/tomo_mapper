import json
import logging
import os
from collections import defaultdict
from pprint import pprint
from typing import List

from pydantic import ValidationError

from src.IO.MappingAbortionError import MappingAbortionError
from src.model.ImageMD import ImageMD
from src.model.RunMD import RunMD
from src.model.SchemaConcepts.Dataset_simplified import Dataset
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import AcquisitionMain
from src.model.SetupMD import SetupMD
from deepmerge import always_merger, conservative_merger

class OutputWriter:

    @staticmethod
    def stitch_together(setupMDs: List[SetupMD], runMDs: List[RunMD], imageMD: List[ImageMD]) -> dict:

        acquisitionModel = dict()
        predefined_ds = dict()
        ds_template = None

        # Skip None
        setupMDs = [s for s in setupMDs if s]
        runMDs = [r for r in runMDs if r]

        #add the base info about the acquisition from metadata files
        for setupMD in setupMDs: # Merge all setup metadata
            if setupMD and setupMD.acquisition_metadata:
                if setupMD.acquisition_metadata.datasets:

                    predefined_ds = dict([(x.datasetType, x) for x in setupMD.acquisition_metadata.datasets])
                    setupMD.acquisition_metadata.datasets = []
                if setupMD.acquisition_metadata.dataset_template:
                    ds_template = setupMD.acquisition_metadata.dataset_template
                always_merger.merge(acquisitionModel, setupMD.acquisition_metadata.to_schema_dict())

        dsDict = {}


        for runMD in runMDs: # Merge all run metadata
            if runMD.acquisition_metadata:
                always_merger.merge(acquisitionModel, runMD.acquisition_metadata.to_schema_dict())
            for dtype in runMD.get_datasetTypes():
                if dtype not in dsDict:
                    dsDict[dtype] = Dataset(datasetType=dtype)
            #dsDict = dict([(x, Dataset(datasetType=x)) for x in runMD.get_datasetTypes()])

        dsinfo_from_images = defaultdict(list)

        #add info from images
        for img in imageMD:
            if not img.image_metadata:
                logging.warning(f"No image metadata extracted from image {img.fileName()}. Omitting.")
                continue

            dt = None
            for runMD in runMDs:
                if isinstance(img.image_metadata, TOMO_Image): #the check is only here to make static type checking happy
                    dt = runMD.get_datasetType_for_image(img.image_metadata)
                if dt: break
            if not dt:
                logging.warning("Dataset Type for image {} cannot be determined".format(img.fileName()))
                dt = "unknown"
            if not dsDict.get(dt):
                if dt != "unknown":
                    dsDict[dt] = Dataset(datasetType=dt)
                else: #we create an initial fallback dataset for all images that are not matchable
                    dsDict[dt] = Dataset()
            if dsDict[dt].images:
                dsDict[dt].images.append(img.image_metadata)
            else:
                dsDict[dt].images = [img.image_metadata]

            if img.acquisition_info:
                always_merger.merge(acquisitionModel, img.acquisition_info.to_schema_dict())
            if img.dataset_metadata:
                dsinfo_from_images[dt].append(img.dataset_metadata)

        '''
        FALLBACK in case we have image metadata extracted but cannot map to a dataset type
        We split the remaining images by their individual folder and their detector type or name
        The dataset extraction is currently only based on the first image per bucket without further checking,
        so the dataset info might be lacking in some cases.
        '''
        unknown_ds = dsDict.pop("unknown", None)
        dsDict_items = list(dsDict.values())
        if unknown_ds:
            image_buckets = defaultdict(list)
            md_buckets = defaultdict(list)
            for k, img in enumerate(unknown_ds.images):
                folderpath = os.path.dirname(img.filePath)
                instrument = dsinfo_from_images["unknown"][k].instrument
                detector = instrument.detector if instrument else None
                detectorType = detector.detectorType if detector else None
                detectorType = detector.name if detector and not detectorType else detectorType
                image_buckets[(folderpath, detectorType)].append(img)
                md_buckets[(folderpath, detectorType)].append(dsinfo_from_images["unknown"][k])
            for k, v in image_buckets.items():
                current_ds = Dataset(**md_buckets[k][0].to_schema_dict())
                current_ds.images = v
                dsDict_items.append(current_ds)

        for v in dsDict_items:
            if not v.images:
                logging.warning("No images successfully extracted for {}. Omitting from output".format(v.datasetType))
                continue
            v_dict = v.to_schema_dict()
            k = v.datasetType
            if k:
                if predefined_ds and predefined_ds.get(k):
                    conservative_merger.merge(v_dict, predefined_ds[k].to_schema_dict())
                for ds_md in dsinfo_from_images[k]:
                    conservative_merger.merge(v_dict, ds_md.to_schema_dict())
            acquisitionModel["acquisition"]["dataset"].append(v_dict)

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
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(outputDict, f, indent=4, ensure_ascii=False)