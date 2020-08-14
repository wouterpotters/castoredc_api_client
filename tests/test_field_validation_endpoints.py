# -*- coding: utf-8 -*-
"""
Testing class for field-validation endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-validation

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.data_models import field_val_model
from castoredc_api_client.exceptions import CastorException


class TestFieldValidation:
    model_keys = field_val_model.keys()

    @pytest.fixture(scope="class")
    def all_field_vals(self, client):
        all_field_vals = client.all_field_validations()
        return all_field_vals

    def test_all_field_vals(self, all_field_vals, item_totals):
        assert len(all_field_vals) > 0
        assert len(all_field_vals) == item_totals["total_field_vals"]

    def test_all_field_vals_model(self, all_field_vals):
        rand_field = random.choice(all_field_vals)
        api_keys = rand_field.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(rand_field[key]) in field_val_model[key]

    def test_single_field_success(self, client, all_field_vals):
        rand_id = random.choice(all_field_vals)["id"]
        opt = client.single_field_validation(rand_id)
        api_keys = opt.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(opt[key]) in field_val_model[key]

    def test_single_field_failure(self, client, all_field_vals):
        with pytest.raises(CastorException) as e:
            client.single_field_validation(random.choice(all_field_vals)["id"] - 10 ** 10)
        assert str(e.value) == "404 Entity not found."
