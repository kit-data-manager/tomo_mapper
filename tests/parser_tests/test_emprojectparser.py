import os
from pprint import pprint

from src import EMProjectParser


class TestEmprojectParser:

    def setUp(self):
        dir_to_testscript = os.path.split(__file__)[0]

        test_path = os.path.join(dir_to_testscript, "../sampleData/EMProject.emxml")
        print(test_path)
        print(os.getenv('PYTEST_CURRENT_TEST'))
        with open(test_path, "r") as xmlPayload:
            self.payload = xmlPayload.read()


    def test_setup(self):
        self.setUp()
        # TODO: You are not a real test yet
        parser = EMProjectParser()
        setupmd, raw = parser.parse_setup(self.payload)
        print(setupmd.__dict__)
        print(raw)
        pprint(setupmd.acquisition_metadata.to_schema_dict())
