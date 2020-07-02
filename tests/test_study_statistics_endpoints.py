# -*- coding: utf-8 -*-
"""
Testing class for statistics endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest


class TestStatistics:
    statistics_model = {
        "study_id": "string",
        "records": "dict",
        "_links": "dict",
    }

    records_model = {
        "total_count": "int",
        "institutes": "list",
    }

    institutes_model = {
        "institute_id": "string",
        "institute_name": "string",
        "record_count": "int",
    }

    s_model_keys = statistics_model.keys()
    r_model_keys = records_model.keys()
    i_model_keys = institutes_model.keys()

    @pytest.fixture(scope="session")
    def stats(self, client):
        stats = client.statistics()
        return stats

    def test_study_statistics(self, stats):
        stats_keys = stats.keys()
        assert len(stats_keys) == len(self.s_model_keys)
        for key in stats_keys:
            assert key in self.s_model_keys

    def test_study_statistics_records(self, stats):
        records = stats["records"]
        records_keys = records.keys()
        assert len(records_keys) == len(self.r_model_keys)
        for key in records_keys:
            assert key in self.r_model_keys

    def test_study_statistics_institutes(self, stats):
        institutes = stats["records"]["institutes"]
        for institute in institutes:
            institute_keys = institute.keys()
            assert len(institute_keys) == len(self.i_model_keys)
            for key in institute_keys:
                assert key in self.i_model_keys
