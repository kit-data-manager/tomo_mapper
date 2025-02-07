from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import ConfigDict, field_validator

def parse_datetime(value: str):
    try:
        return datetime.strptime(value, '%d.%m.%Y %H:%M:%S') #specific handling of expected date format that usual validator cannot handle
    except ValueError:
        return value #not a German date - lets hope that the normal validator can handle it

class Schema_Concept(ABC):

    __pydantic_config__ = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,
    )