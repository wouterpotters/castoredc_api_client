# -*- coding: utf-8 -*-
"""
Testing class for record progress endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record-progress

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest


class TestRecordProgress:
    record_model = {
        "record_id": "string",
        "steps": "list",
        "_links": "dict",
    }

    steps_model = {
        "step_id": "string",
        "complete": "int",
        "sdv": "boolean",
        "locked": "boolean",
        "signed": "boolean"
    }

    record_keys = record_model.keys()
    steps_keys = steps_model.keys()

    @pytest.fixture(scope="class")
    def progress_report(self, client):
        progress_report = client.record_progress()
        return progress_report

    def test_record_progress(self, progress_report, all_record_ids):
        # Test if all records are added
        assert len(progress_report) == len(all_record_ids)
        for record in progress_report:
            api_record_keys = record.keys()
            assert len(api_record_keys) == len(self.record_keys)
            for key in api_record_keys:
                assert key in self.record_keys

            for step in record["steps"]:
                api_step_keys = step.keys()
                assert len(api_step_keys) == len(self.steps_keys), "See TODO under report_progress in client"
                for key in api_step_keys:
                    assert key in self.steps_keys
