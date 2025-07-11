import logging
from typing import Dict, Type

from tomo_mapper.parser.ImageParser import ImageParser
from tomo_mapper.parser.RunMD_Parser import RunMD_Parser
from tomo_mapper.parser.SetupMD_Parser import SetupMD_Parser
from tomo_mapper.parser.impl.Atlas3dParser import Atlas3dParser
from tomo_mapper.parser.impl.EMProjectParser import EMProjectParser
from tomo_mapper.parser.impl.ProjectDataParser import ProjectDataParser
from tomo_mapper.parser.impl.TomographyProjectParser import TomographyProjectParser
from tomo_mapper.parser.impl.Dataset_infoParser import Dataset_infoParser
from tomo_mapper.parser.impl.TiffParser import TiffParser
from tomo_mapper.parser.impl.TxtParser import TxtParser


class ParserFactory:

    available_setupmd_parsers: Dict[str, Type[SetupMD_Parser]]  = {
        "EMProjectParser": EMProjectParser,
        "Atlas3DParser": Atlas3dParser,
        "TomographyProjectParser": TomographyProjectParser,
        "Dataset_infoParser": Dataset_infoParser
    }

    available_runmd_parsers: Dict[str, Type[RunMD_Parser]] = {
        "ProjectDataParser": ProjectDataParser,
        "Atlas3DParser": Atlas3dParser
    }

    available_img_parsers = {
        "TiffParser": TiffParser,
        "TxtParser": TxtParser
    }

    @staticmethod
    def create_setupmd_parser(parser_name) -> SetupMD_Parser:
        parser_class = ParserFactory.available_setupmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_setupmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @staticmethod
    def create_runmd_parser(parser_name) -> RunMD_Parser:
        parser_class = ParserFactory.available_runmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_runmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @staticmethod
    def create_img_parser(parser_name, **kwargs) -> ImageParser:
        parser_class = ParserFactory.available_img_parsers.get(parser_name)
        if parser_class:
            return parser_class(**kwargs)
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_img_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")