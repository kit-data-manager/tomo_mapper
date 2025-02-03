import logging
import os.path
from urllib.parse import urlparse

from requests import HTTPError

from src.parser.ParserFactory import ParserFactory
from src.parser.mapping_util import _read_mapTable_hardcoded
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
            exit(1)
        except FileNotFoundError as e:
            logging.error("Local map file does not exist: {}".format(filepath))
            logging.error(e)
            exit(1)

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
    def parse_mapinfo_for_acquisition(mapping_dict):

        ac_dict = mapping_dict.get("acquisition info")

        if not ac_dict or not ac_dict.get("sources"):
            logging.warning("No source for acquisition info defined, generic info for acquisition will be solely derived from image metadata")
            return None, None

        sources = ac_dict.get("sources")
        parser = None

        if not ac_dict.get("parser"):
            logging.error("Acquisition data source(s) found, but no parser defined. This is likely a faulty map. If this is intended, remove the source or the whole acquisition section")
            raise ValueError('Error reading map info for acquisition.')

        #parser = available_parsers.get(ac_dict["parser"])
        parser = ParserFactory.create_md_parser(ac_dict.get("parser"))

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

        tagID = im_dict.get("tag")
        if not tagID:
            logging.error("No image tag defined in map file")
            raise ValueError('Error reading map info for images. No image tag provided')

        if not _read_mapTable_hardcoded(tagID, "TOMO_Schema"):
            logging.error("Tag id {} not found in internal mapping file".format(tagID))
            raise ValueError("Error reading tag info from map file. Unable to handle this tag")

        #parser = available_parsers.get(im_dict["parser"])
        parser = ParserFactory.create_img_parser(im_dict["parser"],tagID=tagID)

        for s in sources:
            MapFileReader.validate_relative_path(s)

            if "*" not in s:
                logging.warning("Expected a wildcard path to multiple files, got singular path. This is likely a faulty map input: {}".format(s))
        return sources, parser

