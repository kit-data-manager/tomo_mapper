# Function to get value from nested dictionary using dotted path
import logging
import re
import typing
from sys import exit

import pandas as pd
from importlib import resources
from jsonpath_ng.ext.parser import ExtentedJsonPathParser

parser = ExtentedJsonPathParser()

def escape_pathelements(dotted_path):
    funct = re.search("(`.+`)", dotted_path)
    if funct:
        dotted_path = dotted_path.replace(funct.group(0), "FUNCTIONPLACEHOLDER")

    pathElements = dotted_path.split(".")
    escaped_elements = []
    for pe in pathElements:
        if not pe: continue
        if "[" in pe:
            to_escape, to_keep = pe.split("[", 1)
            escaped = "'" + to_escape + "'"
            pe = escaped + "[" + to_keep
        else:
            pe = "'" + pe + "'"
        if pe == "'FUNCTIONPLACEHOLDER'":
            pe = funct.group(0)
        escaped_elements.append(pe)
    return ".".join(escaped_elements)


# Function to create unified output dict based on the provided JSON mapping
def create_unified_dict(mapping, input_dict):
    output_dict = {}

    for k, v in mapping.items():
        k = escape_pathelements(k)
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

def get_internal_mapping(maptable_cols, contentType):
    assert contentType in ["image", "acquisition"]

    col1, col2 = maptable_cols

    map_info = _read_mapTable_hardcoded(col1, col2, contentType+"_map.csv")
    mapping_dict = dict(map_info)
    return mapping_dict

def map_a_dict(input_dict, mapping_dict):
    return create_unified_dict(mapping_dict, input_dict)