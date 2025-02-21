import argparse
import logging
import os
from pprint import pprint

from src.InputReader import InputReader
from src.OutputWriter import OutputWriter

#make log level configurable from ENV, defaults to info level
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
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
    reader = InputReader(MAP_SOURCE, INPUT_SOURCE)
    tmpdir = reader.temp_dir_path

    setup_infos = reader.retrieve_setup_info()
    #print(len(setup_infos))
    #pprint(setup_infos[0])

    run_infos = reader.retrieve_run_info()
    #print(len(run_infos))
    #pprint(run_infos[0])

    imgs = reader.retrieve_image_info()
    #print(len(imgs))
    #pprint(imgs[0])

    #TODO: Currently we only extract and use the first md file extraction
    si = setup_infos[0] if len(setup_infos) == 1 else None
    ri = run_infos[0] if len(run_infos) == 1 else None

    output = OutputWriter.stitch_together(si, ri, imgs)
    OutputWriter.writeOutput(output, OUTPUT_PATH)

    reader.clean_up()

    logging.info("Temp folder deletion: {} - {}".format(tmpdir, os.path.exists(tmpdir)))

if __name__ == '__main__':
    run_cli()
