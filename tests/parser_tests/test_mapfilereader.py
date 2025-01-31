import unittest

from src.MapfileReader import MapFileReader
from src.parser.TiffParser import TiffParser


class TestMapfileReader(unittest.TestCase):

    def test_pathvalidation(self):

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, r"C:\absolute_windows_path\directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "/c/absolute_unix_path\directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "/User/someone/directory")

        self.assertRaises(ValueError, MapFileReader.validate_relative_path, "http://remote_directory")

        self.assertTrue(MapFileReader.validate_relative_path("./correct_dir"))

        self.assertTrue(MapFileReader.validate_relative_path("../correct/**/wildcard_path"))

