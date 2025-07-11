import os

from tomo_mapper.IO.sem.InputReader import InputReader
from tomo_mapper.parser.impl.TiffParser import TiffParser


class TestInputReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]

        test_path = os.path.join(dir_to_testscript, "../../sampleData/")
        print(test_path)
        return test_path

    def return_plaintext_format(self):
        return "text/plain"

    def test_get_applicable_tiffparser(self, mocker):
        tp = self.set_up_sample_data()

        tffile = os.path.join(tp, "./images/SEM_Image-SliceImage-001.tif")

        parsers = InputReader.get_applicable_parsers(tffile)
        assert len(parsers) >= 1

        tffile = os.path.join(tp, "./images/SEM_Image-SliceImage-001")

        parsers = InputReader.get_applicable_parsers(tffile)
        assert len(parsers) >= 1

    def test_get_applicable_parsers_with_extension(self, mocker):
        tp = self.set_up_sample_data()

        ret = "text/plain"
        mocker.patch('tomo_mapper.parser.impl.TiffParser.TiffParser.expected_input', self.return_plaintext_format())
        assert TiffParser.expected_input_format() == "text/plain"

        jeolfile = os.path.join(tp, "./images/SEM/JEOL/image000.txt")

        parsers = InputReader.get_applicable_parsers(jeolfile)
        assert len(parsers) >= 1

    def test_get_applicable_parsers_wo_extension(self, mocker):
        tp = self.set_up_sample_data()

        ret = "text/plain"
        mocker.patch('tomo_mapper.parser.impl.TiffParser.TiffParser.expected_input', self.return_plaintext_format())
        assert TiffParser.expected_input_format() == "text/plain"

        jeolfile = os.path.join(tp, "./images/SEM/JEOL/image000")

        parsers = InputReader.get_applicable_parsers(jeolfile)
        assert len(parsers) >= 1
