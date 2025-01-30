import logging
from collections import defaultdict
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from src.model.SEM_Image import SEM_FIB_Image
from src.model.TOMO_Image import TOMO_Image
from src.parser.ImageParser import ImageParser
from src.parser.mapping_util import map_a_dict
from src.util import input_to_dict


#TODO: would this have any benefit from replacing with tifffile lib?

class TiffParser(ImageParser):

    @staticmethod
    def expected_input_format():
        return "tiff"

    def parse(self, file_path, tagID, mappingTuple) -> (TOMO_Image, str):
        input_md = self._read_input_file(file_path, tagID)

        image_md = map_a_dict(input_md, mappingTuple)

        image_from_md = self._create_image(image_md)
        image_from_md.filePath = file_path

        return image_from_md, image_md

    def _create_image(self, image_md) -> TOMO_Image:

        image_md_format = {
            "generic_metadata": image_md["acquisition"]["genericMetadata"],
            "dataset_metadata": image_md["acquisition"]["dataset"],
            "image_metadata": image_md["acquisition"]["dataset"]["images"],
        }

        return TOMO_Image(**image_md_format)

    def _read_input_file(self, file_path, tagID) -> Optional[dict]:
        metadata = None
        image = Image.open(file_path)
        exif = image.getexif()
        image.close()
        if exif is None:
            logging.warning("No EXIF data found in image {}".format(file_path))
            return metadata

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if str(tag) == tagID:
                metadata = value

        if metadata:
            dict_from_input = input_to_dict(metadata)
            if dict_from_input:
                logging.debug("Input metadata parsed from {}".format(file_path))
                return dict_from_input
            logging.error("Metadata extracted but unable convert to dictionary for further processing")
        else:
            logging.error("No matching tag found in exif data for {}".format(self.input_tag))
