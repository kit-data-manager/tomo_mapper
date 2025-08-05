import enum
from abc import ABC, abstractmethod

from tomo_mapper.model.ImageMD import ImageMD

class ParserMode(enum.Enum):
    TOMO = "tomo",
    SEM = "sem"

class ImageParser(ABC):

    def __init__(self, mode):
        self.mode = mode

    @staticmethod
    @abstractmethod
    def expected_input_format() -> str:
        """
        Return expected input format of parser. This can be used to determine if a parser is applicable to the given input.
        :return: mimetype string for input format (such as image/tiff or text/plain)
        """
        pass

    @abstractmethod
    def parse(self, file_path, mapping) -> tuple[ImageMD, str]:
        pass

    @abstractmethod
    def _create_tomo_image(self, image_metadata, file_path) -> ImageMD:
        pass

