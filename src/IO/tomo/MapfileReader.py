import logging
import os.path
from json import JSONDecodeError
from urllib.parse import urlparse

from requests import HTTPError

from src.IO.MappingAbortionError import MappingAbortionError
from src.parser.ImageParser import ParserMode
from src.parser.ParserFactory import ParserFactory
from src.util import load_json

import validators


class MapFileReader:
    """
    This class provides utility functions reading and checking the user-provided map
    """

    @staticmethod
    def read_mapfile(filepath) -> dict:
        """
        Load local or remote map file into dict
        :param filepath: local absolute path, local relative path or remote (absolute) URI
        :return: file content as dict
        """
        logging.info("Reading map file content")
        try:
            return load_json(filepath)
        except HTTPError as e:
            logging.error("Tried loading remote mapping file: {}".format(filepath))
            logging.error(e)
            raise MappingAbortionError("Map file loading failed.")
        except FileNotFoundError as e:
            logging.error("Local map file does not exist: {}".format(filepath))
            logging.error(e)
            raise MappingAbortionError("Map file loading failed.")
        except UnicodeDecodeError as e:
            logging.error("Unable to load map file as json. Please check file and file encoding")
            raise MappingAbortionError("Map file loading failed.")
        except JSONDecodeError as e:
            logging.error("Unable to load map file as json. Please check file structure")
            raise MappingAbortionError("Map file loading failed.")

    #TODO: method might me a more generic util function. Move if needed elsewhere
    @staticmethod
    def validate_relative_path(path_string):
        if os.path.isabs(path_string):
            logging.error("Absolute path found in path string.")
            raise ValueError("Input was validated as relative path. Absolute path found instead: {}".format(path_string))

        head, tail = os.path.split(path_string)
        if os.path.normpath(path_string) != os.path.normpath(os.path.join(head, tail)):
            logging.error("Something went wrong parsing the input string: {}".format(path_string))
            raise ValueError("Error reading as relative path: {}".format(path_string))

        url = urlparse(path_string) #should work for relative urls too
        if url.hostname:
            logging.error("Input was validated as relative path. Found absolute URL instead: {}".format(path_string))
            raise ValueError("Error reading as relative path: {}".format(path_string))

        return True

    @staticmethod
    def parse_mapinfo_for_setup(mapping_dict):

        setup = mapping_dict.get("setup info")

        if not setup or not setup.get("sources"):
            logging.warning("No source for setup info defined")
            return None, None

        sources = setup.get("sources")

        if not setup.get("parser"):
            logging.error("Setup metadata source(s) found, but no parser defined. This is likely a faulty map. If this is intended, remove the source or the whole setup info section")
            raise ValueError('Error reading map info for setup metadata.')

        parser = ParserFactory.create_setupmd_parser(setup.get("parser"))

        for s in sources:
            MapFileReader.validate_relative_path(s)

        return sources, parser

    @staticmethod
    def parse_mapinfo_for_run(mapping_dict):
        #TODO: create less redundant method for setup and run parsing
        run = mapping_dict.get("run info")

        if not run or not run.get("sources"):
            logging.warning("No source for run info defined")
            return None, None

        sources = run.get("sources")

        if not run.get("parser"):
            logging.error("Run metadata source(s) found, but no parser defined. This is likely a faulty map. If this is intended, remove the source or the whole info section")
            raise ValueError('Error reading map info for run metadata.')

        parser = ParserFactory.create_runmd_parser(run.get("parser"))

        for s in sources:
            MapFileReader.validate_relative_path(s)

        return sources, parser

    @staticmethod
    def parse_mapinfo_for_images(mapping_dict):
        #TODO: parse other information as well (tag, map)
        im_dict = mapping_dict.get("image info")

        if not im_dict or not im_dict.get("sources"):
            logging.error("You need to provide at least one image source inclusion path for extraction")
            raise ValueError('Error reading map info for images. No image sources provided')

        sources = im_dict.get("sources")
        parser = None

        for s in im_dict.get("sources"):
            MapFileReader.validate_relative_path(s)

        if not im_dict.get("parser"):
            logging.error("No image parser defined in map file")
            raise ValueError('Error reading map info for images. No parser provided')

        #parser = available_parsers.get(im_dict["parser"])
        parserArgs = dict()
        parserArgs["mode"] = ParserMode.TOMO
        if im_dict.get("tag"):
            parserArgs["tagID"] = im_dict.get("tag")
        parser = ParserFactory.create_img_parser(im_dict["parser"], **parserArgs)

        for s in sources:
            MapFileReader.validate_relative_path(s)

            if "*" not in s:
                logging.warning("Expected a wildcard path to multiple files, got singular path. This is likely a faulty map input: {}".format(s))
        return sources, parser

