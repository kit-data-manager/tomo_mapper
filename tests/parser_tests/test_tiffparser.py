import unittest

from src.parser.TiffParser import TiffParser


class TestTiffparser(unittest.TestCase):

    def test_tiffparser(self):
        #TODO: You are not a real test yet
        test_tiffpath = "./sampleData/images/SEM Image - SliceImage - 001.tif"

        parser = TiffParser("34682")
        img, raw = parser.parse(test_tiffpath, ("TF", "TOMO_Schema"))
        print(img.as_tomo_dict())
        print(raw)