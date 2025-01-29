from abc import ABC, abstractmethod


class Schema_Concept(ABC):

    @abstractmethod
    def to_schema_dict(self):
        pass