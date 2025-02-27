from importlib import resources

files = resources.files(__name__)
tiffparser_sem_34682 = files.joinpath("SEM_thermofisher.json")
tiffparser_tomo_34682 = files.joinpath("TOMO_thermofisher_image.json")
tiffparser_sem_34118 = files.joinpath("SEM_zeiss.json")
tiffparser_tomo_51023 = files.joinpath("TOMO_zeiss_image.json")

