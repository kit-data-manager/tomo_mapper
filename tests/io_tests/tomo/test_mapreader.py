import json
import os
import sys
import tempfile

import pytest

from tomo_mapper.IO.tomo.MapfileReader import MapFileReader
from tomo_mapper.parser.impl.Atlas3dParser import Atlas3dParser

from tomo_mapper.parser.impl.Dataset_infoParser import Dataset_infoParser
from tomo_mapper.parser.impl.ProjectDataParser import ProjectDataParser
from tomo_mapper.parser.impl.TomographyProjectParser import TomographyProjectParser

class TestMapfileReader:

    mapdata = {
            "setup info": {
                "sources": [
                    "./EMProject.emxml"
                ],
                "parser": "EMProjectParser"
            },
            "run info": {
                "sources": [
                    "./EMProject.emxml"
                ],
                "parser": "ProjectDataParser"
            },
            "image info": {
                "sources": [
                    "./images/*.tif"
                ],
                "tag": "34682",
                "parser": "TiffParser"
            }
        }

    @pytest.fixture
    def mapfile_latin1(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="latin1") as temp_file:
            json.dump(self.mapdata, temp_file)
            temp_file_path = temp_file.name
        yield temp_file_path
        # Cleanup after test
        try:
            os.remove(temp_file_path)
        except OSError:
            pass

    def test_mapfile_latin1(self, mapfile_latin1):
        """
        Test sample data folder and setup parser
        """
        mapdict = MapFileReader.read_mapfile(mapfile_latin1)
        assert mapdict == self.mapdata

    def create_absolute_path(self):
        if sys.platform.startswith("Windows"):
            return r"C:\absolute\path.tif"
        else:
            return "/absolute/path.tif"

    def test_imageinfo(self):
        test_map = {
        }

        with pytest.raises(ValueError):
            MapFileReader.parse_mapinfo_for_images(test_map)

        test_map["image info"] = {}

        with pytest.raises(ValueError):
            MapFileReader.parse_mapinfo_for_images(test_map)

        test_map["image info"]["sources"] = [self.create_absolute_path()]
        test_map["image info"]["parser"] = "TiffParser"

        with pytest.raises(ValueError):
            MapFileReader.parse_mapinfo_for_images(test_map)

        test_map["image info"]["sources"] = ["./relative/path.tif"]
        MapFileReader.parse_mapinfo_for_images(test_map)

    def test_single_parser_multiple_sources_setup(self):
        """
        Test single parser applied to multiple sources
        """
        test_map = {
            "setup info": {
                "sources": ["./src1.xml", "./src2.xml"],
                "parser": "TomographyProjectParser"
            }
        }
        setupmdPairs = MapFileReader.parse_mapinfo_for_setup(test_map)
        for item in setupmdPairs: # [("./src1.xml", <"TomographyProjectParser" instance>), ("./src2.xml", <"TomographyProjectParser" instance>)]
            assert len(item) == 2
        assert len(setupmdPairs) == 2
        assert isinstance(setupmdPairs[0][1], TomographyProjectParser)
        assert isinstance(setupmdPairs[1][1], TomographyProjectParser)

    def test_parser_sources_list_matching_setup(self):
        """
        Test matching list of parsers and sources
        """
        test_map = {
            "setup info": {
                "sources": ["./src1.hdr", "./src2.xml"],
                "parser": ["Dataset_infoParser", "TomographyProjectParser"]
            }
        }
        setupmdPairs = MapFileReader.parse_mapinfo_for_setup(test_map)
        for item in setupmdPairs: # [("./src1.hdr", <"TomographyProjectParser" instance>), ("./src2.xml", <"TomographyProjectParser" instance>)]
            assert len(item) == 2
        assert len(setupmdPairs) == 2
        assert isinstance(setupmdPairs[0][1], Dataset_infoParser)
        assert isinstance(setupmdPairs[1][1], TomographyProjectParser)

    def test_single_parser_multiple_sources_run(self):
        """
        Test single parser applied to multiple sources
        """
        test_map = {
            "run info": {
                "sources": ["./src1.xml", "./src2.xml"],
                "parser": "Atlas3DParser"
            }
        }
        runmdPairs = MapFileReader.parse_mapinfo_for_run(test_map)
        for item in runmdPairs: # [("./src1.xml", <"TomographyProjectParser" instance>), ("./src2.xml", <"TomographyProjectParser" instance>)]
            assert len(item) == 2
        assert len(runmdPairs) == 2
        assert isinstance(runmdPairs[0][1], Atlas3dParser)
        assert isinstance(runmdPairs[1][1], Atlas3dParser)

    def test_parser_sources_list_matching_run(self):
        """
        Test matching list of parsers and sources
        """
        test_map = {
            "run info": {
                "sources": ["./src1.xml", "./src2.xml"],
                "parser": ["ProjectDataParser", "Atlas3DParser"]
            }
        }
        runmdPairs = MapFileReader.parse_mapinfo_for_run(test_map)
        for item in runmdPairs: # [("./src1.hdr", <"TomographyProjectParser" instance>), ("./src2.xml", <"TomographyProjectParser" instance>)]
            assert len(item) == 2
        assert len(runmdPairs) == 2
        assert isinstance(runmdPairs[0][1], ProjectDataParser)
        assert isinstance(runmdPairs[1][1], Atlas3dParser)

