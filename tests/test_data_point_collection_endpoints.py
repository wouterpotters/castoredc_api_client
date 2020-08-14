# -*- coding: utf-8 -*-
"""
Testing class for data-point-collection endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/data-point-collection

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.data_models import study_data_point_model, report_data_point_model, survey_data_point_model
from castoredc_api_client.exceptions import CastorException
from tests.helper_functions import allowed_value


class TestDataPoint:
    study_data_point_model_keys = study_data_point_model.keys()
    report_data_point_model_keys = report_data_point_model.keys()
    survey_data_point_model_keys = survey_data_point_model.keys()

    def test_all_study_data_points_amount(self, all_study_data_points, item_totals):
        """Tests that the all_study_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_study_data_points) == item_totals["total_study_data_points"]

    def test_all_study_data_points_model(self, all_study_data_points):
        """Tests if the study data point model is the same as the specified model."""
        for i in range(0, 3):
            random_study_data_point = random.choice(all_study_data_points)
            api_keys = random_study_data_point.keys()
            assert len(self.study_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.study_data_point_model_keys
                assert type(random_study_data_point[key]) in study_data_point_model[key]

    def test_all_report_data_points_amount(self, all_report_data_points, item_totals):
        """Tests that the all_report_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_report_data_points) == item_totals["total_report_data_points"]

    def test_all_report_data_points_model(self, all_report_data_points):
        """Tests if the report data point model is the same as the specified model."""
        for i in range(0, 3):
            random_report_data_point = random.choice(all_report_data_points)
            api_keys = random_report_data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.report_data_point_model_keys
                assert type(random_report_data_point[key]) in report_data_point_model[key]

    def test_all_survey_data_points_amount(self, all_survey_data_points, item_totals):
        """Tests that the all_survey_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_survey_data_points) == item_totals["total_survey_data_points"]

    def test_all_survey_data_points_model(self, all_survey_data_points):
        """Tests if the survey data point model is the same as the specified model."""
        for i in range(0, 3):
            random_survey_data_point = random.choice(all_survey_data_points)
            api_keys = random_survey_data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.survey_data_point_model_keys
                assert type(random_survey_data_point[key]) in survey_data_point_model[key]

    def test_single_report_instance_data_points_success(
            self, client, all_report_data_points
    ):
        """Tests if single_report_instance_data_points returns the data points in the proper model."""
        random_report_id = random.choice(all_report_data_points)["report_instance_id"]
        random_report = client.single_report_instance_data_points(random_report_id)
        for random_report_data_point in random_report:
            api_keys = random_report_data_point.keys()
            for key in api_keys:
                assert key in self.report_data_point_model_keys
                assert type(random_report_data_point[key]) in report_data_point_model[key]

    def test_single_report_instance_data_points_fail(
            self, client, all_report_data_points
    ):
        """Tests if single_report_instance_data_points throws proper error when non-existing report is called."""
        random_report_id = random.choice(all_report_data_points)["report_instance_id"] + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_report_instance_data_points(random_report_id)
        assert str(e.value) == "404 Report Instance not found"

    def test_single_survey_instance_data_points_success(
            self, client, all_survey_data_points
    ):
        """Tests if single_survey_instance_data_points returns the data points in the proper model."""
        random_survey_id = random.choice(all_survey_data_points)["survey_instance_id"]
        random_survey = client.single_survey_instance_data_points(random_survey_id)
        for random_survey_data_point in random_survey:
            api_keys = random_survey_data_point.keys()
            for key in api_keys:
                assert key in self.survey_data_point_model_keys
                assert type(random_survey_data_point[key]) in survey_data_point_model[key]

    def test_single_survey_instance_data_points_fail(
            self, client, all_survey_data_points
    ):
        """Tests if single_survey_instance_data_points throws proper error when non-existing survey is called."""
        random_survey_id = random.choice(all_survey_data_points)["survey_instance_id"] + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_survey_instance_data_points(random_survey_id)
        assert str(e.value) == "404 Survey Package Instance not found"

    @pytest.fixture(scope="session")
    def all_survey_package_instance_ids(self, client):
        all_survey_package_instance = client.all_survey_package_instances()
        all_survey_package_instance_ids = [
            package["survey_package_instance_id"]
            for package in all_survey_package_instance
        ]
        return all_survey_package_instance_ids

    def test_single_survey_package_instance_data_points_success(
            self, client, all_survey_package_instance_ids
    ):
        api_package = []
        # Find a survey package with filled in fields
        while len(api_package) == 0:
            rand_id = random.choice(all_survey_package_instance_ids)
            api_package = client.single_survey_package_instance_data_points(rand_id)

        for data_point in api_package:
            api_keys = data_point.keys()
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_survey_package_instance_data_points_fail(
            self, client, all_survey_package_instance_ids
    ):
        rand_id = random.choice(all_survey_package_instance_ids) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_survey_package_instance_data_points(rand_id)
        assert str(e.value) == "404 Survey Package Instance not found"

    # ALL DATA - RECORD SPECIFIC
    def test_all_study_data_points_record_success(self, client, all_record_ids):
        all_data = []

        # Find a record with fields
        while len(all_data) == 0:
            random_id = random.choice(all_record_ids)
            all_data = client.all_study_data_points_record(random_id)

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.study_data_point_model_keys) == len(api_keys)
            for key in self.study_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in study_data_point_model[key]

    def test_all_study_data_points_record_fail(self, client, all_record_ids):
        random_id = random.choice(all_record_ids) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.all_study_data_points_record(random_id)
        assert str(e.value) == "404 Record not found"

    def test_all_report_data_points_record_success(self, client, all_record_ids):
        all_data = []
        while len(all_data) == 0:
            random_id = random.choice(all_record_ids)
            all_data = client.all_report_data_points_record(random_id)

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in self.report_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in report_data_point_model[key]

    def test_all_report_data_points_record_fail(self, client, all_record_ids):
        random_id = random.choice(all_record_ids) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.all_report_data_points_record(random_id)
        assert str(e.value) == "404 Record not found"

    def test_all_survey_data_points_record_success(self, client, all_record_ids):
        all_data = []
        while len(all_data) == 0:
            random_id = random.choice(all_record_ids)
            all_data = client.all_survey_data_points_record(random_id)

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_all_survey_data_points_record_fail(self, client, all_record_ids):
        random_id = random.choice(all_record_ids) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.all_survey_data_points_record(random_id)
        assert str(e.value) == "404 Record not found"

    # SINGLE SURVEY/REPORT - RECORD SPECIFIC
    def test_single_report_data_points_record_success(
            self, client, records_with_reports
    ):
        report_data = []
        while len(report_data) == 0:
            records = list(records_with_reports.keys())
            random_id = random.choice(records)
            random_report = random.choice(records_with_reports[random_id])
            report_data = client.single_report_data_points_record(
                random_id, random_report
            )

        for data_point in report_data:
            api_keys = data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in self.report_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in report_data_point_model[key]

    def test_single_report_data_points_record_fail(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        random_id = random.choice(records)
        random_report = random.choice(records_with_reports[random_id]) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_report_data_points_record(
                random_id, random_report
            )
        assert str(e.value) == "404 Report Instance not found"

    def test_single_survey_package_data_points_record_success(
            self, client, records_with_survey_package_instances
    ):
        survey_data = []
        while len(survey_data) == 0:
            records = list(records_with_survey_package_instances.keys())
            random_id = random.choice(records)
            random_package = random.choice(
                records_with_survey_package_instances[random_id]
            )
            survey_data = client.single_survey_package_data_points_record(
                random_id, random_package
            )

        for data_point in survey_data:
            api_keys = data_point.keys()
            assert (
                    len(self.survey_data_point_model_keys) == len(api_keys)
                    or len(api_keys) == 7
            ), "length is 6 or 7 in api. Does not always contain 'survey_package_id'"
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_survey_package_data_points_record_fail(
            self, client, records_with_survey_package_instances
    ):
        records = list(records_with_survey_package_instances.keys())
        random_id = random.choice(records)
        random_package = (
                random.choice(records_with_survey_package_instances[random_id]) + "FAKE"
        )
        with pytest.raises(CastorException) as e:
            client.single_survey_package_data_points_record(
                random_id, random_package
            )
        assert str(e.value) == "404 Survey Package Instance not found"

    def test_single_survey_data_points_record_success(
            self, client, records_with_survey_instances
    ):
        survey_data = []
        while len(survey_data) == 0:
            records = list(records_with_survey_instances.keys())
            random_id = random.choice(records)
            random_survey = random.choice(records_with_survey_instances[random_id])[0]
            survey_data = client.single_survey_data_points_record(
                random_id, random_survey
            )

        for data_point in survey_data:
            api_keys = data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_survey_data_points_record_fail(
            self, client, records_with_survey_instances
    ):
        records = list(records_with_survey_instances.keys())
        random_id = random.choice(records)
        random_survey = (
                random.choice(records_with_survey_instances[random_id])[0] + "FAKE"
        )
        with pytest.raises(CastorException) as e:
            client.single_survey_data_points_record(
                random_id, random_survey
            )
        assert str(e.value) == "404 Survey Package Instance not found"

    # POST
    def test_create_study_data_points_success(self, client, all_record_ids):
        random_record = random.choice(all_record_ids)
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API", "confirmed_changes": True}
        data = [
            {
                "field_id": field.field_id,
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in random_fields
        ]
        feedback = client.update_study_data_record(random_record, common, data)
        assert feedback["total_processed"] == 5
        # Assert that not everything failed, indication that it worked
        assert feedback["total_failed"] == 0

    def test_create_study_data_points_fail_ids(self, client, all_record_ids):
        random_record = random.choice(all_record_ids)
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API", "confirmed_changes": True}
        data = [
            {
                "field_id": field.field_id + "FAKE",
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in random_fields
        ]
        feedback = client.update_study_data_record(random_record, common, data)
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 5

    def test_create_study_data_points_fail_record(self, client, all_record_ids):
        random_record = random.choice(all_record_ids) + "FAKE"
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API", "confirmed_changes": True}
        data = [
            {
                "field_id": field.field_id,
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in random_fields
        ]
        with pytest.raises(CastorException) as e:
            client.update_study_data_record(random_record, common, data)
        assert str(e.value) == "404 Record not found"

    def test_create_report_data_points_success(self, client, records_with_reports):
        # Find a random record with a random report instance
        fields = []

        # Some reports do not have filled in fields, so keep searching until report with fields is found.
        while len(fields) == 0:
            random_record = random.choice(list(records_with_reports.keys()))
            rand_report_instance = random.choice(records_with_reports[random_record])
            # Find the parent report of the instance
            report = client.single_report_instance(rand_report_instance)
            report_id = report["_embedded"]["report"]["id"]
            # Find the fields belonging to the report
            fields = [
                field
                for field in client.field_references["reports"]
                if field.parent_id == report_id
            ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field.field_id,
                "instance_id": rand_report_instance,
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        feedback = client.update_report_data_record(
            random_record, rand_report_instance, common, data
        )
        assert feedback["total_processed"] == len(fields)
        assert feedback["total_failed"] == 0

    def test_create_report_data_points_fail_ids(self, client, records_with_reports):
        fields = []

        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random report instance
            random_record = random.choice(list(records_with_reports.keys()))
            rand_report_instance = random.choice(records_with_reports[random_record])
            # Find the parent report of the instance
            report = client.single_report_instance(rand_report_instance)
            report_id = report["_embedded"]["report"]["id"]
            # Find the fields belonging to the report
            fields = [
                field
                for field in client.field_references["reports"]
                if field.parent_id == report_id
            ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field.field_id + "FAKE",
                "instance_id": rand_report_instance,
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        feedback = client.update_report_data_record(
            random_record, rand_report_instance, common, data
        )
        assert feedback["total_processed"] == len(fields)
        # Assert that everything failed, indication that it worked
        assert feedback["total_failed"] == len(fields)

    def test_create_report_data_points_fail_record(self, client, records_with_reports):
        fields = []

        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random report instance
            random_record = random.choice(list(records_with_reports.keys()))
            rand_report_instance = random.choice(records_with_reports[random_record])
            # Find the parent report of the instance
            report = client.single_report_instance(rand_report_instance)
            report_id = report["_embedded"]["report"]["id"]
            # Find the fields belonging to the report
            fields = [
                field
                for field in client.field_references["reports"]
                if field.parent_id == report_id
            ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field.field_id,
                "instance_id": rand_report_instance,
                "field_value": allowed_value(client, field.field_id),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        with pytest.raises(CastorException) as e:
            client.update_report_data_record(
                random_record + "FAKE", rand_report_instance, common, data
            )
        assert str(e.value) == "404 Record not found"
        # TODO: Test that nothing changed in the database

    def test_create_survey_instance_data_points_success(
            self, client, records_with_survey_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(list(records_with_survey_instances.keys()))
            random_survey_instance, random_name = random.choice(
                records_with_survey_instances[random_record]
            )

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id,
                "instance_id": random_survey_instance,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_instance_data_record(
            random_record, random_survey_instance, data
        )
        assert feedback["total_processed"] == len(fields)
        assert feedback["total_failed"] == 0

    def test_create_survey_instance_data_points_fail_ids(
            self, client, records_with_survey_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(list(records_with_survey_instances.keys()))
            random_survey_instance, random_name = random.choice(
                records_with_survey_instances[random_record]
            )

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id + "FAKE",
                "instance_id": random_survey_instance,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_instance_data_record(
            random_record, random_survey_instance, data
        )
        assert feedback["total_processed"] == len(fields)
        assert feedback["total_failed"] == len(fields)

    def test_create_survey_instance_data_points_fail_record(
            self, client, records_with_survey_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(list(records_with_survey_instances.keys()))
            random_survey_instance, random_name = random.choice(
                records_with_survey_instances[random_record]
            )

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id,
                "instance_id": random_survey_instance,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        with pytest.raises(CastorException) as e:
            client.update_survey_instance_data_record(
                random_record + "FAKE", random_survey_instance, data
            )
        assert str(e.value) == "404 Record not found"

    def test_create_survey_package_instance_data_points_success(
            self, client, records_with_survey_package_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(
                list(records_with_survey_package_instances.keys())
            )
            random_package_id = random.choice(
                records_with_survey_package_instances[random_record]
            )
            random_package = client.single_survey_package_instance(random_package_id)
            contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"][
                "surveys"
            ]
            random_survey_name = random.choice(contained_surveys)["name"]

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_survey_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id,
                "instance_id": random_package_id,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(
            random_record, random_package_id, data
        )

        assert feedback["total_processed"] == len(fields)
        assert feedback["total_failed"] == 0

    def test_create_survey_package_instance_data_points_fail_ids(
            self, client, records_with_survey_package_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(
                list(records_with_survey_package_instances.keys())
            )
            random_package_id = random.choice(
                records_with_survey_package_instances[random_record]
            )
            random_package = client.single_survey_package_instance(random_package_id)
            contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"][
                "surveys"
            ]
            random_survey_name = random.choice(contained_surveys)["name"]

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_survey_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id + "FAKE",
                "instance_id": random_package_id,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        with pytest.raises(CastorException) as e:
            client.update_survey_package_instance_data_record(
                random_record, random_package_id, data
            )
        assert str(e.value) == "500 The application has encountered an error"

    def test_create_survey_package_instance_data_points_fail_records(
            self, client, records_with_survey_package_instances
    ):
        fields = []
        # Keep looking for a report until one with fields is found
        while len(fields) == 0:
            # Find a random record with a random survey instance
            random_record = random.choice(
                list(records_with_survey_package_instances.keys())
            )
            random_package_id = random.choice(
                records_with_survey_package_instances[random_record]
            )
            random_package = client.single_survey_package_instance(random_package_id)
            contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"][
                "surveys"
            ]
            random_survey_name = random.choice(contained_surveys)["name"]

            # Find the fields belonging to the survey
            fields = [
                field
                for field in client.field_references["surveys"]
                if field.survey_name == random_survey_name
            ]

        # Instantiate fake data
        data = [
            {
                "field_id": field.field_id,
                "instance_id": random_package_id,
                "field_value": allowed_value(client, field.field_id),
            }
            for field in fields
        ]

        # Update the survey
        with pytest.raises(CastorException) as e:
            client.update_survey_package_instance_data_record(
                random_record + "FAKE", random_package_id, data
            )
        assert str(e.value) == "404 Record not found"
