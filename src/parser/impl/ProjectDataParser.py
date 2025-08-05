from typing import List

from src.model.RunMD import RunMD
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses_TOMO import DatasetType
from src.parser.RunMD_Parser import RunMD_Parser
from src.util import normalize_path


class ProjectDataParser(RunMD_Parser):
    @staticmethod
    def supported_input_sources() -> List[str]:
        return ['Thermofisher Helios']

    def parse_run(self, payload) -> RunMD:
        parsed = self._read_input(payload)

        resultMD = parsed["Project"]["Results"]

        runMD = RunMD()

        for imgmd in resultMD["Image"]:
            if imgmd.get("ImagePurpose") and imgmd["ImagePurpose"] in DatasetType:
                fp = normalize_path(imgmd["@FilePath"])
                img = TOMO_Image(localPath=fp)
                runMD.add_image(img, DatasetType(imgmd["ImagePurpose"]))

        return runMD

    @staticmethod
    def expected_input_format():
        return "text/xml"