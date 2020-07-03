# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random
from tests.conftest import data_options


class TestStudyDataEntry:
    study_data_point_model = {
        "record_id": "string",
        "field_variable_name": "string",
        "field_id": "string",
        "value": "string",
        "updated_on": "string",
        "_embedded": "dict",
        "_links": "dict",
    }
    model_keys = study_data_point_model.keys()

    data_options = data_options

    def test_all_study_data_record_success(self, client, all_study_data_points):
        for i in range(0, 3):
            random_field = random.choice(all_study_data_points)
            record = random_field["record_id"]
            study_data = client.all_study_fields_record(record)
            assert len(study_data) > 0
            for field in study_data:
                field_keys = field.keys()
                assert len(field_keys) == len(self.model_keys)
                for key in field_keys:
                    assert key in self.model_keys

    def test_all_study_data_record_fail(self, client, all_study_data_points):
        for i in range(0, 3):
            random_field = random.choice(all_study_data_points)
            record = random_field["record_id"] + "FAKE"
            study_data = client.all_study_fields_record(record)
            assert study_data is None

    def test_single_study_data_point_record_success(
        self, client, all_study_data_points
    ):
        for i in range(0, 3):
            random_field = random.choice(all_study_data_points)
            record = random_field["record_id"]
            field = random_field["field_id"]
            study_data = client.single_study_field_record(record, field)
            study_data_keys = study_data.keys()
            assert len(study_data_keys) == len(self.model_keys)
            for key in study_data_keys:
                assert key in self.model_keys

    def test_single_study_data_point_record_fail(self, client, all_study_data_points):
        for i in range(0, 3):
            random_field = random.choice(all_study_data_points)
            record = random_field["record_id"]
            field = random_field["field_id"] + "FAKE"
            study_data = client.single_study_field_record(record, field)
            assert study_data is None

    def test_update_single_study_field_record_success(
        self, client, all_study_data_points
    ):
        # TODO: Also test if change works if new_value == old_value
        for i in range(0, 3):
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
                post_value = self.data_options[field_exp["field_type"]]

            # Update the field
            change_reason = "Testing API"
            feedback = client.update_single_study_field_record(
                record, field, post_value, change_reason
            )

            # Check if changing worked
            assert feedback is not None
            new_value = client.single_study_field_record(record, field)
            assert new_value["value"] == str(post_value)
            if str(post_value) != str(old_value):
                assert new_value["value"] != str(old_value)

    def test_update_single_study_field_record_fail(self, client, all_study_data_points):
        # TODO: Also test if no change if post_value == old_value
        for i in range(0, 3):
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
                post_value = self.data_options[field_exp["field_type"]]

            # Update the field
            change_reason = "Testing API"
            feedback = client.update_single_study_field_record(
                record, "FAKE" + field + "FAKE", post_value, change_reason
            )

            assert feedback is None
            new_value = client.single_study_field_record(record, field)
            assert new_value["value"] == str(old_value)
