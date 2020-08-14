# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random

import pytest

from tests.data_models import report_data_point_extended_model, data_options
from castoredc_api_client.exceptions import CastorException


class TestReportDataEntry:
    model_keys = report_data_point_extended_model.keys()
    data_options = data_options

    def test_single_report_instance_all_fields_record_success(
        self, client, all_report_data_points
    ):
        # Get all filled in report data points
        random_report_field = random.choice(all_report_data_points)
        random_id = random_report_field["report_instance_id"]
        random_record = random_report_field["record_id"]
        report = client.single_report_instance_all_fields_record(
            random_record, random_id
        )

        for field in report:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in report_data_point_extended_model[key]

    def test_single_report_instance_all_fields_record_fail(
        self, client, all_report_data_points
    ):
        random_report_field = random.choice(all_report_data_points)
        random_id = random_report_field["report_instance_id"] + "FAKE"
        random_record = random_report_field["record_id"]
        with pytest.raises(CastorException) as e:
            client.single_report_instance_all_fields_record(random_record, random_id)
        assert str(e.value) == "404 The report you requested data for does not exist."

    def test_single_report_instance_single_field_record_success(
        self, client, all_report_data_points
    ):
        # Get all filled in report data points
        random_report_field = random.choice(all_report_data_points)
        random_id = random_report_field["report_instance_id"]
        random_record = random_report_field["record_id"]
        random_field = random_report_field["field_id"]
        field = client.single_report_instance_single_field_record(
            random_record, random_id, random_field
        )
        field_keys = field.keys()
        assert len(field_keys) == len(self.model_keys)
        for key in field_keys:
            assert key in self.model_keys
            assert type(field[key]) in report_data_point_extended_model[key]

    def test_single_report_instance_single_field_record_fail(
        self, client, all_report_data_points
    ):
        random_report_field = random.choice(all_report_data_points)
        random_id = random_report_field["report_instance_id"]
        random_record = random_report_field["record_id"]
        random_field = random_report_field["field_id"] + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_report_instance_single_field_record(
                random_record, random_id, random_field
            )
        assert str(e.value) == "404 The field you are interacting with does not exist."

    def test_update_report_instance_single_field_record_success(
        self, client, all_report_data_points
    ):
        # Get all filled in report data points
        random_report_field = random.choice(all_report_data_points)

        # Get information on the field
        report = random_report_field["report_instance_id"]
        record = random_report_field["record_id"]
        field = random_report_field["field_id"]
        old_value = random_report_field["field_value"]

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
        client.update_report_instance_single_field_record(
            record, report, field, change_reason, post_value
        )

        # Check if changing worked
        new_value = client.single_report_instance_single_field_record(
            record, report, field
        )
        assert new_value["value"] == str(post_value)

    def test_update_report_instance_single_field_record_fail(
        self, client, all_report_data_points
    ):
        # Get all filled in report data points
        random_report_field = random.choice(all_report_data_points)

        # Get information on the field
        report = random_report_field["report_instance_id"]
        record = random_report_field["record_id"]
        field = random_report_field["field_id"]
        old_value = random_report_field["field_value"]

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
            client.update_report_instance_single_field_record(
                record, report, field + "FAKE", post_value, change_reason
            )
        assert str(e.value) == "404 The field you are interacting with does not exist."

        # Check if changing actually failed
        new_value = client.single_report_instance_single_field_record(
            record, report, field
        )
        assert new_value["value"] == old_value
