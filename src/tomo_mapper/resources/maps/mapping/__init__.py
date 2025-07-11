from importlib import resources

files = resources.files(__name__)

tiffparser_sem_34682 = files.joinpath("SEM_thermofisher.json")
tiffparser_tomo_34682 = files.joinpath("TOMO_thermofisher_image.json")
tiffparser_sem_34118 = files.joinpath("SEM_zeiss.json")
tiffparser_tomo_51023 = files.joinpath("TOMO_zeiss_image.json")

textparser_tomo_tescan = files.joinpath("TOMO_tescan_image.json")
textparser_sem_tescan = files.joinpath("SEM_tescan.json")
textparser_sem_jeol = files.joinpath("SEM_jeol.json")

setup_zeiss = files.joinpath("TOMO_zeiss_setup.json")
setup_tf = files.joinpath("TOMO_thermofisher_setup.json")
setup_tescan = files.joinpath("TOMO_tescan_setup.json")

