# -*- coding: utf-8 -*-
"""
Testing class for report endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import report_model
from castoredc_api_client.exceptions import CastorException


class TestReport:
    model_keys = report_model.keys()

    @pytest.fixture(scope="class")
    def all_reports(self, client):
        all_reports = client.all_reports()
        return all_reports

    def test_all_reports(self, all_reports, item_totals):
        assert len(all_reports) > 0
        assert len(all_reports) == item_totals["total_reports"]

    def test_all_reports_model(self, all_reports):
        rand_report = random.choice(all_reports)
        api_keys = rand_report.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(rand_report[key]) in report_model[key]

    def test_single_report_success(self, client, all_reports):
        rand_id = random.choice(all_reports)["id"]
        report = client.single_report(rand_id)
        api_keys = report.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(report[key]) in report_model[key]

    def test_single_report_failure(self, client, all_reports):
        with pytest.raises(CastorException) as e:
            client.single_report(random.choice(all_reports)["id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
