from abc import ABC, abstractmethod

from src.model.ImageMD import ImageMD

class ImageParser(ABC):

    @staticmethod
    @abstractmethod
    def expected_input_format():
        pass

    @abstractmethod
    def parse(self, file_path) -> tuple[ImageMD, str]:
        pass

    @abstractmethod
    def _create_image(self, image_metadata, file_path) -> ImageMD:
        pass