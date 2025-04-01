import json
import os
import sys
import tempfile

import pytest

from src.IO.tomo.MapfileReader import MapFileReader

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
