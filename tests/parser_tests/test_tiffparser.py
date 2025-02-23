import os
from pprint import pprint

from src.config import MappingConfig
from src.parser.ImageParser import ParserMode
from src.parser.impl.TiffParser import TiffParser


class TestTiffparser:

    def test_tiffparser_tomo(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SEM_Image-SliceImage-001.tif")

        parser = TiffParser("34682", ParserMode.TOMO)
        img, raw = parser.parse(test_tiffpath)
        pprint(raw)

        pprint(img.acquisition_info.to_schema_dict())
        pprint(img.dataset_metadata.to_schema_dict())
        pprint(img.image_metadata.to_schema_dict())

    def test_tiffparser_sem(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SEM_Image-SliceImage-001.tif")

        parser = TiffParser("34682", ParserMode.SEM)
        img, raw = parser.parse_wo_tag(test_tiffpath)
        pprint(raw)

        pprint(img.image_metadata.to_schema_dict())

    def test_zeiss(self):
        #TODO: You are not a real test yet
        MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]

        test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SESI_slice_00000_z=0.5100um.tif")

        parser = TiffParser("51023", ParserMode.TOMO)
        img, raw = parser.parse(test_tiffpath)
        pprint(raw)

        pprint(img.acquisition_info.to_schema_dict())
        pprint(img.dataset_metadata.to_schema_dict())
        pprint(img.image_metadata.to_schema_dict())