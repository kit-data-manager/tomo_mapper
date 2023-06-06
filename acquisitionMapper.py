import json
from imageMapper import readFile, formatMetadata, extractImageMappings, extractImageData, headerMapping, writeMetadataToJson

def extract_metadata_addresses(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the "acquisition" information
    acquisition_data = data.get('acquisition_main_schema', {})

    # Store key-value pairs starting with "EMProject"
    EM_metadata = {}
    Image_metadata = {}
    for key, value in acquisition_data.items():
        if value.startswith('EMProject'):
            EM_metadata[key] = value
        elif value.startswith('Images'):
            Image_metadata[key] = value

    return EM_metadata, Image_metadata

import xml.etree.ElementTree as ET

def xml_to_dict(file_path):
    def parse_element(element):
        result = {}
        if len(element) == 0:
            return element.text
        for child in element:
            child_data = parse_element(child)
            if '}' in child.tag:
                child_tag = child.tag.split('}', 1)[1]  # Remove the namespace
            else:
                child_tag = child.tag
            if child_tag in result:
                if type(result[child_tag]) is list:
                    result[child_tag].append(child_data)
                else:
                    result[child_tag] = [result[child_tag], child_data]
            else:
                result[child_tag] = child_data
        return result

    tree = ET.parse(file_path)
    root = tree.getroot()
    root_tag = root.tag
    if '}' in root_tag:
        root_tag = root_tag.split('}', 1)[1]  # Remove the namespace from the root tag
    return {root_tag: parse_element(root)}

def traverse_dict(data, path):
    keys = path.split('.')
    result = data
    try:
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return None
    
def extract_values(addresses, data, dataset_num = 1):
    result = {}
    for key, address in addresses.items():
        levels = address.split('.')
        current_data = data
        for level in levels:
            # emxml contains multiple instances of "Dataset", so it returns a list when asked. We need to tell it
            # which dataset we actually want. 1 is SEM Image, 2 is SEM Image 2, and 3 is the one we're not
            # interested in. We subtract 1 because indexing begins at zero
            # Still needed: check this against image folder name
            if level == 'Dataset':
                current_data = current_data[level][dataset_num - 1]
            else:
                current_data = current_data[level]
        result[key] = current_data
    return result


if __name__ == "__main__":
    # Define relevant files
    emxml_file = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2/EMproject.emxml'
    json_file = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/schemas/sem_fib_nested_schema_map.json'
    imgFile = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2/Images/SEM Image/SEM Image - SliceImage - 001.tif'
    output_path = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/results/acquisitionMetadata.json'
    dataset_num = 1 # 1 or 2

    emMetadata, imgMetadata = extract_metadata_addresses(json_file)
    emData = xml_to_dict(emxml_file)
    mappedEMMetadata = extract_values(emMetadata, emData, dataset_num)
    image_data = readFile(imgFile)
    formatted_metadata = formatMetadata(image_data)
    image_metadata = extractImageData(formatted_metadata, imgMetadata)
    mappedImgMetadata = headerMapping(image_metadata, imgMetadata)

    # Merge the two metadata dictionaries
    acquisitionMetadata = {**mappedEMMetadata, **mappedImgMetadata}

    writeMetadataToJson(acquisitionMetadata, output_path)
    print(f'Successfully processed. Results are in {output_path}')