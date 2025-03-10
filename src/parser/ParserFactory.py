import logging

from src.parser.impl.Atlas3dParser import Atlas3dParser
from src.parser.impl.EMProjectParser import EMProjectParser
from src.parser.impl.ProjectDataParser import ProjectDataParser
from src.parser.impl.TiffParser import TiffParser


class ParserFactory:

    available_setupmd_parsers = {
        "EMProjectParser": EMProjectParser,
        "Atlas3DParser": Atlas3dParser
    }

    available_runmd_parsers = {
        "ProjectDataParser": ProjectDataParser,
        "Atlas3DParser": Atlas3dParser
    }

    available_img_parsers = {
        "TiffParser": TiffParser
    }

    @staticmethod
    def create_setupmd_parser(parser_name):
        parser_class = ParserFactory.available_setupmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_setupmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @staticmethod
    def create_runmd_parser(parser_name):
        parser_class = ParserFactory.available_runmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_runmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @staticmethod
    def create_img_parser(parser_name, **kwargs):
        parser_class = ParserFactory.available_img_parsers.get(parser_name)
        if parser_class:
            return parser_class(**kwargs)
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_img_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")