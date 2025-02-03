# Function to get value from nested dictionary using dotted path
import json
from collections import defaultdict

import pandas as pd
from importlib import resources
from jsonpath_ng import parse

# Function to create unified output dict based on the provided JSON mapping
def create_unified_dict(mapping, input_dict):
    output_dict = {}

    for k, v in mapping.items():

        exprIN = parse(k)
        exprOUT = parse(v)

        values = [m.value for m in exprIN.find(input_dict)]
        if not values: continue

        if not "*" in v: #as long as the output path in the map is not a list, we expect that we can map the input to one value
            try:
                assert len(set(values)) == 1
            except AssertionError:
                print(values)
                exit(1)
            exprOUT.update_or_create(output_dict, values[0])
        else: #split output in accordance to list of input values
            for i, value in enumerate(values):
                indexed_expr = parse(v.replace('*', str(i)))
                indexed_expr.update_or_create(output_dict, value)
    return output_dict

def _read_mapTable_hardcoded(col1, col2, fname = "image_map.csv"):
    """
    #TODO: prettify this. This is a proof-of-concept shortcut implementation.
    :param col1: name of input column in csv
    :param col2: name of output column in csv
    :return: dict with key-value pairs of input and output column values
    """

    fname = fname

    with resources.path("src.resources.maps", fname) as dfresource:
        df = pd.read_csv(dfresource)

        dropped_df = df[[col1, col2]].dropna() #ignore rows with either NaN in input or output col (may occur on mapping csv with more than 2 columns)
        return list(zip(dropped_df[col1], dropped_df[col2]))

def map_a_dict(input_dict, maptable_cols, contentType):
    """
    use this function to convert a dict of tiff extracted metadata in original format to the output format for the schemas
    #TODO: prettify this. This is a proof-of-concept shortcut implementation.
    :param input_dict:
    :param maptable_cols: (col1, col2) tuple to describe which mapping to use (in a fixed map at the moment). Possible values "Zeiss_TOMO", "TF" for col1, "SEM_Schema", "TOMO_Schema" for col2
    :return:
    """
    assert contentType in ["image", "acquisition"]

    col1, col2 = maptable_cols

    map_info = _read_mapTable_hardcoded(col1, col2, contentType+"_map.csv")
    mapping_dict = dict(map_info)

    return create_unified_dict(mapping_dict, input_dict)