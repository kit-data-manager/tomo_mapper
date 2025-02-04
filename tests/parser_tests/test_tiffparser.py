import unittest
import os

from src.parser.TiffParser import TiffParser


class TestTiffparser(unittest.TestCase):

    def test_tiffparser(self):
        #TODO: You are not a real test yet
        dir_to_testscript = os.path.split(__file__)[0]

        test_tiffpath = os.path.join(dir_to_testscript, "../sampleData/images/SEM_Image-SliceImage-001.tif")

        parser = TiffParser("34682")
        img, raw = parser.parse(test_tiffpath)
        print(img.as_tomo_dict())
        print(raw)