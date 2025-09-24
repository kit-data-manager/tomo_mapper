import logging
import mimetypes
import os
import shutil
from pathlib import Path

from src.IO.MappingAbortionError import MappingAbortionError
from src.parser.ImageParser import ParserMode
from src.parser.ParserFactory import ParserFactory
from src.IO.BaseInputReader import BaseInputReader 
from src.util import is_zipfile, extract_zip_file, load_json, get_filetype_with_magica, robust_textfile_read


class InputReader(BaseInputReader):

    mapping = None
    parser_names = None
    #temp_dir_path: str = None

    def __init__(self, map_path, input_path, output_path):
        logging.info("Preparing parsers based on parsing map file and input.")
        self.mapping = load_json(map_path)
        self.output_path = output_path
        super().__init__(map_path, input_path)
        
        if is_zipfile(self.input_path):
            # THIS PART CHECKS WHETHER THE USER DID NOT SPECIFIED THE CORRECT OUTPUT_PATH EXTENSION,
            # PARTICULARLY PREVENTING MISUSE OF THE .JSON EXTENSION, WHICH CAN BE EASILY MISTAKEN.
            # THIS CHECK CAN BE IMPROVE FOR A STANDALONE USE, BUT WE STICK ON THIS SIMPLE CHECK BECAUSE THE MAPPING SERVICE RENAMES THE IO FILES AND HANDLES CORRECTLY THE EXTENSIONS 
            #if output_path.lower().endswith('.json'):
                #logging.error("The output path {} is expecting the extension '.zip' since the input is a zip file".format(output_path))
                #raise MappingAbortionError("Input file parsing aborted.")
            #self.temp_dir_path = extract_zip_file(input_path)
            self._handle_zip_input(self.input_path, self.output_path)
        else:
            #if not output_path.lower().endswith('.json'):
                #logging.warning("The output path {} is expecting the extension '.json'.".format(output_path))
            #self.parser_names = self.get_applicable_parsers(input_path)

            #if not self.parser_names:
                #logging.error("No applicable parsers found for input {}".format(input_path))
                #mimetype_set = list(set([v.expected_input_format() for v in ParserFactory.available_img_parsers.values()]))
                #logging.info("Supported mimetypes: {}".format(mimetype_set))
                #raise MappingAbortionError("Input file parsing aborted.")
            #logging.info("Applicable parsers: {}".format(", ".join(self.parser_names)))
            self._handle_single_input(self.input_path)


    def _handle_zip_input(self, input_path: str, output_path: str):
        """
        Handles zipped input files: Extract and detect applicable parsers.
        """
        # THIS PART CHECKS WHETHER THE USER DID NOT SPECIFIED THE CORRECT OUTPUT_PATH EXTENSION,
        # PARTICULARLY PREVENTING MISUSE OF THE .JSON EXTENSION, WHICH CAN BE EASILY MISTAKEN.
        # THIS CHECK CAN BE IMPROVE FOR A STANDALONE USE, BUT WE STICK ON THIS SIMPLE CHECK BECAUSE THE MAPPING SERVICE RENAMES THE IO FILES AND HANDLES CORRECTLY THE EXTENSIONS
        if output_path.lower().endswith('.json'):
            logging.error(f"Expected '.zip' output path for zipped input '{input_path}', got '.json' instead.")
            raise MappingAbortionError("Output path extension mismatch for zipped input.")

        self.temp_dir_path = extract_zip_file(input_path)
        found_valid_parser = False

        for file_path in self.filter_zipfile(self.temp_dir_path):
            self.parser_names = self.get_applicable_parsers(file_path)
            if self.parser_names:
                found_valid_parser = True
                logging.info("Valid parsers found for files in the zip archive.")
                break

        if not found_valid_parser:
            logging.warning("There is no valid files in the zipped input file !")
            self._log_no_parser_error(input_path)

    def _handle_single_input(self, input_path: str):
        """
        Handles single input file: Detect applicable parsers.
        """
        self.parser_names = self.get_applicable_parsers(input_path)

        if not self.parser_names:
            self._log_no_parser_error(input_path)
        else:
            logging.info("Applicable parsers: {}".format(", ".join(self.parser_names)))

    def filter_zipfile(self, tmpdir: str):
        valid_filePaths = []
        for file_path in Path(tmpdir).rglob('*'):
            if not file_path.is_file():
                # No directory path is allowed. Only process files
                logging.debug(f"Skipping {file_path} as it is probably a directory.")
                continue
            if '__MACOSX' in str(file_path):
                logging.debug(f"Skipping macOS metadata file: {file_path}")
                continue
            valid_filePaths.append(file_path)
        return valid_filePaths
    
    @staticmethod
    def _log_no_parser_error(input_path: str):
        """
        Logs a detailed error when no parser is found.
        """
        logging.error("No applicable parsers found for input {}".format(input_path))
        mimetype_set = list(set([v.expected_input_format() for v in ParserFactory.available_img_parsers.values()]))
        logging.info("Supported mimetypes: {}".format(mimetype_set))
        raise MappingAbortionError("Input file parsing aborted.")

    @staticmethod
    def get_applicable_parsers(input_path, by_extension = False):
        """
        Filters the available image parsers to those applicable to the input file format.
        It tries to determine by extension, but can fallback to using magica.
        :param by_extension: set to True if guessing by extension should be used.
        :param input_path: file path to input
        :return: list of parser names that can handle the provided input format
        """
        applicable_types = [ip.expected_input_format() for ip in ParserFactory.available_img_parsers.values()]

        mt = None
        if by_extension:
            mt, _ = mimetypes.guess_type(input_path)
            logging.debug("Mimetypes file identification result: {}".format(mt))
        if not mt or mt == "application/unknown" or mt not in applicable_types: #fallback, especially if file extension is not available
            #Text files are tricky with magica, so try to read as such first
            mt = get_filetype_with_magica(input_path)
            logging.debug("Magika file identification result: {}".format(mt))
            # This part tends to also position TxtParser as a fallback solution. Need to be improved.
            if mt not in applicable_types:
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
