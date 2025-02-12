import unittest

from src.model.RunMD import RunMD
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses import DatasetType


class TestSetupMD:

    def test_get_dstypes(self):
        smd = RunMD()

        #no dataset types are returned since no images have been added
        assert not smd.get_datasetTypes()

        smd.add_image(TOMO_Image(localPath="p"), DatasetType("SEM Image"))
        smd.add_image(TOMO_Image(localPath="p"), DatasetType("SEM Image"))

        assert len(smd.get_datasetTypes()) == 1

        assert len(smd.get_images_for_datasetType(DatasetType("SEM Image"))) == 2
