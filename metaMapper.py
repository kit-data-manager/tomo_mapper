from acquisitionMapper import extract_metadata_addresses, xml_to_dict, extract_values
from imageMapper import readFile, formatMetadata, extractImageMappings, extractImageData, headerMapping
from datasetMapper import extract_metadata_addresses_dataset
import os
import json
import zipfile
import tempfile
import shutil
import time
import sys

def extract_zip_file(zip_file_path):
    temp_dir = tempfile.mkdtemp()

    start_time = time.time()  # Start time
    print(zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())

        for index, file_name in enumerate(zip_ref.namelist(), start=1):
            file_path = os.path.join(temp_dir, file_name)
            zip_ref.extract(file_name, temp_dir)
            print(f"Extracting file {index}/{total_files}: {file_name}")

    main_directory = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    end_time = time.time()  # End time
    total_time = end_time - start_time

    print(f"Total time taken to process: {total_time:.2f} seconds")
    return main_directory

# inputZip = '/Users/elias/Desktop/NFDI Tomographiedaten/20200818_AlSi13 XRM tomo2.zip'
# output_path = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/result_jsons'
# mapFile = '/Users/elias/Desktop/PP13_Mapping/pp13-mapper/schemas/new_sem_fib_nested_schema_map.json'

mapFile    = sys.argv[1]
inputZip   = sys.argv[2]
outputFile = sys.argv[3]

mainDir = extract_zip_file(inputZip)
imgFile = os.path.join(mainDir, 'Images/SEM Image 2/SEM Image 2 - SliceImage - 012.tif')
imgDirectory = os.path.join(mainDir, 'Images')
xmlFile = os.path.join(mainDir, 'EMproject.emxml')

xmlMap, imgMap = extract_metadata_addresses(mapFile)
xmlMetadata = xml_to_dict(xmlFile)

acqXmlMetadata = extract_values(xmlMap, xmlMetadata)

# Read an image for acquisition metadata
imgMetadata = readFile(imgFile)
formattedImgMetadata = formatMetadata(imgMetadata)
extractedImgMetadata = extractImageData(formattedImgMetadata, imgMap)
acqImgMetadata = headerMapping(extractedImgMetadata, imgMap)

# The metadata for the acquisition is then the combined metadata from the xml file and an image
acqMetadata = {**acqXmlMetadata, **acqImgMetadata}


# Read and format dataset metadata
datasetXmlMap, datasetImgMap = extract_metadata_addresses_dataset(mapFile)
datasets = xmlMetadata['EMProject']['Datasets']['Dataset']
datasetNames = [d['Name'] for d in datasets]
def processDatasets(datasetNum, imageDirectory):
    # Extract xml data for this dataset
    mappedEMMetadata = extract_values(datasetXmlMap, xmlMetadata, datasetNum)
    
    # Read data from image in proper folder
    datasetName = datasetNames[datasetNum - 1]
    for root, dirs, files in os.walk(imageDirectory):
        if os.path.basename(root) == datasetName:
            for file in files:
                if file.endswith('.tif'):
                    imgPath = os.path.join(root, file)
                    break
            break
    imageData = readFile(imgPath)
    formattedMetadata = formatMetadata(imageData)
    imageMetadata = extractImageData(formattedMetadata, datasetImgMap)
    mappedImgMetadata = headerMapping(imageMetadata, datasetImgMap)
    
    return {**mappedEMMetadata, **mappedImgMetadata}

datasetMetadata = []
for i, dataset in enumerate(datasetNames[:2]):
    print(i, dataset)
    datasetMetadata.append(processDatasets(i+1, imgDirectory))


# Read and format image metadata

imgMappings = extractImageMappings(mapFile)
def processImage(imgPath):
    # read image file
    rawImgMetadata = readFile(imgPath)
    formattedMetadata = formatMetadata(rawImgMetadata)
    imageMetadata = extractImageData(formattedMetadata, imgMappings)
    mappedImgMetadata = headerMapping(imageMetadata, imgMappings)
    
    return mappedImgMetadata


