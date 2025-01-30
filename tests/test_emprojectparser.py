import unittest

from src.parser.EMProjectParser import EMProjectParser


class TestEmprojectParser(unittest.TestCase):

    def setUp(self):
        with open("./sampleData/EMProject.emxml", "r") as xmlPayload:
            self.payload = xmlPayload.read()


    def test_setup(self):
        # TODO: You are not a real test yet
        parser = EMProjectParser()
        acqu, raw = parser.parse(self.payload)
        print(acqu.to_schema_dict())
        print(raw)
