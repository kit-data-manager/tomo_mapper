# Function to get value from nested dictionary using dotted path
import logging
import typing
from sys import exit

import pandas as pd
from importlib import resources
from jsonpath_ng.ext.parser import ExtentedJsonPathParser

parser = ExtentedJsonPathParser()

# Function to create unified output dict based on the provided JSON mapping
def create_unified_dict(mapping, input_dict):
    output_dict = {}

    for k, v in mapping.items():

        k = ".".join(["'" + x + "'" if not ("[" in x or "`" in x) else x for x in k.split('.')] ) #make sure that unexpected tokens in input can be handled properly (such as #)
        exprIN = parser.parse(k)
        exprOUT = parser.parse(v)

        values = [m.value for m in exprIN.find(input_dict)]
        if not values:
            logging.warning("Mapping defined but no corresponding value found in input dict: {}".format(k))
            continue

        if not "*" in v: #as long as the output path in the map is not a list, we expect that we can map the input to one value
            try:
                if not all([isinstance(x, typing.Hashable) for x in values]):
                    logging.warning("Found multiple complex values in input dict, but output target is not a list. Only the first value will be used, no check for equivalence.")
                else:
                    assert len(set(values)) == 1
            except AssertionError:
                logging.error("Found multiple values in input dict, but output target is not a list. Aborting. Input path: {}, values: {}".format(k, values))
                exit(1)
            if values[0]:
                exprOUT.update_or_create(output_dict, values[0])
            else:
                logging.warning("Found a value equivalent to None. path: {}, value: {}".format(k, values[0]))
        else: #split output in accordance to list of input values
            for i, value in enumerate(values):
                if value:
                    indexed_expr = parser.parse(v.replace('*', str(i)))
                    indexed_expr.update_or_create(output_dict, value)
                else:
                    logging.warning(
                        "Found a value equivalent to None. path: {}, value: {}".format(k, value))
    return output_dict

def _read_mapTable_hardcoded(col1, col2, fname = "image_map.csv"):
    """
    #TODO: prettify this. This is a proof-of-concept shortcut implementation.
    :param col1: name of input column in csv
    :param col2: name of output column in csv
    :return: dict with key-value pairs of input and output column values
    """

    with resources.as_file(resources.files("src.resources.maps") / fname) as dfresource:
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