from dataclasses import dataclass

from typing import List

from src.model.Dataset import Dataset
from src.model.Schema_Concept import Schema_Concept

@dataclass
class Acquisition(Schema_Concept):

    technique: str = None
    measurementPurpose: str = None
    measurementDescription: str = None
    equipment: str = None
    consumables: list = None
    parents: list = None
    program: dict = None
    applicationID: dict = None
    fileVersion: str = None
    projectName: str = None
    projectID: dict = None
    userDescription: str = None
    zCutSpacing: dict = None
    millingLocationHeight: dict = None
    millingLocationWidth: dict = None
    millingLocationDepth: dict = None
    millingLocationX: dict = None
    millingLocationY: dict = None
    millingMaterial: str = None
    millingCurrent: dict = None
    numberOfCuts: int = None
    pump: str = None
    column: str = None
    source: str = None
    eucentricWorkingDistance: dict = None
    ESEM: bool = None
    systemType: str = None
    angleToEBeam: dict = None
    stage: str = None
    datasets: List[Dataset] = None

    def to_schema_dict(self):
        baseDict = self.__dict__
        datasetList = baseDict.pop("datasets")
        genericMetadata = {k: v for k, v in baseDict.items() if v is not None}
        datasets = [x.to_schema_dict() for x in datasetList]
        schema_dict = {"genericMetadata": genericMetadata, "datasets": datasets}
        return schema_dict