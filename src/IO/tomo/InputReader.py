import os
import shutil
from glob import glob
from typing import List

from src.IO.MappingAbortionError import MappingAbortionError
from src.IO.tomo.MapfileReader import MapFileReader
from src.config import MappingConfig
from src.model.ImageMD import ImageMD
from src.model.RunMD import RunMD
import logging

from src.model.SetupMD import SetupMD
from src.parser.ImageParser import ImageParser
from src.parser.SetupMD_Parser import SetupMD_Parser
from src.parser.ParserFactory import ParserFactory
from src.util import is_zipfile, extract_zip_file, strip_workdir_from_path, robust_textfile_read


class InputReader:
    """
    The input reader reads, checks/sanitizes and parses all parameters provided for the mapping.

    Implementation concept:
    - fail early: i.e. errors in mapping file can be handled before starting to extract any zip file content.
    - reject with error
    - warn about unusual input
    """

    setupParser: SetupMD_Parser = None
    setupmdSources: List[str] = []
    imageParser: ImageParser = None
    imageSources: List[str] = []
    mapping_dict: dict = None
    temp_dir_path: str = None
    working_dir_path: str = None

    parserFactory = ParserFactory()

    def __init__(self, map_path, input_path):

        ### reading and sanity checking map file
        self.mapping_dict = MapFileReader.read_mapfile(map_path)

        ac_sources, ac_parser = MapFileReader.parse_mapinfo_for_setup(self.mapping_dict)
        self.setupParser = ac_parser
        self.setupmdSources = ac_sources

        run_sources, run_parser = MapFileReader.parse_mapinfo_for_run(self.mapping_dict)
        self.runParser = run_parser
        self.runmdSources = run_sources

        im_sources, im_parser = MapFileReader.parse_mapinfo_for_images(self.mapping_dict)
        self.imageParser = im_parser
        self.imageSources = im_sources

        ###various further checks for map input

        if len(ac_sources) > 1 or len([x for x in ac_sources if "*" in x]) > 0:
            raise NotImplementedError("More than one metadata file for setup info found. This feature is not yet implemented.")

        if not os.path.isfile(input_path) and not os.path.isdir(input_path):
            logging.error("Input file or folder does not exist: {}. Aborting".format(input_path))
            raise MappingAbortionError("Input file loading failed.")

        logging.info("Map file content successfully read and validated.")
        logging.info("The chosen parsers support the following instruments/vendors: {}".format(", ".join(self._get_supported_instruments())))

        ### reading input file
        if is_zipfile(input_path):
            self.temp_dir_path = extract_zip_file(input_path)
            # auto-detect root dir in zip. TODO: make more flexible and robust. Allow for non-zip input (no auto-detect then)
            root_dir = self._detect_project_root(self.temp_dir_path)
            if root_dir:
                self.working_dir_path = root_dir
                logging.info(
                    "Root path for data detected: {}".format(strip_workdir_from_path(self.temp_dir_path, root_dir)))
            else:
                logging.error("Could not determine common root path for all sources in map file. Aborting")
                raise MappingAbortionError("Input file loading failed. Mapping info not applicable to input.")
        else:
            if not os.path.isdir(input_path):
                raise MappingAbortionError("Invalid input path. Not an existing directory: {}".format(input_path))
            detected_root = self._detect_project_root(input_path)
            if not input_path == detected_root:
                if self._detect_project_root(input_path):
                    raise MappingAbortionError("Invalid input path. Did you mean to use {} instead?".format(detected_root)) #most specific error
                raise MappingAbortionError("Input path is not pointing to the root folder for all sources specified in input map: {}".format(input_path)) #error otherwise
            self.working_dir_path = input_path

        MappingConfig.set_working_dir(self.working_dir_path)


    def _get_supported_instruments(self) -> List[str]:
        supports = set()
        if self.setupParser:
            supports.update(self.setupParser.supported_input_sources())
        if self.runParser:
            supports.update(self.runParser.supported_input_sources())
        return list(supports)

    def _detect_project_root(self, root_dir_path) -> str:
        """
        function to allow for as many nested directories in a zip file iff all described pathes in the mapping file point to the same root directory anyway.

        CAREFUL: only enable this in case of a zip file input (currently the only implementation) - if a local folder is specified as input, the mapping file should point to the exact same folder (reject otherwise)
        :return:
        """
        sources = []
        if self.setupParser:
            sources += self.mapping_dict["setup info"]["sources"]
        if self.runParser:
            sources += self.mapping_dict["run info"]["sources"]
        sources += self.mapping_dict["image info"]["sources"]

        for p, _, _ in os.walk(root_dir_path):
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
        if self.temp_dir_path:
            shutil.rmtree(self.temp_dir_path)
            logging.debug("Temp folder deletion: {} - {}".format(self.temp_dir_path, os.path.exists(self.temp_dir_path)))
        else:
            logging.debug("No temp folder used, nothing to clean up.")

    def retrieve_setup_info(self) -> List[SetupMD]:

        setup_infos = []

        if self.setupParser:
            for s in self.setupmdSources:
                try:
                    logging.info("Extracting setup info from: {}".format(s))
                    file_contents = robust_textfile_read(os.path.join(self.working_dir_path, s))
                    setupMD, _ = self.setupParser.parse_setup(file_contents)
                    setup_infos.append(setupMD)
                except FileNotFoundError:
                    logging.error("Setup md file does not exist: {}. Please make sure the configuration in the map file matches your input data".format(s))
        return setup_infos

    def retrieve_run_info(self) -> List[RunMD]:

        run_infos = []

        if self.runParser:
            for s in self.runmdSources:
                try:
                    logging.info("Extracting run info from: {}".format(s))
                    file_contents = robust_textfile_read(os.path.join(self.working_dir_path, s))
                    runMD, _ = self.runParser.parse_run(file_contents)
                    run_infos.append(runMD)
                except FileNotFoundError:
                    logging.error("Run md file does not exist: {}. Please make sure the configuration in the map file matches your input data".format(s))
        return run_infos

    def retrieve_image_info(self) -> List[ImageMD]:
        image_infos = []

        #create TOMO_Image objects from tiff files
        for s in self.mapping_dict["image info"]["sources"]:
            curr_impath_list = glob(os.path.normpath(os.path.join(self.working_dir_path, s)))
            for ip in curr_impath_list:
                logging.info("Extracting image info from: {}/{}".format(os.path.basename(os.path.dirname(ip)), os.path.basename(ip)))
                img, _ = self.imageParser.parse(ip, mapping=None) #TODO: sanitize and prepare params before
                if img:
                    image_infos.append(img)
        return image_infos
