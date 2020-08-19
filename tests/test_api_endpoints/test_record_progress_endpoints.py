# -*- coding: utf-8 -*-
"""
Testing class for record progress endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record-progress

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random

import pytest

from tests.test_api_endpoints.data_models import record_progress_model, steps_model


class TestRecordProgress:
    record_progress_keys = record_progress_model.keys()
    steps_keys = steps_model.keys()

    @pytest.fixture(scope="class")
    def progress_report(self, client):
        progress_report = client.record_progress()
        return progress_report

    def test_record_progress(self, progress_report, client):
        assert len(progress_report) == len(
            client.all_records(archived=0)
        )
        record = random.choice(progress_report)
        api_record_keys = record.keys()
        assert len(api_record_keys) == len(self.record_progress_keys)

        for key in api_record_keys:
            assert key in self.record_progress_keys
            assert type(record[key]) in record_progress_model[key]

            for step in record["steps"]:
                api_step_keys = step.keys()
                assert len(api_step_keys) == len(self.steps_keys)
                for step_key in api_step_keys:
                    assert step_key in self.steps_keys
                    assert type(step[step_key]) in steps_model[step_key]
