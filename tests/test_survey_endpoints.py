# -*- coding: utf-8 -*-
"""
Testing class for survey endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.exceptions import CastorException
from tests.data_models import survey_model, package_model, survey_package_instance_model


def create_survey_package_instance(client, record_id, fake):
    survey_package = client.all_survey_packages()
    package_ids = [package["id"] for package in survey_package]
    random_package = random.choice(package_ids)

    if fake:
        random_package += "FAKE"

    return {
        "survey_package_id": random_package,
        "record_id": record_id,
        "ccr_patient_id": None,
        "email_address": "clearlyfakemail@itsascam.com",
        "package_invitation_subject": None,
        "package_invitation": None,
        "auto_send": None,
        "auto_lock_on_finish": None,
    }


class TestSurveyEndpoints:
    s_model_keys = survey_model.keys()
    p_model_keys = package_model.keys()
    i_model_keys = survey_package_instance_model.keys()

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
        random_survey = random.choice(all_surveys)
        survey_keys = random_survey.keys()
        assert len(survey_keys) == len(self.s_model_keys)
        for key in survey_keys:
            assert key in self.s_model_keys
            assert type(random_survey[key]) in survey_model[key]

    def test_single_survey_success(self, client, all_surveys):
        random_survey = client.single_survey(random.choice(all_surveys)["id"])
        survey_keys = random_survey.keys()
        assert len(survey_keys) == len(self.s_model_keys)
        for key in survey_keys:
            assert key in self.s_model_keys
            assert type(random_survey[key]) in survey_model[key]

    def test_single_survey_fail(self, client, all_surveys):
        with pytest.raises(CastorException) as e:
            client.single_survey(random.choice(all_surveys)["id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."

    # SURVEY PACKAGES
    def test_all_survey_packages(self, all_survey_packages):
        random_package = random.choice(all_survey_packages)
        package_keys = random_package.keys()
        assert len(package_keys) == len(self.p_model_keys)
        for key in package_keys:
            assert key in self.p_model_keys
            assert type(random_package[key]) in package_model[key]

    def test_single_survey_package_success(self, client, all_survey_packages):
        random_package = client.single_survey_package(
            random.choice(all_survey_packages)["id"]
        )
        package_keys = random_package.keys()
        assert len(package_keys) == len(self.p_model_keys)
        for key in package_keys:
            assert key in self.p_model_keys
            assert type(random_package[key]) in package_model[key]

    def test_single_survey_package_fail(self, client, all_survey_packages):
        with pytest.raises(CastorException) as e:
            client.single_survey_package(
                random.choice(all_survey_packages)["id"] + "FAKE"
            )
        assert str(e.value) == "404 Entity not found."

    # SURVEY PACKAGE INSTANCES
    def test_all_survey_package_instances(self, all_survey_package_instances):
        random_instance = random.choice(all_survey_package_instances)
        instance_keys = random_instance.keys()
        assert len(instance_keys) == len(self.i_model_keys)
        for key in instance_keys:
            assert key in self.i_model_keys
            assert type(random_instance[key]) in survey_package_instance_model[key]

    def test_all_survey_package_instance_record_success(
        self, client, all_survey_package_instances
    ):
        random_instance = random.choice(all_survey_package_instances)
        random_record = random_instance["record_id"]
        instances = client.all_survey_package_instances(record=random_record)

        for instance in instances:
            assert instance["record_id"] == random_record
            instance_keys = instance.keys()
            assert len(instance_keys) == len(self.i_model_keys)
            for key in instance_keys:
                assert key in self.i_model_keys
                assert type(random_instance[key]) in survey_package_instance_model[key]

    def test_all_survey_package_instance_record_fail(
        self, client, all_survey_package_instances
    ):
        random_record = (
            random.choice(all_survey_package_instances)["record_id"] + "FAKE"
        )
        with pytest.raises(CastorException) as e:
            client.all_survey_package_instances(record=random_record)
        assert str(e.value) == "404 Not found."

    def test_single_survey_package_instance_success(
        self, client, all_survey_package_instances
    ):
        random_id = random.choice(all_survey_package_instances)["id"]
        random_instance = client.single_survey_package_instance(random_id)
        instance_keys = random_instance.keys()
        assert len(instance_keys) == len(self.i_model_keys)
        for key in instance_keys:
            assert key in self.i_model_keys
            assert type(random_instance[key]) in survey_package_instance_model[key]

    def test_single_survey_package_instance_fail(
        self, client, all_survey_package_instances
    ):
        with pytest.raises(CastorException) as e:
            client.single_survey_package_instance(
                random.choice(all_survey_package_instances)["id"] + "FAKE"
            )
        assert str(e.value) == "404 Survey package invitation not found"

    # POST
    def test_create_survey_package_instance_success(self, client):
        random_record = random.choice(client.all_records(archived=0))["id"]
        body = create_survey_package_instance(client, random_record, fake=False)
        old_amount = len(client.all_survey_package_instances(record=random_record))

        feedback = client.create_survey_package_instance(**body)

        new_amount = len(client.all_survey_package_instances(record=random_record))

        assert feedback["record_id"] == random_record
        assert new_amount == old_amount + 1

    def test_create_survey_package_instance_fail(self, client):
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]
        body = create_survey_package_instance(client, random_record, fake=True)
        old_amount = len(client.all_survey_package_instances(record=random_record))

        with pytest.raises(CastorException) as e:
            client.create_survey_package_instance(**body)
        assert str(e.value) == "422 Failed Validation"

        new_amount = len(client.all_survey_package_instances(record=random_record))
        assert new_amount == old_amount

    def test_patch_survey_package_instance_success(
        self, client, all_survey_package_instances
    ):
        random_instance = random.choice(all_survey_package_instances)["id"]
        package = client.single_survey_package_instance(random_instance)
        old_status = package["locked"]

        target_status = not old_status
        client.patch_survey_package_instance(random_instance, target_status)

        package = client.single_survey_package_instance(random_instance)
        new_status = package["locked"]
        assert new_status is not old_status

    def test_patch_survey_package_instance_failure(
        self, client, all_survey_package_instances
    ):
        random_instance = random.choice(all_survey_package_instances)["id"]
        package = client.single_survey_package_instance(random_instance)
        old_status = package["locked"]
        target_status = not old_status
        fake_id = random_instance + "FAKE"

        with pytest.raises(CastorException) as e:
            client.patch_survey_package_instance(fake_id, target_status)
        assert str(e.value) == "404 Survey package invitation not found"

        package = client.single_survey_package_instance(random_instance)
        new_status = package["locked"]
        assert new_status is old_status
