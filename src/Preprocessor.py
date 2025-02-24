from datetime import datetime

from jsonpath_ng.parser import JsonPathParser

from src.model.SchemaConcepts.Schema_Concept import parse_datetime


class Preprocessor:
    """
    Use / adapt / extend for final preprocessing steps before converting a dictionary into the according pydantic class instances
    """

    parser = JsonPathParser()

    unit_normalization = {
        'deg': 'degree',
        'degr': 'degree',
        '°': 'degree',
        'μm': 'um',
    }

    @staticmethod
    def normalize_unit(input_value) -> str:
        if input_value in Preprocessor.unit_normalization.keys():
            return Preprocessor.unit_normalization[input_value]
        return input_value

    @staticmethod
    def normalize_all_units(input_dict):
        """
        Inplace normalization of all values in fields "unit"
        :param input_dict: dictionary to replace units in
        :return: None
        """
        unit_fields = Preprocessor.parser.parse("$..unit")
        unit_matches = [m for m in unit_fields.find(input_dict)]
        for m in unit_matches:
            if type(m.value) != str: continue #TODO: should this be possible?
            original_value = m.value
            if not Preprocessor.unit_normalization.get(original_value): continue

            normalized_value = Preprocessor.unit_normalization[original_value]
            if normalized_value != original_value:
                m.full_path.update(input_dict, normalized_value)

    @staticmethod
    def normalize_datetime(input_value) -> str:
        output_value = parse_datetime(input_value)
        if type(output_value) == datetime:
            return output_value.isoformat()
        return input_value

    @staticmethod
    def normalize_all_datetimes(input_dict):
        fields_for_normalization = ["creationTime", "startTime", "endTime"] #we could do it more generically but may want to limit it to specific fields

        for f in fields_for_normalization:
            date_fields = Preprocessor.parser.parse("$.." + f)
            date_matches = [m for m in date_fields.find(input_dict)]
            for m in date_matches:
                if type(m.value) != str: continue #TODO: should this be possible?
                original_value = m.value
                normalized_value = Preprocessor.normalize_datetime(original_value)
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)

