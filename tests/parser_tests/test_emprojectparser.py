import os
import unittest

from src.parser.EMProjectParser import EMProjectParser


class TestEmprojectParser(unittest.TestCase):

    def setUp(self):
        dir_to_testscript = os.path.split(__file__)[0]

        test_path = os.path.join(dir_to_testscript, "../sampleData/EMProject.emxml")
        print(test_path)
        print(os.getenv('PYTEST_CURRENT_TEST'))
        with open(test_path, "r") as xmlPayload:
            self.payload = xmlPayload.read()


    def test_setup(self):
        # TODO: You are not a real test yet
        parser = EMProjectParser()
        acqu, raw = parser.parse(self.payload)
        print(acqu.to_schema_dict())
        print(raw)
