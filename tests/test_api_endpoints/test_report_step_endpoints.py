# -*- coding: utf-8 -*-
"""
Testing class for report step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import report_step_model
from castoredc_api_client.exceptions import CastorException


class TestReportStep:
    model_keys = report_step_model.keys()

    @pytest.fixture(scope="class")
    def reports_with_steps(self, client):
        reports_with_steps = {}
        all_reports = client.all_reports()
        for report in all_reports:
            steps = client.single_report_all_steps(report["id"])
            reports_with_steps[report["id"]] = steps
        return reports_with_steps

    def test_all_report_steps(self, reports_with_steps):
        for report in reports_with_steps:
            assert len(reports_with_steps[report]) > 0
            for step in reports_with_steps[report]:
                assert len(step) == len(self.model_keys)
                api_keys = step.keys()
                for key in self.model_keys:
                    assert key in api_keys
                    assert type(step[key]) in report_step_model[key]

    def test_single_report_single_step_success(self, client, reports_with_steps):
        rand_report = random.choice(list(reports_with_steps.keys()))
        rand_step = random.choice(reports_with_steps[rand_report])["id"]
        step = client.single_report_single_step(rand_report, rand_step)
        api_keys = step.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(step[key]) in report_step_model[key]

    def test_single_report_single_step_failure(self, client, reports_with_steps):
        rand_report = random.choice(list(reports_with_steps.keys()))
        rand_step = random.choice(reports_with_steps[rand_report])["id"] + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_report_single_step(rand_report, rand_step)
        assert str(e.value) == "404 Entity not found."
