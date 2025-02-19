import logging
import re
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from src.model.ImageMD import ImageMD
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.parser.ImageParser import ImageParser
from src.parser.mapping_util import map_a_dict
from src.util import input_to_dict


#TODO: would this have any benefit from replacing with tifffile lib?

class TiffParser(ImageParser):

    def __init__(self, tagID):
        self.tagID = tagID
        self.mapping_tuple = (tagID, "TOMO_Schema")

    @staticmethod
    def expected_input_format():
        return "tiff"

    def parse(self, file_path) -> tuple[ImageMD, str]:
        input_md = self._read_input_file(file_path, self.tagID)
        input_md = self._preprocess_image_metadata(input_md)
        if not input_md:
            logging.warning("No metadata extractable from {}".format(file_path))
            return None, None

        image_md = map_a_dict(input_md, self.mapping_tuple, "image")

        image_from_md = self._create_image(image_md, file_path)

        return image_from_md, image_md

    def _create_image(self, image_md, fp) -> ImageMD:

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
            logging.error("No matching tag found in exif data for {} on {}".format(tagID, file_path))

    def _preprocess_image_metadata(self, image_md_format):
        """
        Sanitize and xml image metadata.
        """

        # Ensure the input 'image_md_format' is always a dictionary
        if image_md_format is None:
            logging.warning("Received None as image metadata, initializing an empty dictionary.")
            image_md_format = {}
            return image_md_format

        #self.save_the_file(image_md_format, "./image_md_original") #----for debugging purpose

        # Ensure dataset_metadata structure exists before accessing it
        Fibics = image_md_format.setdefault("Fibics", {})
        ScanInfo = Fibics.setdefault("ScanInfo", {})
        DetectorInfo = Fibics.setdefault("DetectorInfo", {})
        Stage = Fibics.setdefault("Stage", {})
        Scan = Fibics.setdefault("Scan", {})


        # Process Fibics.Scan.ScanRot (Convert "deg" -> "degree")
        ScanRot = Scan.setdefault("ScanRot", {})
        if ScanRot.get("@units") == "deg":
            ScanRot["@units"] = "degree"

        # Process Fibics.Stage.Rot (Convert "deg" -> "degree")
        Rot = Stage.setdefault("Rot", {})
        if Rot.get("@units") == "deg":
            Rot["@units"] = "degree"

        # Process numeric value from Fibics.ScanInfo.item : tiltCorrectionAngle.value
        item = ScanInfo.setdefault("item", {})
        if isinstance(item.get("#text"), str):
            match = re.search(r"-?\d+(\.\d+)?", item["#text"])
            if match:
                item["#text"] = float(match.group())
                #item["@units"] = "degree"

        # Process DetectorInfo.item[*] (Extract values for 'signal' and 'setting')
        item = DetectorInfo.setdefault("item", [])
        cleaned_detector_items = []
        for item in DetectorInfo["item"]:
            if "@name" in item and "#text" in item:
                cleaned_item = {
                    "@name": item["@name"],
                    "#text": item["#text"].strip()
                }
                
                cleaned_value = cleaned_item["#text"].replace("=", "").replace("kV", "").strip()
                match = re.search(r"-?\d+(\.\d+)?", cleaned_value)

                if match:
                    cleaned_item["#text"] = float(match.group())  # Convert to float
                cleaned_detector_items.append(cleaned_item)

        # Assign cleaned detector info back to Fibics
        DetectorInfo["item"] = cleaned_detector_items

        #self.save_the_file(image_md_format, "./image_md_processed") #----for debugging purpose
        return image_md_format
