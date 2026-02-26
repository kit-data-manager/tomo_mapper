import logging
from typing import Type

from mappingservice_plugincore.mappingservice_plugincore.parser.ImageParser import ImageParser
from mappingservice_plugincore.mappingservice_plugincore.parser.RunMD_Parser import RunMD_Parser
from mappingservice_plugincore.mappingservice_plugincore.parser.SetupMD_Parser import SetupMD_Parser


class ParserFactory:

    available_setupmd_parsers: dict[str, Type[SetupMD_Parser]]  = {
    }

    available_runmd_parsers: dict[str, Type[RunMD_Parser]] = {
    }

    available_img_parsers = {
    }

    @classmethod
    def register_setupmdparser(cls, name, parser_cls: Type[SetupMD_Parser]):
        cls.available_setupmd_parsers[name] = parser_cls

    @classmethod
    def register_runmdparser(cls, name, parser_cls):
        cls.available_runmd_parsers[name] = parser_cls

    @classmethod
    def register_imgparser(cls, name, parser_cls):
        cls.available_img_parsers[name] = parser_cls

    @classmethod
    def create_setupmd_parser(cls, parser_name) -> SetupMD_Parser:
        parser_class = ParserFactory.available_setupmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_setupmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @classmethod
    def create_runmd_parser(cls, parser_name) -> RunMD_Parser:
        parser_class = ParserFactory.available_runmd_parsers.get(parser_name)
        if parser_class:
            return parser_class()
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_runmd_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")

    @classmethod
    def create_img_parser(cls, parser_name, **kwargs) -> ImageParser:
        parser_class = ParserFactory.available_img_parsers.get(parser_name)
        if parser_class:
            return parser_class(**kwargs)
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_img_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")