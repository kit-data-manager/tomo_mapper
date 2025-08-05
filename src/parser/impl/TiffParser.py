import logging
from typing import Optional
from importlib import resources

from PIL import Image

from src.IO.MappingAbortionError import MappingAbortionError
from src.Preprocessor import Preprocessor
from src.model.ImageMD import ImageMD
from src.model.SchemaConcepts.SEM_Image import SEM_Image
from src.parser.ImageParser import ImageParser, ParserMode
from src.parser.mapping_util import map_a_dict
from src.resources.maps.mapping import tiffparser_tomo_51023, tiffparser_tomo_34682, tiffparser_sem_34682, \
    tiffparser_sem_34118
from src.util import input_to_dict


#TODO: would this have any benefit from replacing with tifffile lib?

class TiffParser(ImageParser):

    available_tomo_mappings = {
        "34682": tiffparser_tomo_34682,
        "51023": tiffparser_tomo_51023
    }

    available_sem_mappings = {
        "34682": tiffparser_sem_34682,
        "34118": tiffparser_sem_34118
    }

    expected_input = "image/tiff"
    tagID = None
    internal_mapping = None

    def __init__(self, mode, tagID=None):
        if tagID:
            self.tagID = tagID
            if mode == ParserMode.TOMO:
                if self.tagID not in self.available_tomo_mappings:
                    logging.error("Internal mapping for tag '{}' is not available".format(self.tagID))
                    raise MappingAbortionError("Setting up image parser failed.")
                m = self.available_tomo_mappings[self.tagID]
                self.internal_mapping = input_to_dict(m.read_text())
        super().__init__(mode)

    @staticmethod
    def expected_input_format():
        return TiffParser.expected_input

    def parse(self, file_path, mapping):
        input_md = self._read_input_file(file_path, self.tagID)
        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None

        if not mapping and not self.internal_mapping:
            logging.error("No mapping provided for image parsing. Aborting")
            raise MappingAbortionError("Image parsing failed.")
        mapping_dict = mapping if mapping else self.internal_mapping
        image_md = map_a_dict(input_md, mapping_dict)

        Preprocessor.normalize_all_units(image_md)
        Preprocessor.normalize_all_datetimes(image_md)

        if self.mode == ParserMode.TOMO:
            image_from_md = self._create_tomo_image(image_md, file_path)
        else:
            image_from_md = ImageMD(image_metadata=SEM_Image(**image_md), filePath="")

        return image_from_md

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
        """
        Reading input may be done with a predefined tag or without. In the latter case we try to extract from all tags and use the joint dictionary for mapping.
        :param file_path: image file path
        :param tagID: tag to extract from, may be None
        :return: data from extracted tag(s) as dict
        """
        image = Image.open(file_path)
        exif = image.getexif()
        image.close()
        if exif is None:
            logging.warning("No EXIF data found in image {}".format(file_path))
            return None

        if tagID:
            try:
                md_list = [value for key, value in exif.items() if key == int(tagID)]
            except IndexError:
                logging.warning("Tag ID defined but no corresponding data extractable: tag {} in {}".format(tagID, file_path))
                return None
        else:
            md_list = [value for key, value in exif.items()]

        output_dict = {}
        for md in md_list:
            try:
                additional_input = input_to_dict(md)
                if not additional_input:
                    logging.debug("Unable to extract metadata as dictionary for {}".format(md))
                output_dict.update(input_to_dict(md))
            except Exception as e:
                logging.debug("Unable to extract metadata as dictionary for {}".format(md))
                pass

        return output_dict
