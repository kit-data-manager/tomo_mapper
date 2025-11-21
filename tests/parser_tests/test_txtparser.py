import glob
import os
from pprint import pprint

import pytest

from src.config import MappingConfig
from src.parser.ImageParser import ParserMode
from src.parser.impl.TxtParser import TxtParser
from src.resources.maps.mapping import textparser_sem_tescan, textparser_sem_jeol
from src.util import load_json, input_to_dict


class TestTXTparser:

    def test_sem_tescan(self):
        parser = TxtParser(ParserMode.SEM)

        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        tesc_glob = glob.glob(os.path.normpath(os.path.join(dir_to_testscript, "../sampleData/images/SEM/TESCAN/*.hdr")))
        if len(tesc_glob) == 0:
            pytest.skip("Test files not included, skipping test")

        mapping_dict = input_to_dict(textparser_sem_tescan.read_text())

        for zg in tesc_glob:
            img = parser.parse(zg, mapping_dict)
            #pprint(raw)
            
            if img and img.image_metadata:
                pprint(img.image_metadata.to_schema_dict())

    def test_sem_jeol(self):
        parser = TxtParser(ParserMode.SEM)

        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        tesc_glob = glob.glob(os.path.normpath(os.path.join(dir_to_testscript, "../sampleData/images/SEM/JEOL/*.txt")))
        if len(tesc_glob) == 0:
            pytest.skip("Test files not included, skipping test")

        mapping_dict = input_to_dict(textparser_sem_jeol.read_text())

        for zg in tesc_glob:
            img = parser.parse(zg, mapping_dict)
            #pprint(raw)

            if img and img.image_metadata:
                pprint(img.image_metadata.to_schema_dict())