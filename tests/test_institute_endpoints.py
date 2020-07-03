# -*- coding: utf-8 -*-
"""
Testing class for institute endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/institute

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class Testinstitute:
    institute_model = {
        "id": "string",
        "institute_id": "string",
        "name": "string",
        "abbreviation": "string",
        "code": "string",
        "order": "int",
        "country_id": "int",
        "deleted": "boolean",
        "_links": "dict",
    }
    model_keys = institute_model.keys()

    @pytest.fixture(scope="class")
    def all_institutes(self, client):
        all_institutes = client.all_institutes()
        return all_institutes

    def test_all_institutes(self, all_institutes, item_totals):
        assert len(all_institutes) > 0
        assert len(all_institutes) == item_totals["total_institutes"]

    def test_all_institutes_model(self, all_institutes):
        for i in range(0, 3):
            rand_institute = random.choice(all_institutes)
            api_keys = rand_institute.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_institute_success(self, client, all_institutes):
        for i in range(0, 3):
            rand_id = random.choice(all_institutes)["institute_id"]
            institute = client.single_institute(rand_id)
            api_keys = institute.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_institute_failure(self, client, all_institutes):
        for i in range(0, 3):
            rand_id = random.choice(all_institutes)["institute_id"] + "FAKE"
            institute = client.single_institute(rand_id)
            assert institute is None
