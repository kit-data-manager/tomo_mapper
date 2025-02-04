import argparse
import logging
import os

from src.InputReader import InputReader

#make log level configurable from ENV, defaults to info level
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'DEBUG').upper()
)

def get_args():
    parser = argparse.ArgumentParser(description='Extracting of SEM FIB Tomography metadata to unified json format')
    parser.add_argument('-i','--input', help='Input zip file as file path', required=True)
    parser.add_argument('-m', '--map', help='Map file as path or remote URI', required=True)
    parser.add_argument('-o', '--output', help='Path to output json file', required=True)
    return vars(parser.parse_args())

def run_cli():
    args = get_args()
    INPUT_SOURCE = args.get('input')
    MAP_SOURCE = args.get('map')
    OUTPUT_PATH = args.get('output')

    logging.info(f'This is a dummy implementation for a command line interface.')
    reader = InputReader(INPUT_SOURCE, MAP_SOURCE)
    tmpdir = reader.temp_dir_path

    acs = reader.retrieve_acquisition_info()
    print(len(acs))
    print(acs[0])

    imgs = reader.retrieve_image_info()
    print(len(imgs))
    print(imgs[0])

    reader.clean_up()

    logging.info("Temp folder deletion: {} - {}".format(tmpdir, os.path.exists(tmpdir)))

if __name__ == '__main__':
    run_cli()