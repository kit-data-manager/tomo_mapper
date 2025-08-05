import json
from datetime import datetime

from tomo_mapper.config import MappingConfig
from tomo_mapper.model.SchemaConcepts.SEM_Image import SEM_Image
from tomo_mapper.model.SchemaConcepts.TOMO_Image import TOMO_Image


class TestSEMImage:
    json_payload = """
        {
            "entry": {
                "title": "JEOL SEM - etched sidewall 01",
                "endTime": "2010-10-01T08:44:19",
                "program": {
                    "programVersion": "1.0"
                },
                "user": {
                    "userName": "Blumenthal"
                },
                "instrument": {
                    "instrumentName": "JEOL-SEM",
                    "instrumentManufacturer": {
                        "modelName": "7600F"
                    },
                    "chamberPressure": {
                        "value": 0.0
                    },
                    "eBeamSource": {
                        "accelerationVoltage": {
                            "value": 1.0
                        },
                        "beamCurrent": {
                            "value": 0.0
                        },
                        "gunVacuum": {
                            "value": 9.634e-05
                        }
                    },
                    "stage": {
                        "coordinateReference": "origin at centre of sample",
                        "tiltCorrectionAngle": {
                            "value": 298.8
                        },
                        "tiltCorrectionType": "none",
                        "eBeamWorkingDistance": {
                            "value": 2.77
                        }
                    },
                    "imaging": {
                        "collectionMethod": "normal scan",
                        "apertureSetting": {
                            "size": {
                                "value": 9.0
                            }
                        },
                        "dwellTime": {
                            "value": 3.0
                        },
                        "cycleTime": {
                            "value": 9.0
                        }
                    },
                    "detectors": {
                        "signalMixingDone": false,
                        "detector1": {
                            "detectorType": "Secondary Electron",
                            "detectorName": "0"
                        }
                    }
                }
            }
        }      
    """

    def test_deserialize_json(self):
        """
        Test must read in sample without error
        """

        image_dict = json.loads(self.json_payload)
        image_obj = SEM_Image(**image_dict)

    def test_date(self):
        """
        tests if date strings are both read in and converted to schema conform string successfully
        """
        #TODO: how do we even make sure we parse correctly, for example if no time zone is given?

        MappingConfig.set_working_dir("w")

        #German date format
        entryDict = {"endTime":"01.01.2020 00:00:00"}
        img = SEM_Image(entry=entryDict)
        assert img.entry.endTime.year == 2020
        img.to_schema_dict()

        #generously reading in date as datetime
        entryDict["endTime"] = "2020-01-01"
        img = SEM_Image(entry=entryDict)
        assert img.entry.endTime.year == 2020
        img.to_schema_dict()

        #iso date formats
        entryDict["endTime"] = "2020-01-01 00:00:00"
        img = SEM_Image(entry=entryDict)
        assert img.entry.endTime.year == 2020
        img.to_schema_dict()

        entryDict["endTime"] = "2017-04-04T16:22:20.855+02:00"
        img = SEM_Image(entry=entryDict)
        assert img.entry.endTime.year == 2017
        output_dict = img.to_schema_dict()
        assert output_dict["entry"]["endTime"].endswith("Z")
        assert "14:22:20" in output_dict["entry"]["endTime"]

        #setting with expected output format
        img.entry.endTime = "2017-04-04T16:22:20.855"
        #TODO: careful, this is not setting a datetime but a string - behaviour should likely be changed?
        img.to_schema_dict()

        #Other date formats (e.g. from ProjectData.dat in TF data)
        entryDict["endTime"] = "07/07/2023 10:12:46"
        img = SEM_Image(entry=entryDict)
        assert img.entry.endTime.year == 2023
        img.to_schema_dict()

        #setting with datetime object directly (for whatever reason)
        dt = datetime(2020, 1, 1, 0, 0, 0)
        img.entry.endTime = dt
        img.to_schema_dict()


