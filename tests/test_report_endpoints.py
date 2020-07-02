# -*- coding: utf-8 -*-
"""
Testing class for report endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestReport:
    report_model = {
        "id": "string",
        "report_id": "string",
        "description": "string",  # TODO: returned value unclear
        "name": "string",
        "type": "string",
        "_links": "dict",
    }

    model_keys = report_model.keys()

    @pytest.fixture(scope="class")
    def all_reports(self, client):
        all_reports = client.all_reports()
        return all_reports

    def test_all_reports(self, all_reports, item_totals):
        assert len(all_reports) > 0
        assert len(all_reports) == item_totals["total_reports"]

    def test_all_reports_model(self, all_reports):
        for i in range(0, 3):
            rand_report = random.choice(all_reports)
            api_keys = rand_report.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_report_success(self, client, all_reports):
        for i in range(0, 3):
            rand_id = random.choice(all_reports)["id"]
            report = client.single_report(rand_id)
            api_keys = report.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_report_failure(self, client, all_reports):
        for i in range(0, 3):
            rand_id = random.choice(all_reports)["id"] + "FAKE"
            report = client.single_report(rand_id)
            assert report is None
