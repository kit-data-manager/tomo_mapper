from src.model.RunMD import RunMD
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses import DatasetType
from src.parser.RunMD_Parser import RunMD_Parser


class ProjectDataParser(RunMD_Parser):
    def parse_run(self, payload) -> tuple[RunMD, str]:
        parsed = self._read_input(payload)

        #get root dir for md file somehow?

        resultMD = parsed["Project"]["Results"]

        runMD = RunMD()

        for imgmd in resultMD["Image"]:
            if imgmd.get("ImagePurpose") and imgmd["ImagePurpose"] in DatasetType:
                fp = imgmd["@FilePath"]
                img = TOMO_Image(localPath=fp)
                runMD.add_image(img, DatasetType(imgmd["ImagePurpose"]))

        return RunMD(), parsed

    @staticmethod
    def expected_input_format():
        return "xml"