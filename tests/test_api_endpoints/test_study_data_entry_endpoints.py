# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random

import pytest

from castoredc_api_client.exceptions import CastorException
from tests.test_api_endpoints.data_models import (
    study_data_point_extended_model,
    data_options,
)


class TestStudyDataEntry:
    model_keys = study_data_point_extended_model.keys()

    def test_all_study_data_record_success(self, client, all_study_data_points):
        # Grab a record with data
        random_field = random.choice(all_study_data_points)
        record = random_field["record_id"]
        study_data = client.all_study_fields_record(record)
        for field in study_data:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in study_data_point_extended_model[key]

    def test_all_study_data_record_fail(self, client, all_study_data_points):
        random_field = random.choice(all_study_data_points)
        with pytest.raises(CastorException) as e:
            client.all_study_fields_record(random_field["record_id"] + "FAKE")
        assert str(e.value) == "404 The record you requested data for does not exist"

    def test_single_study_data_point_record_success(
        self, client, all_study_data_points
    ):
        random_field = random.choice(all_study_data_points)
        record = random_field["record_id"]
        field = random_field["field_id"]
        study_data = client.single_study_field_record(record, field)
        study_data_keys = study_data.keys()
        assert len(study_data_keys) == len(self.model_keys)
        for key in study_data_keys:
            assert key in self.model_keys
            assert type(study_data[key]) in study_data_point_extended_model[key]

    def test_single_study_data_point_record_fail(self, client, all_study_data_points):
        random_field = random.choice(all_study_data_points)
        record = random_field["record_id"]
        field = random_field["field_id"] + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_study_field_record(record, field)
        assert str(e.value) == "500 The application has encountered an error"

    def test_update_single_study_field_record_success(
        self, client, all_study_data_points
    ):
        random_field = random.choice(all_study_data_points)
        record = random_field["record_id"]
        field = random_field["field_id"]
        old_value = random_field["field_value"]

        # Get the allowed values to update
        field_exp = client.single_field(field)
        if field_exp["field_type"] == "numeric":
            min_val = field_exp["field_min"]
            max_val = field_exp["field_max"]
            if min_val is None:
                min_val = 0
            if max_val is None:
                max_val = 99
            post_value = random.choice(range(min_val, max_val))
        else:
            post_value = data_options[field_exp["field_type"]]

        # Update the field
        change_reason = "Testing API"
        feedback = client.update_single_study_field_record(
            record, field, post_value, change_reason
        )

        # Check if changing worked
        new_value = client.single_study_field_record(record, field)
        assert new_value["value"] == str(post_value)

    def test_update_single_study_field_record_fail(self, client, all_study_data_points):
        random_field = random.choice(all_study_data_points)
        record = random_field["record_id"]
        field = random_field["field_id"]
        old_value = random_field["field_value"]

        # Get the allowed values to update
        field_exp = client.single_field(field)
        if field_exp["field_type"] == "numeric":
            min_val = field_exp["field_min"]
            max_val = field_exp["field_max"]
            if min_val is None:
                min_val = 0
            if max_val is None:
                max_val = 99
            post_value = random.choice(range(min_val, max_val))
        else:
            post_value = data_options[field_exp["field_type"]]

        # Update the field
        change_reason = "Testing API"

        with pytest.raises(CastorException) as e:
            client.update_single_study_field_record(
                record, "FAKE" + field + "FAKE", post_value, change_reason
            )
        assert str(e.value) == "500 Could not create data point(s)"

        new_value = client.single_study_field_record(record, field)
        assert new_value["value"] == str(old_value)
