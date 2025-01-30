# Function to get value from nested dictionary using dotted path
import json
import pandas as pd

from src.model.SEM_Image import SEM_FIB_Image
from src.model.TOMO_Image import TOMO_Image

from importlib import resources

def get_value_from_nested_dict(nested_dict, dotted_path):
    keys = dotted_path.split('.')
    value = nested_dict
    for key in keys:
        if type(value) is dict:
            try:
                value = value[key]
            except:
                value = value[key.capitalize()]
    return value


# Function to create nested dictionary from dotted path
def create_nested_dict(dotted_path, value):
    keys = dotted_path.split('.')
    nested_dict = value
    for key in reversed(keys):
        nested_dict = {key: nested_dict}
    return nested_dict


# Function to merge two dictionaries
def merge_dicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]

# Function to create unified output dict based on the provided JSON mapping
def create_unified_dict(mapping, input_dict):
    output_dict = {}

    for input_key, output_key in mapping.items():
        try:
            value = get_value_from_nested_dict(input_dict, input_key)
            nested_dict = create_nested_dict(output_key, value)
            merge_dicts(output_dict, nested_dict)
        except KeyError:
            pass

    return output_dict

def _read_mapTable_hardcoded(col1, col2):
    """
    #TODO: prettify this
    :param col1:
    :param col2:
    :return:
    """
    with resources.path("src.resources.maps", "image_map.csv") as dfresource:
        df = pd.read_csv(dfresource)

        dropped_df = df[[col1, col2]].dropna()
        return list(zip(dropped_df[col1], dropped_df[col2]))

def map_a_dict(input_dict, maptable_cols):
    """
    use this function to convert a dict of tiff extracted metadata in original format to the output format for the schemas
    #TODO: prettify this
    :param input_dict:
    :param maptable_cols: (col1, col2) tuple to describe which mapping to use (in a fixed map at the moment). Possible values "Zeiss_TOMO", "TF" for col1, "SEM_Schema", "TOMO_Schema" for col2
    :return:
    """
    col1, col2 = maptable_cols

    map_info = _read_mapTable_hardcoded(col1, col2)
    mapping_dict = dict(map_info)

    return create_unified_dict(mapping_dict, input_dict)