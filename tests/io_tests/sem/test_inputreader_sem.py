import os
import shutil
import tempfile
import pytest
import zipfile

from src.IO.sem.InputReader import InputReader
from src.parser.impl.TiffParser import TiffParser

from src.IO.MappingAbortionError import MappingAbortionError


class TestInputReader:

    def set_up_sample_data(self):
        dir_to_testscript = os.path.split(__file__)[0]

        test_path = os.path.join(dir_to_testscript, "../../sampleData/")
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
        mocker.patch('src.parser.impl.TiffParser.TiffParser.expected_input', self.return_plaintext_format())
        assert TiffParser.expected_input_format() == "text/plain"

        jeolfile = os.path.join(tp, "./images/SEM/JEOL/image000.txt")

        parsers = InputReader.get_applicable_parsers(jeolfile)
        assert len(parsers) >= 1

    def test_get_applicable_parsers_wo_extension(self, mocker):
        tp = self.set_up_sample_data()

        ret = "text/plain"
        mocker.patch('src.parser.impl.TiffParser.TiffParser.expected_input', self.return_plaintext_format())
        assert TiffParser.expected_input_format() == "text/plain"

        jeolfile = os.path.join(tp, "./images/SEM/JEOL/image000")

        parsers = InputReader.get_applicable_parsers(jeolfile)
        assert len(parsers) >= 1

    def test_filter_zipfile(self):
        tp = self.set_up_sample_data()
        zpfile = os.path.join(tp, "Archive.zip")

        # Extract Archive.zip into a temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zpfile, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # Create instance without calling __init__ 
            # because we want to test filter_zipfile as a static method although it is an instance method.
            reader = InputReader.__new__(InputReader)

            filtered = reader.filter_zipfile(tmpdir)

            # Check that we have non-zero filtered files
            assert filtered, "Expected at least one valid file in filtered result"

            # Optional: check that no macOSX or dirs are present
            #filteredPaths = [f.name for f in filtered]
            assert all("__MACOSX" not in os.path.basename(fp) for fp in filtered), "Found __MACOSX file"
            assert all(os.path.isfile(fp) for fp in filtered), "Non-file returned"

    def test_handle_zip_input_with_valid_archive_zip(self):
        tp = self.set_up_sample_data()
        zpfile = os.path.join(tp, "Archive.zip") # contains at least one file with applicable parser
        output_path = "output.zip"  # Valid .zip output path

        # Create instance without calling __init__ 
        # because we will test filter_zipfile as a static method although it is an instance method.
        reader = InputReader.__new__(InputReader)

        reader._handle_zip_input(zpfile, output_path)
        assert reader.parser_names

    def test_handle_zip_input_with_non_valid_archive_zip(self):
        tp = self.set_up_sample_data()
        zpfile = os.path.join(tp, "DummyArchive.zip") # No file with applicable parser
        output_path = "output.zip"  # Valid .zip output path

        reader = InputReader.__new__(InputReader)
        with pytest.raises(MappingAbortionError):#, match="Input file parsing aborted"): # The msg might change, be aware!
            reader._handle_zip_input(zpfile, output_path)
        assert reader.parser_names is None

    def test_handle_zip_input_rejects_json_output(self):
        tp = self.set_up_sample_data()
        zpfile = os.path.join(tp, "Archive.zip") # valid input

        output_path = "output.json" # non valid output

        reader = InputReader.__new__(InputReader)
        with pytest.raises(MappingAbortionError):#, match="Output path extension mismatch"): # The msg might change, be aware!
            reader._handle_zip_input(zpfile, output_path)
        assert reader.temp_dir_path is None

