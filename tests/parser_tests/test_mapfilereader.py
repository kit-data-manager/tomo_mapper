import unittest
from glob import glob

from src.MapfileReader import MapFileReader
from src.parser.Atlas3dParser import Atlas3dParser
from src.parser.EMProjectParser import EMProjectParser
from src.parser.TiffParser import TiffParser


class TestMapfileReader(unittest.TestCase):

    def test_pathvalidation(self):
        self.assertRaises(ValueError, MapFileReader.validate_relative_path, r"C:\absolute_windows_path\directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "/c/absolute_unix_path\directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "/User/someone/directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "http://remote_directory")

        self.assertTrue(MapFileReader.validate_relative_path("./correct_dir"))

        self.assertTrue(MapFileReader.validate_relative_path("../correct/**/wildcard_path"))

    def test_loading_default_maps(self):

        map_sources = glob("../../src/resources/maps/parsing/inputmap_*.json")

        for ms in map_sources:
            #test only checks if loading as dict is successful
            map_content = MapFileReader.read_mapfile(ms)
            self.assertIsNotNone(map_content)
            self.assertIs(type(map_content), dict)


    def test_parsing_default_maps(self):
        map_sources = glob("../../src/resources/maps/parsing/inputmap_*.json")

        available_ac_parsers = {
            "EMProjectParser": EMProjectParser,
            "Atlas3DParser": Atlas3dParser
        }

        available_im_parsers = {
            "TiffParser": TiffParser,
        }

        for ms in map_sources:
            # test only checks if loading as dict is successful
            map_content = MapFileReader.read_mapfile(ms)
            MapFileReader.parse_mapinfo_for_acquisition(map_content, available_ac_parsers)
            MapFileReader.parse_mapinfo_for_images(map_content, available_im_parsers)

    def test_fail_on_missing_parser(self):

        mapping_content = {
            "acquisition info": {
                "sources": ["./mdfilepath"],
                "parser": "Atlas3DParser"
            }
        }

        available_ac_parsers = {
            "EMProjectParser": EMProjectParser
        }

        self.assertRaises(ValueError, MapFileReader.parse_mapinfo_for_acquisition, mapping_content, available_ac_parsers)

