import logging

from src.parser.Atlas3dParser import Atlas3dParser
from src.parser.EMProjectParser import EMProjectParser
from src.parser.TiffParser import TiffParser


class ParserFactory:

    available_md_parsers = {
        "EMProjectParser": EMProjectParser,
        "Atlas3DParser": Atlas3dParser
    }

    available_img_parsers = {
        "TiffParser": TiffParser
    }

    @staticmethod
    def create_md_parser(parser_name):
        parser_class = ParserFactory.available_md_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_md_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @staticmethod
    def create_img_parser(parser_name, **kwargs):
        parser_class = ParserFactory.available_img_parsers.get(parser_name)
        if parser_class:
            return parser_class(**kwargs)
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_img_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")