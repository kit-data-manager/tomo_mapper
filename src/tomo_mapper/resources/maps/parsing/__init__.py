from importlib import resources

files = resources.files(__name__)

default_zeiss = files.joinpath("inputmap_zeiss-auriga.json")
default_tf = files.joinpath("inputmap_thermofisher.json")
default_tescan = files.joinpath("inputmap_tescan-minimal.json")

map_from_flag = {
    "zeiss": default_zeiss,
    "tf": default_tf,
    "tescan": default_tescan,
}