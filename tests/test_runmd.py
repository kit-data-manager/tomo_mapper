import unittest

from src.model.RunMD import RunMD
from src.model.SchemaConcepts.TOMO_Image import TOMO_Image
from src.model.SchemaConcepts.codegen.SchemaClasses import DatasetType


class TestSetupMD(unittest.TestCase):

    def test_get_dstypes(self):
        smd = RunMD()

        #no dataset types are returned since no images have been added
        self.assertFalse(smd.get_datasetTypes())

        smd.add_image(TOMO_Image(localPath="p"), DatasetType("SEM Image"))
        smd.add_image(TOMO_Image(localPath="p"), DatasetType("SEM Image"))

        self.assertEqual(1, len(smd.get_datasetTypes()))

        self.assertEqual(2, len(smd.get_images_for_datasetType(DatasetType("SEM Image"))))
