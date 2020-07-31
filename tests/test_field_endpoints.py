# -*- coding: utf-8 -*-
"""
Testing class for field endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.data_models import field_model
from castoredc_api_client.exceptions import CastorException


class TestField:
    model_keys = field_model.keys()

    @pytest.fixture(scope="class")
    def all_fields(self, client):
        all_fields = client.all_fields()
        return all_fields

    def test_all_fields(self, all_fields, item_totals):
        assert len(all_fields) > 0
        assert len(all_fields) == item_totals["total_fields"]

    def test_all_fields_model(self, all_fields):
        for i in range(0, 3):
            rand_field = random.choice(all_fields)
            api_keys = rand_field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys
                assert type(rand_field[key]) in field_model[key]

    def test_single_field_success(self, client, all_fields):
        for i in range(0, 3):
            rand_field = random.choice(all_fields)["field_id"]
            field = client.single_field(rand_field)
            api_keys = field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys
                assert type(field[key]) in field_model[key], f"{key}"

    def test_single_field_failure(self, client, all_fields):
        with pytest.raises(CastorException) as e:
            client.single_field(random.choice(all_fields)["field_id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
