import logging
from typing import Optional

from PIL import Image

from src.Preprocessor import Preprocessor
from src.model.ImageMD import ImageMD
from src.parser.ImageParser import ImageParser, ParserMode
from src.parser.mapping_util import map_a_dict
from src.resources.maps.mapping import textparser_sem_jeol, textparser_tomo_tescan
from src.util import input_to_dict
import configparser



#TODO: would this have any benefit from replacing with tifffile lib?

class TxtParser(ImageParser):

    internal_mapping = None
    def __init__(self, mode):
        if mode == ParserMode.TOMO:
            m1 = input_to_dict(textparser_tomo_tescan.read_text())
            m2 = input_to_dict(textparser_sem_jeol.read_text())
            self.internal_mapping = m1 | m2
        super().__init__(mode)

    @staticmethod
    def expected_input_format():
        return "text/plain"

    def parse(self, file_path, mapping) -> tuple[ImageMD, str]:
        input_md = self._read_input_file(file_path)
        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None, None

        if not mapping and not self.internal_mapping:
            logging.error("No mapping provided for image parsing. Aborting")
            exit(1)
        mapping_dict = mapping if mapping else self.internal_mapping
        image_md = map_a_dict(input_md, mapping_dict)
        #print("image_md: ", image_md)

        Preprocessor.normalize_all_units(image_md)
        Preprocessor.normalize_all_datetimes(image_md)

        if self.mode == ParserMode.TOMO:
            image_from_md = self._create_tomo_image(image_md, file_path)
        else:
            image_from_md = ImageMD(image_metadata=image_md, filePath="")

        #print("image_from_md: ", image_from_md)
        return image_from_md, image_md

    def _create_tomo_image(self, image_md, fp) -> ImageMD:

        image_md_format = {
            "acquisition_info": image_md["acquisition"],
            "dataset_metadata": image_md["acquisition"]["dataset"],
            "image_metadata": image_md["acquisition"]["dataset"]["images"],
            "filePath": fp
        }

        image_md_format["dataset_metadata"].pop("images")
        if image_md_format.get("image_metadata"):
            image_md_format["image_metadata"]["localPath"] = fp

        return ImageMD(**image_md_format)

    def _read_input_file(self, file_path) -> Optional[dict]:
        """
        Reading input may be done with a predefined tag or without. In the latter case we try to extract from all tags and use the joint dictionary for mapping.
        :param file_path: image file path
        :param tagID: tag to extract from, may be None
        :return: data from extracted tag(s) as dict
        """
        #print(f"I am trying to read a {file_path}")

        config = configparser.ConfigParser(allow_no_value=True, delimiters=(" "))
        config.optionxform = str

        # Read the .txt file either as UTF-8 or a different byte format using errors="replace"
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            md = file.read()

        output_dict = {}
        output_dict.update(input_to_dict(md))

        return output_dict
