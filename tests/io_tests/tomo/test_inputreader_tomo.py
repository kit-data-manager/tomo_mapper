import json
import os
import tempfile

import pytest

from src.IO.MappingAbortionError import MappingAbortionError
from src.IO.tomo.InputReader import InputReader
from src.model.RunMD import RunMD
from src.util import is_zipfile


class TestInputReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]

        test_path = os.path.join(dir_to_testscript, "../../sampleData/")
        return test_path

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
    def mapfile(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
            json.dump(self.mapdata, temp_file)
            temp_file_path = temp_file.name
        yield temp_file_path
        # Cleanup after test
        try:
            os.remove(temp_file_path)
        except OSError:
            pass

    def override_mapdata(self, mapfile, new_mapdata):
        with open(mapfile, "w") as f:
            json.dump(new_mapdata, f)

    def test_inputreader_with_folder(self, mapfile, mocker):
        """
        Test sample data folder and setup parser
        """
        datapath = self.set_up_sample_data()
        mocker.patch('src.parser.impl.ProjectDataParser.ProjectDataParser.parse_run', return_value=(RunMD(), {}))
        ir = InputReader(mapfile, datapath)

        ir.retrieve_setup_info()
        ir.retrieve_run_info()
        ir.retrieve_image_info()

    def test_inputreader_with_zip(self, mapfile):
        """
        Test simple zip, no setup parser, no run parser
        """
        datapath = self.set_up_sample_data()
        testpath = os.path.join(datapath, "images", "dummyimage.zip")
        test_data = self.mapdata.copy()
        test_data["image info"]["sources"][0] = "./*.png"
        del test_data["setup info"]
        del test_data["run info"]
        self.override_mapdata(mapfile, test_data)
        assert os.path.isfile(testpath)

        ir = InputReader(mapfile, testpath)

        ir.retrieve_setup_info()
        ir.retrieve_setup_info()
        ir.retrieve_image_info()

    def test_inputreader_with_unsuitable_map(self, mapfile):
        """
        Test image file instead of json input for map
        """
        datapath = self.set_up_sample_data()
        testpath = os.path.join(datapath, "images", "SEM_Image-SliceImage-001.tif")
        assert os.path.isfile(testpath)

        with pytest.raises(MappingAbortionError):
            InputReader(testpath, datapath)

    def test_inputreader_missing_input(self, mapfile):
        """
        Test map file with missing setup file
        """
        test_data = self.mapdata.copy()
        test_data["setup info"]["sources"][0] = "./file_not_exists.emxml"
        self.override_mapdata(mapfile, test_data)
        datapath = self.set_up_sample_data()

        with pytest.raises(MappingAbortionError):
            InputReader(mapfile, datapath)
