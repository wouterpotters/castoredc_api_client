# -*- coding: utf-8 -*-
"""
Testing class for study endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.exceptions import CastorException
from tests.data_models import study_model, user_model


class TestStudy:
    s_model_keys = study_model.keys()
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
                assert type(study[key]) in study_model[key]

    def test_single_study_success(self, all_studies, client):
        random_id = random.choice(all_studies)["study_id"]
        study = client.single_study(random_id)
        assert study is not None

        study_keys = study.keys()
        assert len(study_keys) == len(self.s_model_keys)
        for key in study_keys:
            assert key in self.s_model_keys
            assert type(study[key]) in study_model[key]

    def test_single_study_fail(self, all_studies, client):
        with pytest.raises(CastorException) as e:
            client.single_study(random.choice(all_studies)["study_id"] + "FAKE")
        assert str(e.value) == "403 You are not authorized to view this study."

    def test_all_users_success(self, all_studies, client):
        random_study = random.choice(all_studies)["study_id"]
        total_users = client.request_size(
            "/study/{random_study}/user".format(random_study=random_study), base=True
        )
        all_users = client.all_users_study(random_study)
        assert all_users is not None
        assert len(all_users) == total_users
        for user in all_users:
            user_keys = user.keys()
            assert len(user_keys) == len(self.u_model_keys)
            for key in user_keys:
                assert key in self.u_model_keys
                assert type(user[key]) in user_model[key]

    def test_all_users_fail(self, all_studies, client):
        with pytest.raises(CastorException) as e:
            client.all_users_study(random.choice(all_studies)["study_id"] + "FAKE")
        assert str(e.value) == "403 Forbidden"

    def test_single_user_success(self, all_studies, client):
        random_study = random.choice(all_studies)["study_id"]
        all_users = client.all_users_study(random_study)
        random_id = random.choice(all_users)["user_id"]
        user = client.single_user_study(random_study, random_id)
        user_keys = user.keys()
        assert len(user_keys) == len(self.u_model_keys)
        for key in user_keys:
            assert key in self.u_model_keys
            assert type(user[key]) in user_model[key]

    def test_single_user_fail(self, all_studies, client):
        random_study = random.choice(all_studies)["study_id"]
        all_users = client.all_users_study(random_study)
        with pytest.raises(CastorException) as e:
            client.single_user_study(random_study, random.choice(all_users)["user_id"] + "FAKE")
        assert str(e.value) == "404 User not found"
