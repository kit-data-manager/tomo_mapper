# SEM-FIB-Tomography Mapper

## Overview
SEM-FIB-Tomography Mapper is a tool designed for mapping and analyzing SEM (Scanning Electron Microscope) images and SEM-FIB Tomography data. This project includes functionality for both SEM and tomography mapping, sharing a common mapping concept.

## Usage

### 1. Python Command Line Interface

#### Prerequisites

Minimal supported python version: 3.10

#### Cloning the Repository
To get started, clone the repository and navigate to the project directory:
```
git clone https://github.com/kit-data-manager/tomo_mapper.git
cd tomo_mapper
```

#### Setting Up the Environment
You can optionally set up a virtual environment. Depending on your environment, you may have to use the `python3` alias instead of `python` for the following commands.

Install the required dependencies:
```
pip install -r requirements.txt
```

#### Running the Mapper
To run the mapper, use the `mapping_cli` module:
```
python -m mapping_cli
```

**1. Tomography Mapping**

Use the `tomo` subcommand for tomography mapping. The mapper expects a map file, a zip file, and a JSON output path:
```
python -m mapping_cli tomo -m <map_file> -i <zip_file> -o <json_output_path>
```

Fur further information about the necessary map file, see [Parsing README](./src/resources/maps/parsing/README.md)

**2. SEM Mapping**

Use the `sem` subcommand for SEM mapping. The mapper expects a map file, an image or image metadata file, and a JSON output path:
```
python -m mapping_cli sem -m <map_file> -i <zip_file> -o <json_output_path>
```

For further information about the necessary map file, see [TBD]

### 2. Command Line Interface Executable

Each release contains the python CLI as platform-specific packaged executable. Usage is identical to use with python, just replace
`python -m mapping_cli` with the platform-specific executable.

### 3. Usage as plugin for the [Mapping-Service](https://github.com/kit-data-manager/mapping-service)

The mapper can be used as a plugin for the [kit-data-manager/Mapping-Service](https://github.com/kit-data-manager/mapping-service). The necessary gradle project to build the plugin is included in the [plugin subfolder](./mappingservice-plugin).

Plugin and Python code base share the same semantic versioning, so the plugin version always indicates the specific script version used for mapping.

## Testing
Run tests using `pytest`:
```
pytest tests
```

## Supported instruments and formats

Due to the large range and variety of vendors, instruments and setups we cannot guarantee successful mapping for all cases. 
The following list provides the minimal range of formats, that have been tested via sample data.

### Image Metadata (SEM and Tomography Mapping)

- tiff format
  -  Carl Zeiss SEM (Zeiss instruments, tag 34118)
  -  FibicsXML (Zeiss instruments, tag 51023)
  -  FEI Helios (FEI / Thermofisher, tag 34682)

### Tomography metadata

- XML format
  - ATLAS3D-Job (Zeiss)
  - XML ATLAS3D-Setup (Zeiss)
  - XML EMProject (Thermofisher)
  - XML ProjectData (Thermofisher)

### Planned, currently not supported
- Tescan png hdr files
- JEOL bmp hdr files