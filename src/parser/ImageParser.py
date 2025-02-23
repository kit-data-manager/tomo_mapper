import enum
from abc import ABC, abstractmethod

from src.model.ImageMD import ImageMD

class ParserMode(enum.Enum):
    TOMO = "tomo",
    SEM = "sem"

class ImageParser(ABC):

    def __init__(self, mode):
        self.mode = mode

    @staticmethod
    @abstractmethod
    def expected_input_format():
        pass

    @abstractmethod
    def parse(self, file_path, mapping) -> tuple[ImageMD, str]:
        pass

    @abstractmethod
    def _create_tomo_image(self, image_metadata, file_path) -> ImageMD:
        pass

