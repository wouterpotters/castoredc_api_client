# -*- coding: utf-8 -*-
"""
Testing class for field-validation endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-validation

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestFieldvalidation:
    field_val_model = {
        "id": "int",
        "type": "string",
        "value": "string",
        "operator": "string",
        "text": "string",
        "field_id": "string",
        "_links": "dict",
    }
    model_keys = field_val_model.keys()

    @pytest.fixture(scope="class")
    def all_field_vals(self, client):
        all_field_vals = client.all_field_validations()
        return all_field_vals

    def test_all_field_vals(self, all_field_vals, item_totals):
        assert len(all_field_vals) > 0
        assert len(all_field_vals) == item_totals["total_field_vals"]

    def test_all_field_vals_model(self, all_field_vals):
        for i in range(0, 5):
            rand_field = random.choice(all_field_vals)
            api_keys = rand_field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_success(self, client, all_field_vals):
        for i in range(0, 5):
            rand_id = random.choice(all_field_vals)["id"]
            opt = client.single_field_validation(rand_id)
            api_keys = opt.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_failure(self, client, all_field_vals):
        for i in range(0, 5):
            rand_id = random.choice(all_field_vals)["id"] - 10 ** 10
            opt = client.single_field_validation(rand_id)
            assert opt is None
