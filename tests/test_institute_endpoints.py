# -*- coding: utf-8 -*-
"""
Testing class for institute endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/institute

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.data_models import institute_model
from castoredc_api_client.exceptions import CastorException


class TestInstitute:
    model_keys = institute_model.keys()

    @pytest.fixture(scope="class")
    def all_institutes(self, client):
        all_institutes = client.all_institutes()
        return all_institutes

    def test_all_institutes(self, all_institutes, item_totals):
        assert len(all_institutes) > 0
        assert len(all_institutes) == item_totals["total_institutes"]

    def test_all_institutes_model(self, all_institutes):
        rand_institute = random.choice(all_institutes)
        api_keys = rand_institute.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(rand_institute[key]) in institute_model[key]

    def test_single_institute_success(self, client, all_institutes):
        rand_id = random.choice(all_institutes)["institute_id"]
        institute = client.single_institute(rand_id)
        api_keys = institute.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(institute[key]) in institute_model[key]

    def test_single_institute_failure(self, client, all_institutes):
        with pytest.raises(CastorException) as e:
            client.single_institute(random.choice(all_institutes)["institute_id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
