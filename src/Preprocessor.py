import logging
from datetime import datetime, timezone
from typing import Union

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
        'um': 'µm',
        'Secs': 's',
        'Mins': 'min',
        'μs': 'us'
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
        unit_field_names = ["unit", "coordinatesUnit"]
        for field_name in unit_field_names:
            unit_fields = Preprocessor.parser.parse("$.." + field_name)
            unit_matches = [m for m in unit_fields.find(input_dict)]
            for m in unit_matches:
                if type(m.value) != str: continue #TODO: should this be possible?
                original_value = m.value
                if not Preprocessor.unit_normalization.get(original_value): continue

                normalized_value = Preprocessor.unit_normalization[original_value]
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)

    @staticmethod
    def normalize_datetime(input_value) -> Union[str, dict]:
        if type(input_value) == dict:
            curr_date = input_value.get("Date")
            curr_time = input_value.get("Time")
            if not curr_date and not curr_time: return input_value
            if not curr_date and curr_time: # Not possible to handle only Time
                logging.warning("Encountered complex date field, but cannot interpret it")
                return input_value
            if curr_date and not curr_time: # Handle only Date
                curr_time = "00:00:00"
                logging.info("Input with date information but no time information found. Setting time to 00:00:00")
            input_value = curr_date + " " + curr_time
        output_value = parse_datetime(input_value)
        if type(output_value) == datetime:
            if output_value.tzinfo:
                output_value = output_value.astimezone(timezone.utc) # datetime has timezone info, convert it to UTC
            else:
                output_value = output_value.replace(tzinfo=timezone.utc) # No timezone, assume it's already in UTC
            return output_value.isoformat().replace("+00:00", "Z")
        return input_value

    @staticmethod
    def normalize_all_datetimes(input_dict):
        """
        Inplace normalization of all values in datetime fields
        :param input_dict: dictionary to replace in
        :return: 
        """
        fields_for_normalization = ["creationTime", "startTime", "endTime"] #we could do it more generically but may want to limit it to specific fields

        for f in fields_for_normalization:
            date_fields = Preprocessor.parser.parse("$.." + f)
            date_matches = [m for m in date_fields.find(input_dict)]
            for m in date_matches:
                original_value = m.value
                normalized_value = Preprocessor.normalize_datetime(original_value)
                if normalized_value != original_value:
                    m.full_path.update(input_dict, normalized_value)