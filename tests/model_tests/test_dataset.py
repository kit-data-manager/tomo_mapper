from tomo_mapper.model.SchemaConcepts.Dataset_simplified import Dataset

class TestDataset:

    def test_pretilt(self):
        """
        This specific test is there to detect problems with unwanted definition in the current schema and a bug in pydantic.
        1. instrument.eBeam.preTilt has an erronous space in the schema definition. In the strictest sense the output of the mapper is not schema conform here
        2. pydantic 2.10 has trouble honoring nested aliases on model_dump. This should be addressed in 2.11 - workaround fix could then be removed
        :return:
        """
        instrument_md = {
            "eBeam": {
                "preTilt": {"value": 1234}
            }
        }

        ds = Dataset(instrument=instrument_md)