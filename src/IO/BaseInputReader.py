from abc import ABC, abstractmethod
import shutil
import os
import logging

from src.IO.MappingAbortionError import MappingAbortionError

class BaseInputReader(ABC):
    """
    Abstract base class for InputReader implementation.
    """

    temp_dir_path: str = None

    def __init__(self, map_path, input_path):
        self.map_path = map_path
        self.input_path = input_path
        self._validate_input_path()

    def _validate_input_path(self):
        if not os.path.exists(self.input_path):
            logging.error("Input file {} does not exist. Aborting".format(self.input_path))
            raise MappingAbortionError("Input file loading failed.")

    @abstractmethod
    def retrieve_image_info(self):
        pass

    def clean_up(self):
        if self.temp_dir_path and os.path.exists(self.temp_dir_path):
            shutil.rmtree(self.temp_dir_path)
            logging.debug("Temp folder deletion: {} - {}".format(self.temp_dir_path, os.path.exists(self.temp_dir_path)))
        else:
            logging.debug("No temp folder used, nothing to clean up.")
