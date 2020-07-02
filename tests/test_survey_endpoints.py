# -*- coding: utf-8 -*-
"""
Testing class for survey endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


def create_survey_package_instance(client, record_id, fake):
    # TODO: make tests more complex with adding different parameters
    # for the parameters that are now None or different type of fakes
    survey_package = client.all_survey_packages()
    package_ids = [package["id"] for package in survey_package]
    random_package = random.choice(package_ids)

    if fake:
        random_package += "FAKE"

    return {"survey_package_id": random_package,
            "record_id": record_id,
            "ccr_patient_id": None,
            "email_address": "clearlyfakemail@itsascam.com",
            "package_invitation_subject": None,
            "package_invitation": None,
            "auto_send": None,
            "auto_lock_on_finish": None
            }


class TestSurveyEndpoints:
    survey_model = {
        "id": "string",
        "survey_id": "string",
        "name": "string",
        "description": "string",
        "intro_text": "string",
        "outro_text": "string",
        "survey_steps": "list",
        "_links": "dict",
    }

    s_model_keys = survey_model.keys()

    package_model = {
        "id": "string",
        "survey_package_id": "string",
        "name": "string",
        "description": "string",
        "intro_text": "string",
        "outro_text": "string",
        "sender_name": "string",
        "sender_email": "string",
        "auto_send": "boolean",
        "allow_step_navigation": "boolean",
        "show_step_navigator": "boolean",
        "finish_url": "string",
        "auto_lock_on_finish": "boolean",
        "default_invitation": "string",
        "default_invitation_subject": "string",
        "_embedded": "dict",
        "_links": "dict",
    }

    p_model_keys = package_model.keys()

    instance_model = {
        "id": "string",
        "survey_package_instance_id": "string",
        "record_id": "string",
        "institute_id": "string",
        "institute_name": "string",
        "survey_package_id": "string",
        "survey_package_name": "string",
        "invitation_subject": "string",
        "invitation_content": "string",
        "created_on": "dict",
        "created_by": "string",
        "sent_on": "dict",
        "first_opened_on": "dict",
        "finished_on": "dict",
        "locked": "boolean",
        "archived": "boolean",
        "survey_url_string": "string",
        "progress": "int",
        "auto_lock_on_finish": "boolean",
        "auto_send": "boolean",
        "_embedded": {
            "record": "dict",
            # Contains info on the record
            "institute": "dict",
            # Contains info on the institute
            "survey_package": "dict"
            # Contains info on the survey package and on thesurveys
        },
        "_links": "dict",
    }

    i_model_keys = instance_model.keys()

    @pytest.fixture
    def all_surveys(self, client):
        all_surveys = client.all_surveys()
        return all_surveys

    @pytest.fixture
    def all_survey_packages(self, client):
        all_survey_packages = client.all_survey_packages()
        return all_survey_packages

    @pytest.fixture
    def all_survey_package_instances(self, client):
        all_survey_package_instances = client.all_survey_package_instances()
        return all_survey_package_instances

        # SURVEYS

    def test_all_surveys(self, all_surveys):
        for i in range(0, 3):
            random_survey = random.choice(all_surveys)
            survey_keys = random_survey.keys()
            assert len(survey_keys) == len(self.s_model_keys)
            for key in survey_keys:
                assert key in self.s_model_keys

    def test_single_survey_success(self, client, all_surveys):
        for i in range(0, 3):
            random_id = random.choice(all_surveys)["id"]
            random_survey = client.single_survey(random_id)
            assert random_survey is not None
            survey_keys = random_survey.keys()
            assert len(survey_keys) == len(self.s_model_keys)
            for key in survey_keys:
                assert key in self.s_model_keys

    def test_single_survey_fail(self, client, all_surveys):
        for i in range(0, 3):
            random_id = random.choice(all_surveys)["id"] + "FAKE"
            random_survey = client.single_survey(random_id)
            assert random_survey is None

    # SURVEY PACKAGES
    def test_all_survey_packages(self, all_survey_packages):
        for i in range(0, 3):
            random_package = random.choice(all_survey_packages)
            package_keys = random_package.keys()
            assert len(package_keys) == len(self.p_model_keys)
            for key in package_keys:
                assert key in self.p_model_keys

    def test_single_survey_package_success(self, client, all_survey_packages):
        for i in range(0, 3):
            random_id = random.choice(all_survey_packages)["id"]
            random_package = client.single_survey_package(random_id)
            assert random_package is not None
            package_keys = random_package.keys()
            assert len(package_keys) == len(self.p_model_keys)
            for key in package_keys:
                assert key in self.p_model_keys

    def test_single_survey_package_fail(self, client, all_survey_packages):
        for i in range(0, 3):
            random_id = random.choice(all_survey_packages)["id"] + "FAKE"
            random_package = client.single_survey_package(random_id)
            assert random_package is None

    # SURVEY PACKAGE INSTANCES
    def test_all_survey_package_instances(self,
                                          all_survey_package_instances):
        for i in range(0, 3):
            random_instance = random.choice(all_survey_package_instances)
            instance_keys = random_instance.keys()
            assert len(instance_keys) == len(self.i_model_keys)
            for key in instance_keys:
                assert key in self.i_model_keys

    def test_all_survey_package_instance_record_success(self,
                                                        client,
                                                        all_survey_package_instances):
        for i in range(0, 3):
            random_instance = random.choice(all_survey_package_instances)
            random_record = random_instance["record_id"]
            instances = client.all_survey_package_instances(record=random_record)
            assert instances is not None
            assert len(instances) > 0
            for instance in instances:
                assert instance["record_id"] == random_record
                instance_keys = instance.keys()
                assert len(instance_keys) == len(self.i_model_keys)
                for key in instance_keys:
                    assert key in self.i_model_keys

    def test_all_survey_package_instance_record_fail(self,
                                                     client,
                                                     all_survey_package_instances):
        for i in range(0, 3):
            random_instance = random.choice(all_survey_package_instances)
            random_record = random_instance["record_id"] + "FAKE"
            instances = client.all_survey_package_instances(record=random_record)
            assert instances is None

    def test_single_survey_package_instance_success(self,
                                                    client,
                                                    all_survey_package_instances):
        for i in range(0, 3):
            random_id = random.choice(all_survey_package_instances)["id"]
            random_instance = client.single_survey_package_instance(random_id)
            assert random_instance is not None
            instance_keys = random_instance.keys()
            assert len(instance_keys) == len(self.i_model_keys)
            for key in instance_keys:
                assert key in self.i_model_keys

    def test_single_survey_package_instance_fail(self,
                                                 client,
                                                 all_survey_package_instances):
        for i in range(0, 3):
            random_id = random.choice(all_survey_package_instances)["id"] + "FAKE"
            random_instance = client.single_survey_package_instance(random_id)
            assert random_instance is None

    # POST
    def test_create_survey_package_instance_success(self, client):
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]
        body = create_survey_package_instance(client, random_record, fake=False)
        old_amount = len(client.all_survey_package_instances(record=random_record))

        feedback = client.create_survey_package_instance(**body)

        new_amount = len(client.all_survey_package_instances(record=random_record))

        assert feedback is not None
        assert feedback["record_id"] == random_record
        assert new_amount == old_amount + 1

    def test_create_survey_package_instance_fail(self, client):
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]
        body = create_survey_package_instance(client, random_record, fake=True)
        old_amount = len(client.all_survey_package_instances(record=random_record))

        feedback = client.create_survey_package_instance(**body)

        new_amount = len(client.all_survey_package_instances(record=random_record))

        assert feedback is None
        assert new_amount == old_amount

    def test_patch_survey_package_instance_success(self,
                                                   client,
                                                   all_survey_package_instances):
        random_instance = random.choice(all_survey_package_instances)["id"]
        for i in range(0, 3):
            package = client.single_survey_package_instance(random_instance)
            old_status = package["locked"]
            target_status = not old_status
            feedback = client.patch_survey_package_instance(random_instance,
                                                            target_status)
            package = client.single_survey_package_instance(random_instance)
            new_status = package["locked"]
            assert feedback is not None
            assert new_status is not old_status

    def test_patch_survey_package_instance_failure(self,
                                                   client,
                                                   all_survey_package_instances):
        random_instance = random.choice(all_survey_package_instances)["id"]
        for i in range(0, 3):
            package = client.single_survey_package_instance(random_instance)
            old_status = package["locked"]
            target_status = not old_status
            fake_id = random_instance + "FAKE"
            feedback = client.patch_survey_package_instance(fake_id,
                                                            target_status)
            package = client.single_survey_package_instance(random_instance)
            new_status = package["locked"]
            assert feedback is None
            assert new_status is old_status
