import importlib
from enum import Enum

from src.Preprocessor import Preprocessor


class TestPreprocessor:

    def test_unit_replacement(self):
        input_dict = {
            "some": {
                "nested": {
                    "units": [
                        {"unit": "degr"},
                        {"unit": "°"},
                        {"unit": "kV"},
                        {"unit": "μm"}
                    ]
                }
            }
        }

        units_module = importlib.import_module('src.model.SchemaConcepts.codegen.SchemaClasses_TOMO')

        # Collect all unit values that are allowed
        all_units = set()

        i = 1
        while True:
            class_name = f'Unit{i}'
            unit_class = getattr(units_module, class_name, None)
            if unit_class and issubclass(unit_class, Enum):
                for unit in unit_class:
                    all_units.add(unit.value)
                i += 1
            else:
                break

        Preprocessor.normalize_all_units(input_dict)
        normalized_units = [x["unit"] for x in input_dict['some']['nested']['units']]
        assert not [x for x in normalized_units if x not in all_units]