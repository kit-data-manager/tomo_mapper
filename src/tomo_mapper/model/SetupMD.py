from pydantic import BaseModel

from tomo_mapper.model.SchemaConcepts.Acquisition_simplified import Acquisition


class SetupMD(BaseModel):
    """
    contains metadata derived from file(s) describing the experiment setup
    MUST contain some acquisition metadata
    """

    acquisition_metadata: Acquisition