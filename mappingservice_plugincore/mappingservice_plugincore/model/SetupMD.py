from typing import Any

from pydantic import BaseModel

class SetupMD(BaseModel):
    """
    Generic SetupMD - also independent of schema specifics.
    """
    acquisition_metadata: Any  # Plugin injects its Acquisition type