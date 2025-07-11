import glob
import os
from pprint import pprint

import pytest

from tomo_mapper.config import MappingConfig
from tomo_mapper.parser.ImageParser import ParserMode
from tomo_mapper.parser.impl.TiffParser import TiffParser
from tomo_mapper.resources.maps.mapping import tiffparser_sem_34118, tiffparser_sem_34682
from tomo_mapper.util import load_json, input_to_dict


class TestTiffparser:

    def test_tiffparser_tomo(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        try:
            test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SEM_Image-SliceImage-001.tif")

            parser = TiffParser(ParserMode.TOMO, "34682")
            img, raw = parser.parse(test_tiffpath, None)
            pprint(raw)

            pprint(img.acquisition_info.to_schema_dict())
            pprint(img.dataset_metadata.to_schema_dict())
            pprint(img.image_metadata.to_schema_dict())
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_tiffparser_sem(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        try:
            test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SEM_Image-SliceImage-001.tif")

            parser = TiffParser(ParserMode.SEM, "34682")
            SEM_map = input_to_dict(tiffparser_sem_34682.read_text())
            img, raw = parser.parse(test_tiffpath, SEM_map)
            #pprint(raw)

            pprint(img.image_metadata.to_schema_dict())
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_zeiss(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        try:
            test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SESI_slice_00000_z=0.5100um.tif")

            parser = TiffParser(ParserMode.TOMO, "51023")
            img, raw = parser.parse(test_tiffpath, None)
            pprint(raw)

            pprint(img.acquisition_info.to_schema_dict())
            pprint(img.dataset_metadata.to_schema_dict())
            pprint(img.image_metadata.to_schema_dict())
        except FileNotFoundError:
            pytest.skip("Test file not included, skipping test")

    def test_sem_zeiss(self):
        parser = TiffParser(ParserMode.SEM)

        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        zeiss_glob = glob.glob(os.path.normpath(os.path.join(dir_to_testscript, "../sampleData/images/SEM/Zeiss/*.tif")))

        if len(zeiss_glob) == 0:
            pytest.skip("Test files not included, skipping test")

        mapping_dict = input_to_dict(tiffparser_sem_34118.read_text())

        for zg in zeiss_glob:
            img, raw = parser.parse(zg, mapping_dict)
            #pprint(raw)

            pprint(img.image_metadata.to_schema_dict())

    def test_sem_tf(self):
        parser = TiffParser(ParserMode.SEM)

        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        tf_glob = glob.glob(os.path.normpath(os.path.join(dir_to_testscript, "../sampleData/images/SEM/TF-FEI/*.tif")))
        if len(tf_glob) == 0:
            pytest.skip("Test files not included, skipping test")

        mapping_dict = input_to_dict(tiffparser_sem_34682.read_text())

        for zg in tf_glob:
            img, raw = parser.parse(zg, mapping_dict)
            #pprint(raw)

            pprint(img.image_metadata.to_schema_dict())