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
    survey_data_point_extended_model,
    data_options,
)


class TestSurveyDataEntry:
    model_keys = survey_data_point_extended_model.keys()
    data_options = data_options

    def test_single_survey_instance_all_fields_record_success(
        self, client, all_survey_data_points
    ):
        # Get all filled in survey data points
        random_survey_field = random.choice(all_survey_data_points)
        survey_id = random_survey_field["survey_instance_id"]
        record_id = random_survey_field["record_id"]
        survey = client.single_survey_instance_all_fields_record(record_id, survey_id)
        for field in survey:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in survey_data_point_extended_model[key]

    def test_single_survey_instance_all_fields_record_fail(
        self, client, all_survey_data_points
    ):
        # Get all filled in survey data points
        random_survey_field = random.choice(all_survey_data_points)
        survey_id = random_survey_field["survey_instance_id"]
        record_id = random_survey_field["record_id"] + "FAKE"

        with pytest.raises(CastorException) as e:
            client.single_survey_instance_all_fields_record(record_id, survey_id)
        assert str(e.value) == "404 The record you requested data for does not exist."

    def test_single_survey_instance_single_field_record_success(
        self, client, all_survey_data_points
    ):
        # Get all filled in survey data points
        random_survey_field = random.choice(all_survey_data_points)
        random_id = random_survey_field["survey_instance_id"]
        random_record = random_survey_field["record_id"]
        random_field = random_survey_field["field_id"]
        field = client.single_survey_instance_single_field_record(
            random_record, random_id, random_field
        )
        field_keys = field.keys()
        assert len(field_keys) == len(self.model_keys)
        for key in field_keys:
            assert key in self.model_keys
            assert type(field[key]) in survey_data_point_extended_model[key]

    def test_single_survey_instance_single_field_record_fail(
        self, client, all_survey_data_points
    ):
        for i in range(0, 3):
            # Get all filled in survey data points
            random_survey_field = random.choice(all_survey_data_points)
            random_id = random_survey_field["survey_instance_id"]
            random_record = random_survey_field["record_id"]
            random_field = random_survey_field["field_id"] + "FAKE"

            with pytest.raises(CastorException) as e:
                client.single_survey_instance_single_field_record(
                    random_record, random_id, random_field
                )
            assert str(e.value) == "400 The request you made was malformed"

    def test_update_survey_instance_single_field_record_success(
        self, client, all_survey_data_points
    ):
        # Get all filled in survey data points
        random_survey_field = random.choice(all_survey_data_points)

        # Get information on the field
        survey = random_survey_field["survey_instance_id"]
        record = random_survey_field["record_id"]
        field = random_survey_field["field_id"]
        old_value = random_survey_field["field_value"]

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
            post_value = self.data_options[field_exp["field_type"]]

        # Update the field
        change_reason = "Testing API"
        client.update_survey_instance_single_field_record(
            record, survey, field, post_value, change_reason
        )

        # Check if changing worked
        new_value = client.single_survey_instance_single_field_record(
            record, survey, field
        )
        assert new_value["value"] == str(post_value)

    def test_update_survey_instance_single_field_record_fail(
        self, client, all_survey_data_points
    ):
        # Get all filled in survey data points
        random_survey_field = random.choice(all_survey_data_points)

        # Get information on the field
        survey = random_survey_field["survey_instance_id"]
        record = random_survey_field["record_id"]
        field = random_survey_field["field_id"]
        old_value = random_survey_field["field_value"]

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
            post_value = self.data_options[field_exp["field_type"]]

        # Update the field
        change_reason = "Testing API"

        with pytest.raises(CastorException) as e:
            client.update_survey_instance_single_field_record(
                record, survey, field + "FAKE", post_value, change_reason
            )
        assert str(e.value) == "400 The request you made was malformed"

        # Check if changing failed
        new_value = client.single_survey_instance_single_field_record(
            record, survey, field
        )
        assert new_value["value"] == old_value
