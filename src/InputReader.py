import os
import shutil
from glob import glob
from typing import List, Optional

from numpy.lib.function_base import extract
from requests import HTTPError

from src.model.Acquisition import Acquisition
from src.model.TOMO_Image import TOMO_Image
from src.parser.Atlas3dParser import Atlas3dParser
from src.parser.EMProjectParser import EMProjectParser
import json
import logging

from src.parser.ImageParser import ImageParser
from src.parser.MetadataParser import MetadataParser
from src.parser.TiffParser import TiffParser
from src.util import load_json, is_zipfile, extract_zip_file, strip_workdir_from_path


class InputReader:

    available_md_parsers = {
        "EMProjectParser": EMProjectParser(),
        "Atlas3DParser": Atlas3dParser()
    }

    available_img_parsers = {
        "TiffParser": TiffParser(),
    }

    acquisitionParser: MetadataParser = None
    imageParser: ImageParser = None
    mapping_dict: dict = None
    temp_dir_path: str = None
    working_dir_path: str = None

    def __init__(self, map_path, input_path):
        try:
            self.mapping_dict = load_json(map_path)
        except HTTPError as e:
            logging.error("Tried loading remote mapping file: {}".format(map_path))
            logging.error(e)
            exit(1)
        except FileNotFoundError as e:
            logging.error("Local map file does not exist: {}".format(map_path))
            logging.error(e)
            exit(1)

        if not self._check_map_validity():
            logging.error("Invalid mapping file. Aborting")
            exit(1)

        try:
            self.imageParser = self.available_img_parsers[self.mapping_dict["image info"]["parser"]]
        except:
            logging.error("Error on setting image parser based on mapping file")
            exit(1)

        if not os.path.isfile(input_path):
            logging.error("Input file does not exist: {}. Aborting".format(input_path))
            exit(1)

        if not is_zipfile(input_path):
            logging.error("Invalid input file format: {}. Aborting".format(input_path))
            exit(1)

        self.temp_dir_path = extract_zip_file(input_path)

        root_dir = self._detect_project_root()
        if root_dir:
            self.working_dir_path = root_dir
            logging.info("Root path for data detected: {}".format(strip_workdir_from_path(self.temp_dir_path, root_dir)))
        else:
            logging.error("Could not determine common root path for all sources in map file. Aborting")
            exit(1)

    def _check_map_validity_acquisition(self, ac_dict):
        if not ac_dict or not ac_dict.get("sources"):
            logging.warning("No source for acquisition info defined, generic info for acquisition will be solely derived from image metadata")
        else:
            if not ac_dict.get("parser"):
                logging.error("Acquisition data source(s) found, but no parser defined. This is likely a faulty map. If this is intended, remove the source or the whole acquisition section")
                return False
            else:
                self.acquisitionParser = self.available_md_parsers.get(ac_dict["parser"]) #TODO: this is a somewhat weird side effect of checking - maybe not the ideal way of setting the parser

                if not self.acquisitionParser:
                    logging.error("Parser not available: {}".format(ac_dict["parser"]))
                    return False
        return True

    def _check_map_validity(self):
        md = self.mapping_dict

        if not self._check_map_validity_acquisition(md.get("acquisition info")):
            return False

        #TODO: check image part

        if not self.acquisitionParser.retrievable_datasets() and not md["image info"].get("autodetect_datasets"):
            logging.info("Dataset info will not be parsable from acquisition metadata and autodetection is set to false")
            if len(md["image info"]["sources"]) == 1:
                logging.warning("Exactly one dataset will be created according to map definition. If this is a mistake, check your map file")

        self.mapping_dict = md

        return True

    def _detect_project_root(self) -> str:
        sources = []
        if self.acquisitionParser:
            sources += self.mapping_dict["acquisition info"]["sources"]
        sources += self.mapping_dict["image info"]["sources"]

        for p, _, _ in os.walk(self.temp_dir_path):
            print(p)
            valid_source_path = False
            for s in sources:
                full_source_path = os.path.normpath(os.path.join(p, s))
                if glob(full_source_path):
                    valid_source_path = True
                else:
                    valid_source_path = False
                    break
            if valid_source_path:
                return p

    def clean_up(self):
        shutil.rmtree(self.working_dir_path)

    def retrieve_acquisition_info(self) -> List[Acquisition]:

        ac_infos = []

        #create Acquisition object from metadata
        if self.acquisitionParser:
            for s in self.mapping_dict["acquisition info"]["sources"]:
               with open(os.path.join(self.working_dir_path, s), "r", encoding="utf-8") as fp:
                   file_contents = fp.read()
                   ac = self.acquisitionParser.parse(file_contents)
                   ac_infos.append(ac)
        return ac_infos

    def retrieve_image_info(self) -> List[TOMO_Image]:
        image_infos = []

        #create TOMO_Image objects from tiff files
        for s in self.mapping_dict["image info"]["sources"]:
            curr_impath_list = glob(os.path.normpath(os.path.join(self.working_dir_path, s)))
            for ip in curr_impath_list:
                img = self.imageParser.parse(ip, self.mapping_dict["image info"]["tag"], self.mapping_dict["image info"]["image_map"].split(",")) #TODO: sanitize and prepare params before
                image_infos.append(img)
        return image_infos


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reader = InputReader("./resources/maps/parsing/inputmap_thermofisher.json", "../../../datasets/DEMO_20200818_AlSi13 XRM tomo2.zip")
    #reader = InputReader("./maps/parsing/inputmap_thermofisher.json", "../../../datasets/matwerk-data-repo/20230707_AlSi13_NFDI_old_structure.zip")
    #reader = InputReader("resources/maps/parsing/inputmap_zeiss-auriga.json", r"E:\downl\Zeiss-Auriga-Atlas_3DTomo.zip")
    tmpdir = reader.temp_dir_path

    acs = reader.retrieve_acquisition_info()
    print(len(acs))
    print(acs[0])

    imgs = reader.retrieve_image_info()
    print(len(imgs))
    print(imgs[0])

    reader.clean_up()

    logging.info("Temp folder deletion: {} - {}".format(tmpdir, os.path.exists(tmpdir)))
