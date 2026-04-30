from pydantic import BaseModel

from src.model.SchemaConcepts.Acquisition_simplified import Acquisition
from mappingservice_plugincore.mappingservice_plugincore.model.SetupMD import SetupMD as GenericSetupMD

class SetupMD(GenericSetupMD):
    """
    contains metadata derived from file(s) describing the experiment setup
    MUST contain some acquisition metadata
    """

    acquisition_metadata: Acquisition