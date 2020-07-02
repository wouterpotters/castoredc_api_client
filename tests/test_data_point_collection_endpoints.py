# -*- coding: utf-8 -*-
"""
Testing class for data-point-collection endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/data-point-collection

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestDataPoint:
    study_data_point_model = {
        "field_id": "string",
        "field_value": "string",
        "record_id": "string",
        "updated_on": "int",
    }
    study_data_point_model_keys = study_data_point_model.keys()

    report_data_point_model = {
        "field_id": "string",
        "report_instance_id": "string",
        "report_instance_name": "string",
        "field_value": "string",
        "record_id": "string",
        "updated_on": "string"
    }
    report_data_point_model_keys = report_data_point_model.keys()

    survey_data_point_model = {
        "field_id": "string",
        "survey_instance_id": "string",
        "survey_name": "string",
        "field_value": "string",
        "record_id": "string",
        "updated_on": "string",
        # "survey_package_id": "string",
    }
    survey_data_point_model_keys = survey_data_point_model.keys()

    # NON RECORD SPECIFIC DATA
    @pytest.fixture(scope="class")
    def all_study_data_points(self, client):
        all_study_data_points = client.all_study_data_points()
        return all_study_data_points

    def test_all_study_data_points(self, all_study_data_points, item_totals):
        assert len(all_study_data_points) > 0
        assert len(all_study_data_points) == \
               item_totals["total_study_data_points"]

    def test_all_data_points_model(self, all_study_data_points):
        for i in range(0, 5):
            rand_data_point = random.choice(all_study_data_points)
            api_keys = rand_data_point.keys()
            assert len(self.study_data_point_model_keys) == len(api_keys)
            for key in self.study_data_point_model_keys:
                assert key in api_keys

    def test_all_report_data_points(self, all_report_data_points, item_totals):
        assert len(all_report_data_points) > 0
        assert len(all_report_data_points) == \
               item_totals["total_report_data_points"]

    def test_all_report_data_points_model(self, all_report_data_points):
        for i in range(0, 5):
            rand_data_point = random.choice(all_report_data_points)
            api_keys = rand_data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in self.report_data_point_model_keys:
                assert key in api_keys

    def test_single_report_instance_data_points_success(self,
                                                        client,
                                                        all_report_data_points):
        for i in range(0, 3):
            random_report = random.choice(all_report_data_points)
            rand_id = random_report["report_instance_id"]
            api_report = client.single_report_instance_data_points(rand_id)
            assert api_report is not None
            assert len(api_report) > 0
            for data_point in api_report:
                api_keys = data_point.keys()
                for key in self.report_data_point_model_keys:
                    assert key in api_keys

    def test_single_report_instance_data_points_fail(self,
                                                     client,
                                                     all_report_data_points):
        for i in range(0, 3):
            random_report = random.choice(all_report_data_points)
            rand_id = random_report["report_instance_id"] + "FAKE"
            api_report = client.single_report_instance_data_points(rand_id)
            assert api_report is None

    @pytest.fixture(scope="class")
    def all_survey_data_points(self, client):
        all_survey_data_points = client.all_survey_data_points()
        return all_survey_data_points

    def test_all_survey_data_points(self, all_survey_data_points, item_totals):
        assert len(all_survey_data_points) > 0
        assert len(all_survey_data_points) == \
               item_totals["total_survey_data_points"]

    def test_all_survey_data_points_model(self, all_survey_data_points):
        for i in range(0, 3):
            rand_data_point = random.choice(all_survey_data_points)
            api_keys = rand_data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys

    def test_single_survey_instance_data_points_success(self,
                                                        client,
                                                        all_survey_data_points):
        for i in range(0, 3):
            random_survey = random.choice(all_survey_data_points)
            rand_id = random_survey["survey_instance_id"]
            api_survey = client.single_survey_instance_data_points(rand_id)
            assert api_survey is not None
            assert len(api_survey) > 0
            for data_point in api_survey:
                api_keys = data_point.keys()
                for key in self.survey_data_point_model_keys:
                    assert key in api_keys

    def test_single_survey_instance_data_points_fail(self,
                                                     client,
                                                     all_survey_data_points):
        for i in range(0, 5):
            random_survey = random.choice(all_survey_data_points)
            rand_id = random_survey["survey_instance_id"] + "FAKE"
            api_survey = client.single_survey_instance_data_points(rand_id)
            assert api_survey is None

    @pytest.fixture(scope="class")
    def all_survey_package_instance_ids(self, client):
        all_survey_package_instance = client.all_survey_package_instances()
        all_survey_package_instance_ids = \
            [package["survey_package_instance_id"]
             for package
             in all_survey_package_instance]
        return all_survey_package_instance_ids

    def test_single_survey_package_instance_data_points_success(self,
                                                                client,
                                                                all_survey_package_instance_ids):
        # TODO: Only select package instances that are filled in
        # Now all package instances are tested, and most dont have data points
        for i in range(0, 3):
            rand_id = random.choice(all_survey_package_instance_ids)
            api_package = client.single_survey_package_instance_data_points(rand_id)
            assert api_package is not None
            for data_point in api_package:
                api_keys = data_point.keys()
                for key in self.survey_data_point_model_keys:
                    assert key in api_keys

    def test_single_survey_package_instance_data_points_fail(self,
                                                             client,
                                                             all_survey_package_instance_ids):
        for i in range(0, 3):
            rand_id = random.choice(all_survey_package_instance_ids) + "FAKE"
            api_package = client.single_survey_package_instance_data_points(rand_id)
            assert api_package is None

    # ALL DATA - RECORD SPECIFIC
    def test_all_study_data_points_record_success(self, client, all_record_ids):
        for i in range(0, 3):
            # TODO: Only select records that have data
            # Now all records are tested, and most dont have data points
            random_id = random.choice(all_record_ids)
            all_data = client.all_study_data_points_record(random_id)
            assert all_data is not None
            for data_point in all_data:
                api_keys = data_point.keys()
                assert len(self.study_data_point_model_keys) == len(api_keys)
                for key in self.study_data_point_model_keys:
                    assert key in api_keys

    def test_all_study_data_points_record_fail(self, client, all_record_ids):
        for i in range(0, 3):
            random_id = random.choice(all_record_ids) + "FAKE"
            all_data = client.all_study_data_points_record(random_id)
            assert all_data is None

    def test_all_report_data_points_record_success(self, client, all_record_ids):
        for i in range(0, 3):
            # TODO: Only select records that have data
            # Now all records are tested, and most dont have data points
            random_id = random.choice(all_record_ids)
            all_data = client.all_report_data_points_record(random_id)
            assert all_data is not None
            for data_point in all_data:
                api_keys = data_point.keys()
                assert len(self.report_data_point_model_keys) == len(api_keys)
                for key in self.report_data_point_model_keys:
                    assert key in api_keys

    def test_all_report_data_points_record_fail(self, client, all_record_ids):
        for i in range(0, 3):
            random_id = random.choice(all_record_ids) + "FAKE"
            all_data = client.all_report_data_points_record(random_id)
            assert all_data is None

    def test_all_survey_data_points_record_success(self, client, all_record_ids):
        for i in range(0, 3):
            # TODO: Only select records that have data
            # Now all records are tested, and most dont have data points
            random_id = random.choice(all_record_ids)
            all_data = client.all_survey_data_points_record(random_id)
            assert all_data is not None
            for data_point in all_data:
                api_keys = data_point.keys()
                assert len(self.survey_data_point_model_keys) == len(api_keys)
                for key in self.survey_data_point_model_keys:
                    assert key in api_keys

    def test_all_survey_data_points_record_fail(self, client, all_record_ids):
        for i in range(0, 3):
            random_id = random.choice(all_record_ids) + "FAKE"
            all_data = client.all_survey_data_points_record(random_id)
            assert all_data is None

    # SINGLE SURVEY/REPORT - RECORD SPECIFIC
    def test_single_report_data_points_record_success(self,
                                                      client,
                                                      records_with_reports):
        # TODO: Only select records that have data
        # Now all records are tested, and most dont have data points
        for i in range(0, 3):
            records = list(records_with_reports.keys())
            random_id = random.choice(records)
            random_report = random.choice(records_with_reports[random_id])
            report_data = client.single_report_data_points_record(random_id,
                                                                  random_report)
            assert report_data is not None
            for data_point in report_data:
                api_keys = data_point.keys()
                assert len(self.report_data_point_model_keys) == len(api_keys)
                for key in self.report_data_point_model_keys:
                    assert key in api_keys

    def test_single_report_data_points_record_fail(self,
                                                   client,
                                                   records_with_reports):
        for i in range(0, 3):
            records = list(records_with_reports.keys())
            random_id = random.choice(records)
            random_report = (random.choice(records_with_reports[random_id])
                             + "FAKE")
            report_data = client.single_report_data_points_record(random_id,
                                                                  random_report)
            assert report_data is None

    # TODO: Sometimes returns a dict of 7 values, sometimes 6..??
    def test_single_survey_package_data_points_record_success(self,
                                                              client,
                                                              records_with_survey_package_instances):
        # TODO: Only select records that have data
        # Now all records are tested, and most dont have data points
        for i in range(0, 3):
            records = list(records_with_survey_package_instances.keys())
            random_id = random.choice(records)
            random_package = random.choice(records_with_survey_package_instances[random_id])
            survey_data = client.single_survey_package_data_points_record(random_id,
                                                                          random_package)
            assert survey_data is not None
            for data_point in survey_data:
                api_keys = data_point.keys()
                assert (len(self.survey_data_point_model_keys) == len(api_keys)
                        or len(
                            api_keys) == 7), "length is 6 or 7 in api. Does not always contain 'survey_package_id'"
                for key in self.survey_data_point_model_keys:
                    assert key in api_keys

    def test_single_survey_package_data_points_record_fail(self,
                                                           client,
                                                           records_with_survey_package_instances):
        for i in range(0, 3):
            records = list(records_with_survey_package_instances.keys())
            random_id = random.choice(records)
            random_package = (random.choice(records_with_survey_package_instances[random_id])
                              + "FAKE")
            survey_data = client.single_survey_package_data_points_record(random_id,
                                                                          random_package)
            assert survey_data is None

    def test_single_survey_data_points_record_success(self,
                                                      client,
                                                      records_with_survey_instances):
        # TODO: Only select records that have data
        # Now all records are tested, and most dont have data points
        for i in range(0, 3):
            records = list(records_with_survey_instances.keys())
            random_id = random.choice(records)
            random_survey = random.choice(records_with_survey_instances[random_id])[0]
            survey_data = client.single_survey_data_points_record(random_id,
                                                                  random_survey)
            assert survey_data is not None
            for data_point in survey_data:
                api_keys = data_point.keys()
                assert len(self.survey_data_point_model_keys) == len(api_keys)
                for key in self.survey_data_point_model_keys:
                    assert key in api_keys

    def test_single_survey_data_points_record_fail(self,
                                                   client,
                                                   records_with_survey_instances):
        for i in range(0, 3):
            records = list(records_with_survey_instances.keys())
            random_id = random.choice(records)
            random_survey = (random.choice(records_with_survey_instances[random_id])[0]
                             + "FAKE")
            survey_data = client.single_survey_data_points_record(random_id,
                                                                  random_survey)
            assert survey_data is None

    # POST
    def test_create_study_data_points_success(self,
                                              client,
                                              all_record_ids):
        random_record = random.choice(all_record_ids)
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}
        data = [{"field_id": field.field_id,
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in random_fields]
        feedback = client.update_study_data_record(random_record, common, data)
        assert feedback is not None
        assert feedback["total_processed"] == 5
        # Assert that not everything failed, indication that it worked
        # TODO: make sure only valid values are entered
        assert feedback["total_failed"] < 5
        # TODO: Test that things truly changed in database (according to audit
        # log they did)

    def test_create_study_data_points_fail_ids(self,
                                               client,
                                               all_record_ids):
        random_record = random.choice(all_record_ids)
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}
        data = [{"field_id": field.field_id + "FAKE",
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in random_fields]
        feedback = client.update_study_data_record(random_record, common, data)
        assert feedback is not None
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 5
        # TODO: Test that things truly did not change changed in database 
        # according to audit log they did not

    def test_create_study_data_points_fail_record(self,
                                                  client,
                                                  all_record_ids):
        random_record = random.choice(all_record_ids) + "FAKE"
        random_fields = random.choices(client.field_references["study"], k=5)
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}
        data = [{"field_id": field.field_id,
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in random_fields]
        feedback = client.update_study_data_record(random_record, common, data)
        assert feedback is None
        # TODO: Test that things truly did not change changed in database 
        # according to audit log they did not

    def test_create_report_data_points_success(self,
                                               client,
                                               records_with_reports):
        # Find a random record with a random report instance
        random_record = random.choice(list(records_with_reports.keys()))
        rand_report_instance = random.choice(records_with_reports[random_record])
        # Find the parent report of the instance
        report = client.single_report_instance(rand_report_instance)
        report_id = report["_embedded"]["report"]["id"]
        # Find the fields belonging to the repot
        fields = [field
                  for field
                  in client.field_references["reports"]
                  if field.parent_id == report_id]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}

        data = [{"field_id": field.field_id,
                 "instance_id": rand_report_instance,
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in fields]

        # Update the report
        feedback = client.update_report_data_record(random_record,
                                                    rand_report_instance,
                                                    common,
                                                    data)
        assert feedback is not None
        assert feedback["total_processed"] == len(fields)
        # Assert that not everything failed, indication that it worked
        # TODO: make sure only valid values are entered
        assert feedback["total_failed"] < len(fields)
        # TODO: Test that things truly changed in database (according to audit
        # log they did)

    def test_create_report_data_points_fail_ids(self,
                                                client,
                                                records_with_reports):
        # Find a random record with a random report instance
        random_record = random.choice(list(records_with_reports.keys()))
        rand_report_instance = random.choice(records_with_reports[random_record])
        # Find the parent report of the instance
        report = client.single_report_instance(rand_report_instance)
        report_id = report["_embedded"]["report"]["id"]
        # Find the fields belonging to the repot
        fields = [field
                  for field
                  in client.field_references["reports"]
                  if field.parent_id == report_id]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}

        data = [{"field_id": field.field_id + "FAKE",
                 "instance_id": rand_report_instance,
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in fields]

        # Update the report
        feedback = client.update_report_data_record(random_record,
                                                    rand_report_instance,
                                                    common,
                                                    data)
        assert feedback is not None
        assert feedback["total_processed"] == len(fields)
        # Assert that everything failed, indication that it worked
        assert feedback["total_failed"] == len(fields)
        # TODO: Test that nothing changed in the database

    def test_create_report_data_points_fail_record(self,
                                                   client,
                                                   records_with_reports):
        # Find a random record with a random report instance
        random_record = random.choice(list(records_with_reports.keys()))
        rand_report_instance = random.choice(records_with_reports[random_record])
        # Find the parent report of the instance
        report = client.single_report_instance(rand_report_instance)
        report_id = report["_embedded"]["report"]["id"]
        # Find the fields belonging to the repot
        fields = [field
                  for field
                  in client.field_references["reports"]
                  if field.parent_id == report_id]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        common = {"change_reason": "Testing API",
                  "confirmed_changes": True}

        data = [{"field_id": field.field_id,
                 "instance_id": rand_report_instance,
                 "field_value": 1,
                 "change_reason": "Testing API",
                 "confirmed_changes": True}
                for field in fields]

        # Update the report
        feedback = client.update_report_data_record(random_record + "FAKE",
                                                    rand_report_instance,
                                                    common,
                                                    data)
        assert feedback is None
        # TODO: Test that nothing changed in the database

    def test_create_survey_instance_data_points_success(self,
                                                        client,
                                                        records_with_survey_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_instances.keys()))
        random_survey_instance, random_name = random.choice(records_with_survey_instances[random_record])

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id,
                 "instance_id": random_survey_instance,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_instance_data_record(random_record,
                                                             random_survey_instance,
                                                             data)
        assert feedback is not None
        assert feedback["total_processed"] == len(fields)
        # Assert that not everything failed, indication that it worked
        # TODO: make sure only valid values are entered
        assert feedback["total_failed"] < len(fields)
        # TODO: Test that things truly changed in database (according to audit
        # log they did)

    def test_create_survey_instance_data_points_fail_ids(self,
                                                         client,
                                                         records_with_survey_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_instances.keys()))
        random_survey_instance, random_name = random.choice(records_with_survey_instances[random_record])

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id + "FAKE",
                 "instance_id": random_survey_instance,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_instance_data_record(random_record,
                                                             random_survey_instance,
                                                             data)
        assert feedback is not None
        assert feedback["total_processed"] == len(fields)
        # Assert that  everything failed
        assert feedback["total_failed"] == len(fields)
        # TODO: Test that things did not change

    def test_create_survey_instance_data_points_fail_record(self,
                                                            client,
                                                            records_with_survey_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_instances.keys()))
        random_survey_instance, random_name = random.choice(records_with_survey_instances[random_record])

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id,
                 "instance_id": random_survey_instance,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_instance_data_record(random_record + "FAKE",
                                                             random_survey_instance,
                                                             data)
        assert feedback is None
        # TODO: Test that things did not change in database

    def test_create_survey_package_instance_data_points_success(self,
                                                                client,
                                                                records_with_survey_package_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_package_instances.keys()))
        random_package_id = random.choice(records_with_survey_package_instances[random_record])
        random_package = client.single_survey_package_instance(random_package_id)
        contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"]["surveys"]
        random_survey_name = random.choice(contained_surveys)["name"]

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_survey_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id,
                 "instance_id": random_package_id,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(random_record,
                                                                     random_package_id,
                                                                     data)
        assert feedback is not None
        assert feedback["total_processed"] == len(fields)
        # Assert that not everything failed, indication that it worked
        # TODO: make sure only valid values are entered
        assert feedback["total_failed"] < len(fields)
        # TODO: Test that things truly changed in database (according to audit
        # log they did)

    def test_create_survey_package_instance_data_points_fail_ids(self,
                                                                 client,
                                                                 records_with_survey_package_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_package_instances.keys()))
        random_package_id = random.choice(records_with_survey_package_instances[random_record])
        random_package = client.single_survey_package_instance(random_package_id)
        contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"]["surveys"]
        random_survey_name = random.choice(contained_surveys)["name"]

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_survey_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id + "FAKE",
                 "instance_id": random_package_id,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(random_record,
                                                                     random_package_id,
                                                                     data)
        assert feedback is None
        # TODO: It seems like this one fails with a server error when supplying
        # wrong field ids, while the other tests return an error message

    def test_create_survey_package_instance_data_points_fail_records(self,
                                                                     client,
                                                                     records_with_survey_package_instances):
        # Find a random record with a random survey instance
        random_record = random.choice(list(records_with_survey_package_instances.keys()))
        random_package_id = random.choice(records_with_survey_package_instances[random_record])
        random_package = client.single_survey_package_instance(random_package_id)
        contained_surveys = random_package["_embedded"]["survey_package"]["_embedded"]["surveys"]
        random_survey_name = random.choice(contained_surveys)["name"]

        # Find the fields belonging to the survey
        fields = [field
                  for field
                  in client.field_references["surveys"]
                  if field.survey_name == random_survey_name]

        # Check if the report fields are found
        assert len(fields) > 0

        # Instantiate fake data
        data = [{"field_id": field.field_id,
                 "instance_id": random_package_id,
                 "field_value": 1}
                for field in fields]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(random_record + "FAKE",
                                                                     random_package_id,
                                                                     data)
        assert feedback is None
