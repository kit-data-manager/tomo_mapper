from imageMapper import readFile, formatMetadata, extractImageMappings, extractImageData, headerMapping, writeMetadataToJson
from acquisitionMapper import xml_to_dict, extract_values, traverse_dict
import json

mapFile = '/path/to/mapfile.json'
imgDir  = 'path/to/dir'
xmlFile = 'path/to/xmlfile.emxml'