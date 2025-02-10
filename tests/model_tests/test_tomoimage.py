import json
import unittest
from datetime import datetime

from src.model.SchemaConcepts.TOMO_Image import TOMO_Image


class TestTOMOImage(unittest.TestCase):
    json_payload = """
                 {
                    "creationTime": "18.08.2020 13:45:16",
                    "stage": {
                        "workingDistance": {
                            "value": 0.00402381
                        },
                        "stageX": {
                            "value": 0.000225271
                        },
                        "stageY": {
                            "value": -0.00467317
                        },
                        "stageZ": {
                            "value": 0.00402333
                        },
                        "stageR": {
                            "value": 0.648119
                        },
                        "stageTa": {
                            "value": 0.33685
                        },
                        "stageTb": {
                            "value": 0
                        },
                        "activeStage": "Bulk"
                    },
                    "vacuum": {
                        "chamberPressure": {
                            "value": 0.000119
                        },
                        "userMode": "High vacuum"
                    },
                    "specimenCurrent": {
                        "value": -1.00539e-09
                    }
                }       
    """

    def test_deserialize_json(self):
        """
        Test must read in sample without error
        """

        image_dict = json.loads(self.json_payload)
        image_obj = TOMO_Image(**image_dict)

    def test_scientific_notation(self):

        image_dict = json.loads(self.json_payload)
        image_obj = TOMO_Image(**image_dict)

        self.assertGreater(-0.000000001, image_obj.specimenCurrent.value)
        self.assertLess(-0.000000002, image_obj.specimenCurrent.value)

    def test_date(self):
        """
        tests if date strings are both read in and converted to schema conform string successfully
        """
        #TODO: how do we even make sure we parse correctly, for example if no time zone is given?

        #German date format
        img = TOMO_Image(creationTime="01.01.2020 00:00:00")
        self.assertEqual(img.creationTime.year, 2020)
        img.to_schema_dict()

        #generously reading in date as datetime
        img = TOMO_Image(creationTime="2020-01-01")
        self.assertEqual(img.creationTime.year, 2020)
        img.to_schema_dict()

        #iso date formats
        img = TOMO_Image(creationTime="2020-01-01 00:00:00")
        self.assertEqual(img.creationTime.year, 2020)
        img.to_schema_dict()

        img = TOMO_Image(creationTime="2017-04-04T16:22:20.855+02:00")
        self.assertEqual(img.creationTime.year, 2017)
        img.to_schema_dict()

        #setting with expected output format
        img.creationTime = "2017-04-04T16:22:20.855"
        #TODO: careful, this is not setting a datetime but a string - behaviour should likely be changed?
        img.to_schema_dict()

        #Other date formats (e.g. from ProjectData.dat in TF data)
        img = TOMO_Image(creationTime="07/07/2023 10:12:46")
        self.assertEqual(img.creationTime.year, 2023)
        img.to_schema_dict()

        #setting with datetime object directly (for whatever reason)
        dt = datetime(2020, 1, 1, 0, 0, 0)
        img.creationTime = dt
        img.to_schema_dict()
