# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random

from tests.conftest import data_options


class TestReportDataEntry:
    report_data_point_model = {
        "record_id": "string",
        "field_variable_name": "string",
        "field_id": "string",
        "value": "string",
        "updated_on": "string",
        "report_instance_id": "string",
        "_embedded": "dict",
        "_links": "dict",
    }
    model_keys = report_data_point_model.keys()

    data_options = data_options

    def test_single_report_instance_all_fields_record_success(self,
                                                              client,
                                                              all_report_data_points):
        for i in range(0, 3):
            # Get all filled in report data points
            random_report_field = random.choice(all_report_data_points)
            random_id = random_report_field["report_instance_id"]
            random_record = random_report_field["record_id"]
            report = client.single_report_instance_all_fields_record(random_record,
                                                                     random_id)
            assert len(report) > 0
            for field in report:
                field_keys = field.keys()
                assert len(field_keys) == len(self.model_keys)
                for key in field_keys:
                    assert key in self.model_keys

    def test_single_report_instance_all_fields_record_fail(self,
                                                           client,
                                                           all_report_data_points):
        for i in range(0, 3):
            # Get all filled in report data points
            random_report_field = random.choice(all_report_data_points)
            random_id = random_report_field["report_instance_id"] + "FAKE"
            random_record = random_report_field["record_id"]
            report = client.single_report_instance_all_fields_record(random_record,
                                                                     random_id)
            assert report is None

    def test_single_report_instance_single_field_record_success(self,
                                                                client,
                                                                all_report_data_points):
        for i in range(0, 3):
            # Get all filled in report data points
            random_report_field = random.choice(all_report_data_points)
            random_id = random_report_field["report_instance_id"]
            random_record = random_report_field["record_id"]
            random_field = random_report_field["field_id"]
            field = client.single_report_instance_single_field_record(random_record,
                                                                      random_id,
                                                                      random_field)
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys

    def test_single_report_instance_single_field_record_fail(self,
                                                             client,
                                                             all_report_data_points):
        for i in range(0, 3):
            # Get all filled in report data points
            random_report_field = random.choice(all_report_data_points)
            random_id = random_report_field["report_instance_id"]
            random_record = random_report_field["record_id"]
            random_field = random_report_field["field_id"] + "FAKE"
            field = client.single_report_instance_single_field_record(random_record,
                                                                      random_id,
                                                                      random_field)
            assert field is None

    def test_update_report_instance_single_field_record_success(self,
                                                                client,
                                                                all_report_data_points):
        for i in range(0, 3):
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
            feedback = client.update_report_instance_single_field_record(record,
                                                                         report,
                                                                         field,
                                                                         change_reason,
                                                                         post_value)

            # Check if changing worked
            assert feedback is not None
            new_value = client.single_report_instance_single_field_record(record,
                                                                          report,
                                                                          field)
            assert new_value["value"] == str(post_value)
            if str(post_value) != str(old_value):
                assert new_value["value"] != str(old_value)

    def test_update_report_instance_single_field_record_fail(self,
                                                             client,
                                                             all_report_data_points):
        # Also test if no change happens if post_value == old_value
        for i in range(0, 3):
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
            feedback = client.update_report_instance_single_field_record(record,
                                                                         report,
                                                                         field + "FAKE",
                                                                         post_value,
                                                                         change_reason)

            # Check if changing worked
            assert feedback is None
            new_value = client.single_report_instance_single_field_record(record,
                                                                          report,
                                                                          field)
            assert new_value["value"] == old_value
