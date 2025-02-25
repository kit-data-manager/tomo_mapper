# SEM-FIB-Tomography mapper

## Usage

- get the code to use it locally
```
git clone ...
cd tomo_mapper
```
- install your favourite virtual environment and activate it (optional)

```
pip install -r requirements.txt
python -m mapping_cli
```

### Tomography and SEM mapping

SEM-FIB-Tomography mapping and SEM mapping share a common mapping concept. At the moment both reside in the same code base for easier testing and code reuse. This may be subject to change.

Usage of Tomography mapping with subcommand `tomo`. Currently the tomo mapper expects a map file, a zip file and a json output path.

Usage of SEM mapping with subcommand `sem`. Currently the sem mapper expects a map file, an image or metadata file and a json output path.

## Testing

```
pytest tests
```

