from abc import ABC, abstractmethod

from src.model.SchemaConcepts.TOMO_Image import TOMO_Image


class ImageParser(ABC):

    @staticmethod
    @abstractmethod
    def expected_input_format():
        pass

    @abstractmethod
    def parse(self, file_path) -> TOMO_Image:
        pass

    @abstractmethod
    def _create_image(self, image_metadata) -> TOMO_Image:
        pass