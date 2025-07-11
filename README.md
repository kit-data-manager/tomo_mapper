<!--![Tests](https://github.com/kit-data-manager/tomo_mapper/actions/workflows/python-app.yml/badge.svg)-->
![Tests](https://img.shields.io/github/actions/workflow/status/kit-data-manager/tomo_mapper/python-app.yml?label=Tests)
[![Coverage Status](https://coveralls.io/repos/github/kit-data-manager/tomo_mapper/badge.svg)](https://coveralls.io/github/kit-data-manager/tomo_mapper)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# SEM-FIB-Tomography Mapper

## Overview
SEM-FIB-Tomography Mapper is a tool designed for mapping SEM (Scanning Electron Microscope) images and SEM-FIB Tomography metadata to a uniform, schema-compliant json format. This project includes functionality for both SEM and tomography mapping, sharing a common mapping concept.

The target format of the mapper follows pre-defined schemas developed for metadata description of SEM microscopy and SEM-FIB tomography, respectively. Technical information is contained in this repository,
for further conceptional description see

- Joseph, R., Chauhan, A., Eschke, C., Ihsan, A. Z., Jalali, M., Jäntsch, U., Jung, N., Shyam Kumar, C. N., Kübel, C., Lucas, C., Mail, M., Mazilkin, A., Neidiger, C., Panighel, M., Sandfeld, S., Stotzka, R., Thelen, R., & Aversa, R. (2021). Metadata schema to support FAIR data in scanning electron microscopy. CEUR-WS.Org. https://doi.org/10.5445/IR/1000141604
- Pauly, C., Joseph, R. E., Vitali, E. G. G., Aversa, R., Stotzka, R., Mücklich, F., Engstler, M., Hermann, H.-G., & Fell, J. (2024). Metadata schema and mapping service for FIB/SEM serial-sectioning and computed tomography. https://doi.org/10.5445/IR/1000175919

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

**1. SEM Mapping**

Use the `sem` subcommand for SEM mapping. The mapper expects a map file, an image or image metadata file, and a JSON output path:
```
python -m mapping_cli sem -m <map_file> -i <image or metadata file> -o <json_output_path>
```

For further information about the necessary map file, see [Mapping README](src/tomo_mapper/resources/maps/mapping)

**2. Tomography Mapping**

Use the `tomo` subcommand for tomography mapping. The mapper expects a map file, a zip file or input data folder, and a JSON output path:
```
python -m mapping_cli tomo -m <map_file> -i <zip_file or folder> -o <json_output_path>
```

For further information about the necessary map file, see [Parsing README](src/tomo_mapper/resources/maps/parsing)

For further information about mappings used internally, see [Mapping README](src/tomo_mapper/resources/maps/mapping)

In cases with no need of tweaking the parsing map file there is a shortcut option to use the supplied vendor-specific default map.

Example usage
```
python -m mapping_cli tomo -dm TF -i <zip_file or folder> -o <json_output_path>
```

This is equivalent to the following command run from the project folder of this repo
```
python -m mapping_cli tomo -m "./src/resources/maps/parsing/inputmap_thermofisher.json" -i <zip_file or folder> -o <json_output_path>
```

To get the current available default map options, check `tomo --help`. 

### 2. Command Line Interface Executable

Each release contains the python CLI as platform-specific packaged executable. Usage is identical to use with python, just replace
`python -m mapping_cli` with the platform-specific executable.

### 3. Usage as plugin for the [Mapping-Service](https://github.com/kit-data-manager/mapping-service)

The mapper can be used as a plugin for the [kit-data-manager/Mapping-Service](https://github.com/kit-data-manager/mapping-service). The necessary gradle project to build the plugin is included in the [plugin subfolder](./mappingservice-plugin).
For details on how to build the jar file, see the "Build with Gradle" step in the [github actions pipeline](./.github/workflows/plugin-integration.yml) for the plugin integration test.

Plugin and Python code base share the same semantic versioning, so the plugin version always indicates the specific script version used for mapping. This behaviour can be explicitly overriding 
(for example for testing or for working with older versions of the mapping service). To do this, on gradle build time provide the environment variable `VERSION_OVERRIDE_BY_BRANCH`.
The variable needs to contain a branch name of this repo and branch deletion may break a plugin in use. Only use this option very carefully. Do not use this option for production. 

To find out tested alignments between plugin versions and mapping-service versions check the following table:

| Plugin version | mapping-service version |
|----------------|------------------------|
| v1.0.0, v1.1.0 | v1.0.5*), v1.1.1*)     |

*) Plugin needs to be built with version override to work with the specified version of the mapping-service

## Testing
Run tests using `pytest`:
```
pytest
```

## Supported instruments and formats

Due to the large range and variety of vendors, instruments and setups we cannot guarantee successful mapping for all cases. 
The following list provides the **minimal range of formats, that have been tested via sample data**.

### Image Metadata (SEM and Tomography Mapping)

- tiff format
  -  Carl Zeiss SEM (Zeiss instruments, tag 34118)
  -  FibicsXML (Zeiss instruments, tag 51023)
  -  FEI Helios (FEI / Thermofisher, tag 34682) 
- text format
  -  Tescan hdr files
  -  JEOL txt files

### Tomography metadata

- XML format
  - ATLAS3D-Job (Zeiss)
  - ATLAS3D-Setup (Zeiss)
  - EMProject (Thermofisher)
  - ProjectData (Thermofisher)
  - TomographyProject (Tescan)
- HDR format
  - Dataset_info (Tescan)

## Acknowlegdements

This work is supported by the consortium NFDI-MatWerk, funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under the National Research Data Infrastructure – NFDI 38/1 – project number 460247524.

All sample and test data included in this repository, if not otherwise specified, was contributed by participant projects of NFDI-Matwerk. Special thanks to participant project pp13.

