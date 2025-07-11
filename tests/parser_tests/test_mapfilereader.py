import platform
from glob import glob
import os

import pytest

from tomo_mapper.IO.MappingAbortionError import MappingAbortionError
from tomo_mapper.IO.tomo.MapfileReader import MapFileReader
from tomo_mapper.parser.impl.Atlas3dParser import Atlas3dParser
from tomo_mapper.parser.impl.EMProjectParser import EMProjectParser
from tomo_mapper.parser.impl.TiffParser import TiffParser


class TestMapfileReader:

    testpath = os.path.split(__file__)[0]

    def test_pathvalidation(self):

        if platform.platform() == "Windows": #we likely will not encounter any absolute paths in windows format on other OS and this test case fails on those OS
            with pytest.raises(ValueError):
                MapFileReader.validate_relative_path(r"C:\absolute_windows_path\directory")

        with pytest.raises(ValueError):
            MapFileReader.validate_relative_path("/c/absolute_unix_path/directory")

        with pytest.raises(ValueError):
            MapFileReader.validate_relative_path("/User/someone/directory")

        with pytest.raises(ValueError):
            MapFileReader.validate_relative_path("http://remote_directory")

        assert MapFileReader.validate_relative_path("./correct_dir")

        assert MapFileReader.validate_relative_path("../correct/**/wildcard_path")

    def test_loading_default_maps(self):
        sourcesPath = os.path.join(self.testpath, "../../src/tomo_mapper/resources/maps/parsing/inputmap_*.json")
        map_sources = glob(sourcesPath)

        assert len(map_sources) > 0

        for ms in map_sources:
            #test only checks if loading as dict is successful
            map_content = MapFileReader.read_mapfile(ms)
            assert map_content is not None
            assert type(map_content) == dict


    def test_parsing_default_maps(self):
        sourcesPath = os.path.join(self.testpath, "../../src/tomo_mapper/resources/maps/parsing/inputmap_*.json")
        map_sources = glob(sourcesPath)

        available_ac_parsers = {
            "EMProjectParser": EMProjectParser,
            "Atlas3DParser": Atlas3dParser
        }

        available_im_parsers = {
            "TiffParser": TiffParser,
        }

        assert len(map_sources) > 0

        for ms in map_sources:
            # test only checks if loading as dict is successful
            map_content = MapFileReader.read_mapfile(ms)
            MapFileReader.parse_mapinfo_for_setup(map_content)
            MapFileReader.parse_mapinfo_for_images(map_content)

    def test_parsing_latin1_map(self):
        sourcesPath = os.path.join(self.testpath, "../sampleData/config/inputmap_thermofisher_latin1.json")
        map_content = MapFileReader.read_mapfile(sourcesPath)

        assert type(map_content) == dict

    def test_reject_binary_as_map(self):
        sourcesPath = os.path.join(self.testpath, "../sampleData/images/dummyimage.zip")

        with pytest.raises(MappingAbortionError):
            map_content = MapFileReader.read_mapfile(sourcesPath)

    def test_reject_nonjson_as_map(self):
        sourcesPath = os.path.join(self.testpath, "../sampleData/config/faulty.txt")

        with pytest.raises(MappingAbortionError):
            map_content = MapFileReader.read_mapfile(sourcesPath)

    def test_fail_on_missing_parser(self):

        mapping_content = {
            "setup info": {
                "sources": ["./mdfilepath"],
                "parser": "NotARealParser"
            }
        }

        with pytest.raises(ValueError):
            MapFileReader.parse_mapinfo_for_setup(mapping_content)

