import enum
from typing import Type

from mappingservice_plugincore.parser.ParserFactory import ParserFactory
from mappingservice_plugincore.parser.RunMD_Parser import RunMD_Parser
from mappingservice_plugincore.parser.SetupMD_Parser import SetupMD_Parser
from src.parser.impl.Atlas3dParser import Atlas3dParser
from src.parser.impl.Dataset_infoParser import Dataset_infoParser
from src.parser.impl.EMProjectParser import EMProjectParser
from src.parser.impl.ProjectDataParser import ProjectDataParser
from src.parser.impl.TiffParser import TiffParser
from src.parser.impl.TomographyProjectParser import TomographyProjectParser
from src.parser.impl.TxtParser import TxtParser

available_setupmd_parsers: dict[str, Type[SetupMD_Parser]] = {
    "EMProjectParser": EMProjectParser,
    "Atlas3DParser": Atlas3dParser,
    "TomographyProjectParser": TomographyProjectParser,
    "Dataset_infoParser": Dataset_infoParser
}

available_runmd_parsers: dict[str, Type[RunMD_Parser]] = {
    "ProjectDataParser": ProjectDataParser,
    "Atlas3DParser": Atlas3dParser
}

available_img_parsers = {
    "TiffParser": TiffParser,
    "TxtParser": TxtParser
}

def register_parsers():
    for p_name, p_cls in available_setupmd_parsers.items():
        ParserFactory.register_setupmdparser(p_name, p_cls)

    for p_name, p_cls in available_runmd_parsers.items():
        ParserFactory.register_runmdparser(p_name, p_cls)

    for p_name, p_cls in available_img_parsers.items():
        ParserFactory.register_imgparser(p_name, p_cls)