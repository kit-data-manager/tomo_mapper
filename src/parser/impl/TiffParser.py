import logging
import re
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from src.Preprocessor import Preprocessor
from src.model.ImageMD import ImageMD
from src.parser.ImageParser import ImageParser, ParserMode
from src.parser.mapping_util import map_a_dict
from src.util import input_to_dict


#TODO: would this have any benefit from replacing with tifffile lib?

class TiffParser(ImageParser):

    @staticmethod
    def expected_input_format():
        return "tiff"

    def parse(self, file_path) -> tuple[ImageMD, str]:
        input_md = self._read_input_file(file_path, self.tagID)
        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None, None

        image_md = map_a_dict(input_md, self.mapping_tuple, "image")

        Preprocessor.normalize_all_units(image_md)

        if self.mode == ParserMode.TOMO:
            image_from_md = self._create_tomo_image(image_md, file_path)
        else:
            image_from_md = ImageMD(image_metadata=image_md, filePath="")

        return image_from_md, image_md

    def parse_wo_tag(self, file_path) -> tuple[ImageMD, str]:
        input_md = self._read_input_file(file_path)
        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None, None

        image_md = map_a_dict(input_md, self.mapping_tuple, "image")

        Preprocessor.normalize_all_units(image_md)

        if self.mode == ParserMode.TOMO:
            image_from_md = self._create_tomo_image(image_md, file_path)
        else:
            image_from_md = ImageMD(image_metadata=image_md, filePath="")

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

    def _read_input_file(self, file_path, tagID = None) -> Optional[dict]:
        metadata = None
        image = Image.open(file_path)
        exif = image.getexif()
        image.close()
        if exif is None:
            logging.warning("No EXIF data found in image {}".format(file_path))
            return metadata

        if tagID:
            md_list = [x[int(tagID)] for x in exif.items()]
        else:
            md_list = [value for key, value in exif.items()]

        output_dict = {}
        for md in md_list:
            try:
                output_dict.update(input_to_dict(md))
            except Exception as e:
                logging.debug("Unable to extract metadata for {}".format(md))
                pass

        return output_dict
        '''
        if metadata:
            dict_from_input = input_to_dict(metadata)
            if dict_from_input:
                logging.debug("Input metadata parsed from {}".format(file_path))
                return dict_from_input
            logging.error("Metadata extracted but unable convert to dictionary for further processing")
        else:
            logging.error("No matching tag found in exif data for {} on {}".format(tagID, file_path))
        '''
