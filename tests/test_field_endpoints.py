# -*- coding: utf-8 -*-
"""
Testing class for field endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestField:
    field_model = {
        "id": "string",
        "parent_id": "string",
        "field_id": "string",
        "field_number": "int",
        "field_label": "string",
        "field_is_alias": "boolean",
        "field_variable_name": "string",
        "field_type": "string",
        "field_required": "int",
        "field_hidden": "int",
        "field_info": "string",
        "field_units": "string",
        "field_min": "int",
        "field_min_label": "string",
        "field_max": "int",
        "field_max_label": "string",
        "field_summary_template": "string",
        "field_slider_step": "unknown",  # TODO: unclear return value
        "report_id": "",
        "field_length": "unknown",  # TODO: unclear return value
        "additional_config": "string",
        "exclude_on_data_export": "boolean",
        "option_group": "unknown",  # TODO: unclear return value
        "metadata_points": "list",
        "validations": "list",
        "dependency_parents": "list",
        "dependency_children": "list",
        "_links": "dict",
        }

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

    def test_single_field_success(self, client, all_fields):
        for i in range(0, 3):
            rand_field = random.choice(all_fields)["field_id"]
            field = client.single_field(rand_field)
            api_keys = field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_failure(self, client, all_fields):
        for i in range(0, 3):
            rand_field = random.choice(all_fields)["field_id"] + "FAKE"
            field = client.single_field(rand_field)
            assert field is None
