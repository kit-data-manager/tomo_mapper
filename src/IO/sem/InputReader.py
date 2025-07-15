import logging
import mimetypes
import os

from src.IO.MappingAbortionError import MappingAbortionError
from src.parser.ImageParser import ParserMode
from src.parser.ParserFactory import ParserFactory
from src.util import load_json, get_filetype_with_magica, robust_textfile_read


class InputReader:

    mapping = None
    parser_names = None

    def __init__(self, map_path, input_path):
        logging.info("Preparing parsers based on parsing map file and input.")
        self.mapping = load_json(map_path)

        if not os.path.exists(input_path):
            logging.error("Input file {} does not exist. Aborting".format(input_path))
            raise MappingAbortionError("Input file loading failed.")

        self.parser_names = self.get_applicable_parsers(input_path)

        if not self.parser_names:
            logging.error("No applicable parsers found for input {}".format(input_path))
            mimetype_set = list(set([v.expected_input_format() for v in ParserFactory.available_img_parsers.values()]))
            logging.info("Supported mimetypes: {}".format(mimetype_set))
            raise MappingAbortionError("Input file parsing aborted.")
        logging.info("Applicable parsers: {}".format(", ".join(self.parser_names)))


    @staticmethod
    def get_applicable_parsers(input_path):
        """
        Filters the available image parsers to those applicable to the input file format.
        It tries to determine by extension, but can fallback to using magica.
        :param input_path: file path to input
        :return: list of parser names that can handle the provided input format
        """
        mt, _ = mimetypes.guess_type(input_path)
        if not mt or mt == "application/unknown": #fallback, especially if file extension is not available
            #Text files are tricky with magica, so try to read as such first
            mt = get_filetype_with_magica(input_path)
            if mt != "text/plain" and "image/" not in mt:
                try:
                    robust_textfile_read(input_path)
                    mt = "text/plain"
                except:
                    logging.error("Could not determine mimetype for input {}".format(input_path))
                    raise MappingAbortionError

        logging.debug("Determined input type: {}".format(mt))

        available_parsers = []
        for k, p in ParserFactory.available_img_parsers.items():
            expected = p.expected_input_format()
            if expected == mt:
                available_parsers.append(k)
        return available_parsers

    def retrieve_image_info(self, input_path):
        """
        Applies the applicable list of parsers to the provided input. Stops on the first successful parsing result and returns it.
        Usually we do not expect more than one applicable parser to be available. If so, it would be advised to add more checks to keep the list of parsers at len 1.
        :param input_path: path to input file
        :return:
        """
        for parser in self.parser_names:
            logging.debug("Trying to parse image with {}".format(parser))
            imgp = ParserFactory.create_img_parser(parser, mode=ParserMode.SEM)

            result, raw = imgp.parse(input_path, self.mapping)
            if result and result.image_metadata:
                output_dict = result.image_metadata.to_schema_dict()
                return output_dict
