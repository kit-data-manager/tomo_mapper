import os.path
from typing import Optional


class MappingConfig:

    working_dir = None

    @classmethod
    def set_working_dir(cls, working_dir):
        cls.working_dir = os.path.normpath(working_dir)

    @classmethod
    def get_working_dir(cls) -> Optional[str]:
        return cls.working_dir
