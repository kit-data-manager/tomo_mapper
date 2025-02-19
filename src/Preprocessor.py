from jsonpath_ng.parser import JsonPathParser


class Preprocessor:

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
        :return:
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