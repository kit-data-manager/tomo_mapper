import os
import json
import time
from PIL import Image
from PIL.ExifTags import TAGS


def readFile(file_path):
    image = Image.open(file_path)
    exif = image.getexif()
    if exif is None:
        return None
    
    exif_data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 34682:
            metadata = value
    return metadata

def formatMetadata(metadata):
    metadata_dict = {}
    current_header = None

    lines = metadata.strip().split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('[') and line.endswith(']'):
            current_header = line[1:-1]
        elif '=' in line:
            key, value = line.split('=', 1)
            split_key = key.split('.')
            last_variable = split_key[-1]
            formatted_last_variable = last_variable.lower()
            split_key[-1] = formatted_last_variable
            formatted_key = f'Images.SEM Image.SliceImage.{current_header}.' + '.'.join(split_key)
            value = value.strip()
            metadata_dict[formatted_key] = value

    return metadata_dict

def extractImageMappings(json_file):
    with open(json_file) as f:
        mappings = json.load(f)
    image_mappings = mappings.get('image', {})
    return image_mappings

def extractImageData(image_data, image_mappings):
    extracted_data = {}

    for key, value in image_data.items():
        if key in image_mappings.values():
            extracted_data[key] = value

    return extracted_data

def headerMapping(image_metadata, image_mappings):
    mapped_metadata = {}

    for desired_var, current_var in image_mappings.items():
        if current_var in image_metadata:
            mapped_metadata[desired_var] = image_metadata[current_var]

    return mapped_metadata

def writeMetadataToJson(mapped_metadata, output_file):
    metadata_dict = {}

    for key, value in mapped_metadata.items():
        levels = key.split('.')
        current_dict = metadata_dict

        for level in levels[:-1]:
            current_dict = current_dict.setdefault(level, {})

        current_dict[levels[-1]] = value

    with open(output_file, 'w') as f:
        json.dump(metadata_dict, f, indent=4)

def processImageFolder(input_folder, output_folder, map_file):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]
    total_images = len(image_files)
    processed_images = 0

    start_time = time.time()

    image_mappings = extractImageMappings(map_file)

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
#         print(image_path)
        image_data = readFile(image_path)
        formatted_metadata = formatMetadata(image_data)
        image_metadata = extractImageData(formatted_metadata, image_mappings)
        mapped_metadata = headerMapping(image_metadata, image_mappings)
        output_filename = os.path.splitext(image_file)[0] + '.json'
        output_path = os.path.join(output_folder, output_filename)
        writeMetadataToJson(mapped_metadata, output_path)
        
        processed_images += 1
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Processed {processed_images}/{total_images} images in {elapsed_time:.2f} seconds")


# Execute
if __name__ == "__main__":
    input_folder = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2/Images/SEM Image'
    output_folder = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/py_script_results'
    map_file = "/Users/elias/Desktop/PP13_Mapping/pp13-mapper/schemas/sem_fib_nested_schema_map.json"

    processImageFolder(input_folder, output_folder, map_file)