import argparse
import json
import logging
import os
from sys import exit

from src.IO.MappingAbortionError import MappingAbortionError
from src.IO.sem.InputReader import InputReader as InputReader_SEM
from src.IO.tomo.InputReader import InputReader as InputReader_TOMO
from src.IO.tomo.OutputWriter import OutputWriter
from src.resources.maps.parsing import map_from_flag

# make log level configurable from ENV, defaults to info level
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper()
)

def add_tomo_parser(subparsers):
    parser_t = subparsers.add_parser(
        "tomo",
        help="Tomography mapping functionality",
        description='Extracting of SEM FIB Tomography metadata to unified json format'
    )
    # Add arguments for input, output, and map
    parser_t.add_argument('-i', '--input', help='Input zip file or folder as path', required=True)
    parser_t.add_argument('-o', '--output', help='Path to output json file', required=True)

    # Create a group for the mutually exclusive map options
    map_group = parser_t.add_mutually_exclusive_group(required=True)

    # Add the map file option to the group
    map_group.add_argument('-m', '--map', help='Map file as path or remote URI')

    # Add the default map option to the group with the allowed values
    map_group.add_argument('-dm', '--default-map', help='Use a default map for a vendor', choices=map_from_flag.keys(), type=str.lower)

    parser_t.set_defaults(func=run_tomo_mapper)


def add_sem_parser(subparsers):
    parser_s = subparsers.add_parser(
        "sem",
        help="SEM mapping functionality",
        description='Extracting of SEM metadata to unified json format'
    )
    parser_s.add_argument('-i','--input', help='Input file as file path', required=True)
    parser_s.add_argument('-m', '--map', help='Map file as path or remote URI', required=True)
    parser_s.add_argument('-o', '--output', help='Path to output json file', required=True)
    parser_s.set_defaults(func=run_sem_mapper)

def run_cli():
    main_parser = argparse.ArgumentParser(prog="SEM-FIB-TOMO Mapper")
    subparsers = main_parser.add_subparsers(dest='command', help="Choose one of the subcommands to use mapper")
    add_tomo_parser(subparsers)
    add_sem_parser(subparsers)

    args = main_parser.parse_args()
    if args.command:
        args.func(args)
    else:
        main_parser.print_help()

def run_tomo_mapper(args):
    argdict = vars(args)
    INPUT_SOURCE = argdict.get('input')
    MAP_SOURCE = argdict.get('map') or str(map_from_flag.get(argdict.get('default_map')))
    OUTPUT_PATH = argdict.get('output')

    reader = None
    try:
        reader = InputReader_TOMO(MAP_SOURCE, INPUT_SOURCE)
        tmpdir = reader.temp_dir_path
    except MappingAbortionError as e:
        if reader:
            reader.clean_up()
        exit(e)

    try:
        setup_infos = reader.retrieve_setup_info()

        run_infos = reader.retrieve_run_info()

        imgs = reader.retrieve_image_info()

        # Now all cases are taken into account
        #si = setup_infos if len(setup_infos) >= 1 else None
        #ri = run_infos if len(run_infos) >= 1 else None

        output = OutputWriter.stitch_together(setup_infos, run_infos, imgs)
        OutputWriter.writeOutput(output, OUTPUT_PATH)
    except MappingAbortionError as e:
        reader.clean_up()
        exit(e)

    logging.info("Tomography mapping completed.")
    reader.clean_up()

def run_sem_mapper(args):
    argdict = vars(args)
    INPUT_SOURCE = argdict.get('input')
    MAP_SOURCE = argdict.get('map')
    OUTPUT_PATH = argdict.get('output')

    try:
        reader = InputReader_SEM(MAP_SOURCE, INPUT_SOURCE)

        img_info = reader.retrieve_image_info(INPUT_SOURCE)
        if not img_info:
            logging.error('Could not retrieve image information due to unknown error. Aborting.')
            exit(1)
        with open(OUTPUT_PATH, 'w', encoding="utf-8") as f:
            json.dump(img_info, f, indent=4, ensure_ascii=False)
    except MappingAbortionError as e:
        exit(e)


if __name__ == '__main__':
    run_cli()
