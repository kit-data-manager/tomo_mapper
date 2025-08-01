import os
import tempfile
from pprint import pprint

import pytest

from mapping_cli import run_tomo_mapper

class TestInputFolder:

    class Config:
        input = ""
        output = ""
        map = ""

        def __init__(self, input_fp, output_fp, map_fp):
            self.input = input_fp
            self.output = output_fp
            self.map = map_fp

    def test_image_folder(self):
        """
        Test folder only contains images in nested folders
        No run md, no setup md

        expected results:
        the 3 images from 3 folders are sorted into 3 datasets
        :return:
        """
        #MappingConfig.set_working_dir("/")
        dir_to_testscript = os.path.split(__file__)[0]
        test_path = os.path.join(dir_to_testscript, "../../sampleData/testinput_folders/minimal")
        assert os.path.exists(test_path)
        map_path = os.path.join(test_path, "input_map.json")
        assert os.path.exists(map_path)
        assert os.path.isfile(map_path)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            output_path = tmp_file.name
        conf = self.Config(test_path, output_path, map_path)

        output = run_tomo_mapper(conf)
        pprint(output)
        assert len(output["acquisition"]["dataset"]) == 3
        os.remove(output_path)