def processDatasets(datasetNum, imageDirectory):
    # Extract xml data for this dataset
    mappedEMMetadata = extract_values(datasetXmlMap, xmlMetadata, datasetNum)
    
    # Read data from image in proper folder
    datasetName = datasetNames[datasetNum - 1]
    for root, dirs, files in os.walk(imageDirectory):
        if os.path.basename(root) == datasetName:
            for file in files:
                if file.endswith('.tif'):
                    imgPath = os.path.join(root, file)
                    break
            break
    imageData = readFile(imgPath)
    formattedMetadata = formatMetadata(imageData)
    imageMetadata = extractImageData(formattedMetadata, datasetImgMap)
    mappedImgMetadata = headerMapping(imageMetadata, datasetImgMap)
    
    # Repeat to produce list of image metadata dictionaries
    imageMetadataList = []
    for root, dirs, files in os.walk(imageDirectory):
        if os.path.basename(root) == datasetName:
            for file in files:
                if file.endswith('.tif'):
                    imgPath = os.path.join(root, file)
                    imageMetadataList.append(processImage(imgPath))
    
    
    return {**mappedEMMetadata, **mappedImgMetadata}, imageMetadataList

datasetMetadata = []
imageMetadata   = []
for i, dataset in enumerate(datasetNames[:2]):
    print(i, dataset)
    datasetMetadataDict, ImageMetadataDict =  processDatasets(i+1, imgDirectory)
    datasetMetadata.append(datasetMetadataDict)
    imageMetadata.append(ImageMetadataDict)

def combineMetadata(acquisition_metadata, dataset_metadata, image_metadata):    
    metadata = {}
    # Combine acquisition metadata
    for key, value in acquisition_metadata.items():
        nested_keys = key.split('.')
        current_dict = metadata

        for nested_key in nested_keys[:-1]:
            if nested_key not in current_dict:
                current_dict[nested_key] = {}
            current_dict = current_dict[nested_key]

        current_dict[nested_keys[-1]] = value

    # Combine dataset metadata
    metadata['acquisition']['dataset'] = []
    for dataset in dataset_metadata:
        dataset_dict = {}
        for key, value in dataset.items():
            nested_keys = key.split('.')
            nested_keys.remove('acquisition')
            nested_keys.remove('dataset')
            current_dict = dataset_dict

            for nested_key in nested_keys[:-1]:
                if nested_key not in current_dict:
                    current_dict[nested_key] = {}
                current_dict = current_dict[nested_key]

            current_dict[nested_keys[-1]] = value

        metadata['acquisition']['dataset'].append(dataset_dict)

    # Combine image metadata
    for i, images in enumerate(image_metadata):
        metadata['acquisition']['dataset'][i]['images'] = []
        for image in images:
            image_dict = {}
            for key, value in image.items():
                nested_keys = key.split('.')
                nested_keys.remove('acquisition')
                nested_keys.remove('dataset')
                nested_keys.remove('images')
                current_dict = image_dict

                for nested_key in nested_keys[:-1]:
                    if nested_key not in current_dict:
                        current_dict[nested_key] = {}
                    current_dict = current_dict[nested_key]

                current_dict[nested_keys[-1]] = value

            metadata['acquisition']['dataset'][i]['images'].append(image_dict)
    return metadata

def save_metadata_as_json(metadata, save_path):
    filename = os.path.join(save_path, "combinedSO_script.json")
    with open(filename, 'w') as file:
        json.dump(metadata, file, indent=4)
    print(f"Metadata saved as {filename}")

combinedMetadata = combineMetadata(acqMetadata, datasetMetadata, imageMetadata)
save_metadata_as_json(combinedMetadata, outputFile)

# Execute
# if __name__ == "__main__":