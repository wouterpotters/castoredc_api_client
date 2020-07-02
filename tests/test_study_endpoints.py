# -*- coding: utf-8 -*-
"""
Testing class for study endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestStudy:
    study_model = {
        "crf_id": "string",
        "study_id": "string",
        "name": "string",
        "created_by": "string",
        "created_on": "string",
        "live": "boolean",
        "randomization_enabled": "boolean",
        "gcp_enabled": "boolean",
        "surveys_enabled": "boolean",
        "premium_support_enabled": "boolean",
        "main_contact": "string",
        "expected_centers": "int",
        "duration": "int",
        "expected_records": "int",
        "slug": "string",
        "version": "string",
        "domain": "string",
        "_links": "dict",
    }

    s_model_keys = study_model.keys()

    user_model = {
        "id": "string",
        "user_id": "string",
        "entity_id": "string",
        "full_name": "string",
        "name_first": "string",
        "name_middle": "string",
        "name_last": "string",
        "email_address": "string",
        "institute": "string",
        "department": "string",
        "last_login": "dict",
        "_links": "dict",
    }

    u_model_keys = user_model.keys()

    @pytest.fixture(scope="class")
    def all_studies(self, client):
        all_studies = client.all_studies()
        return all_studies

    def test_all_studies_amount(self, all_studies, item_totals):
        assert len(all_studies) == item_totals["total_studies"]

    def test_all_studies_model(self, all_studies):
        for study in all_studies:
            study_keys = study.keys()
            assert len(study_keys) == len(self.s_model_keys)
            for key in study_keys:
                assert key in self.s_model_keys

    def test_single_study_success(self, all_studies, client):
        for i in range(0, 3):
            random_id = random.choice(all_studies)["study_id"]
            study = client.single_study(random_id)
            assert study is not None

            study_keys = study.keys()
            assert len(study_keys) == len(self.s_model_keys)
            for key in study_keys:
                assert key in self.s_model_keys

    def test_single_study_fail(self, all_studies, client):
        for i in range(0, 3):
            random_id = random.choice(all_studies)["study_id"] + "FAKE"
            study = client.single_study(random_id)
            assert study is None

    def test_all_users_success(self, all_studies, client):
        random_study = random.choice(all_studies)["study_id"]
        total_users = client.request_size(f"/study/{random_study}/user",
                                          base=True)
        all_users = client.all_users_study(random_study)
        assert all_users is not None
        assert len(all_users) == total_users
        for user in all_users:
            user_keys = user.keys()
            assert len(user_keys) == len(self.u_model_keys)
            for key in user_keys:
                assert key in self.u_model_keys

    def test_all_users_fail(self, all_studies, client):
        random_study = random.choice(all_studies)["study_id"] + "FAKE"
        all_users = client.all_users_study(random_study)
        assert all_users is None

    def test_single_user_success(self, all_studies, client):
        for i in range(0, 3):
            random_study = random.choice(all_studies)["study_id"]
            all_users = client.all_users_study(random_study)
            random_id = random.choice(all_users)["user_id"]
            user = client.single_user_study(random_study, random_id)
            assert user is not None
            user_keys = user.keys()
            assert len(user_keys) == len(self.u_model_keys)
            for key in user_keys:
                assert key in self.u_model_keys

    def test_single_user_fail(self, all_studies, client):
        for i in range(0, 3):
            random_study = random.choice(all_studies)["study_id"]
            all_users = client.all_users_study(random_study)
            random_id = random.choice(all_users)["user_id"] + "FAKE"
            user = client.single_user_study(random_study, random_id)
            assert user is None
