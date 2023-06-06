from imageMapper import readFile, formatMetadata, extractImageMappings, extractImageData, headerMapping, writeMetadataToJson
from acquisitionMapper import xml_to_dict, extract_values, traverse_dict
import json

def extract_metadata_addresses_dataset(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the "acquisition" information
    acquisition_data = data.get('dataset_schema', {})

    # Store key-value pairs starting with "EMProject"
    EM_metadata = {}
    Image_metadata = {}
    for key, value in acquisition_data.items():
        if value.startswith('EMProject'):
            EM_metadata[key] = value
        elif value.startswith('Images'):
            Image_metadata[key] = value

    return EM_metadata, Image_metadata

if __name__ == "__main__":

    emxml_file = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2/EMproject.emxml'
    json_file = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/schemas/sem_fib_nested_schema_map.json'
    imgFile = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2/Images/SEM Image/SEM Image - SliceImage - 001.tif'
    output_path = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/results/datasetMetadata.json'
    dataset_num = 1

    xmlMetadata, imgMetadata = extract_metadata_addresses(json_file)
    emData = xml_to_dict(emxml_file)
    mappedEMMetadata = extract_values(xmlMetadata, emData, dataset_num)
    imageData = readFile(imgFile)
    formattedMetadata = formatMetadata(imageData)
    imageMetadata = extractImageData(formattedMetadata, imgMetadata)
    mappedImgMetadata = headerMapping(imageMetadata, imgMetadata)

    datasetMetadata = {**mappedEMMetadata, **mappedImgMetadata}

    writeMetadataToJson(datasetMetadata, output_path)
    print(f'Successfully processed. Results are in {output_path}')