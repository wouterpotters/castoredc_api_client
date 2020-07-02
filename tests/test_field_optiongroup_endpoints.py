# -*- coding: utf-8 -*-
"""
Testing class for field-optiongroup endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-optiongroup

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestFieldOptionGroup:
    field_opt_model = {
        "id": "string",
        "name": "string",
        "description": "string",
        "layout": "boolean",
        "options": "list",
        "_links": "dict",
      }
    model_keys = field_opt_model.keys()

    @pytest.fixture(scope="class")
    def all_field_opts(self, client):
        all_field_opts = client.all_field_optiongroups()
        return all_field_opts

    def test_all_field_opts(self, all_field_opts, item_totals):
        assert len(all_field_opts) > 0
        assert len(all_field_opts) == item_totals["total_field_opts"]

    def test_all_field_opts_model(self, all_field_opts):
        for i in range(0, 3):
            rand_field = random.choice(all_field_opts)
            api_keys = rand_field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_success(self, client, all_field_opts):
        for i in range(0, 3):
            rand_id = random.choice(all_field_opts)["id"]
            opt = client.single_field_optiongroup(rand_id)
            api_keys = opt.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_failure(self, client, all_field_opts):
        # NOTE: API seems to truncate text after the ID.
        # i.e. if 247 is an existing ID, then 247TEXT also works.
        for i in range(0, 3):
            rand_id = random.choice(all_field_opts)["id"] + "FAKE"
            opt = client.single_field_optiongroup(rand_id)
            assert opt is None
