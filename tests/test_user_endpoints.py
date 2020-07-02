# -*- coding: utf-8 -*-
"""
Testing class for user endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/user

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random
import pytest


class TestUser:
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
    model_keys = user_model.keys()

    @pytest.fixture(scope="class")
    def all_users(self, client):
        all_users = client.all_users()
        return all_users

    def test_all_users(self, all_users):
        assert all_users is not None
        assert len(all_users) > 0
        for user in all_users:
            api_keys = user.keys()
            assert len(api_keys) == len(self.model_keys)
            for key in api_keys:
                assert key in self.model_keys

    def test_single_user_success(self, client, all_users):
        for i in range(0, 3):
            rand_id = random.choice(all_users)["id"]
            user = client.single_user(rand_id)
            assert user is not None
            api_keys = user.keys()
            assert len(api_keys) == len(self.model_keys)
            for key in api_keys:
                assert key in self.model_keys

    def test_single_user_fail(self, client, all_users):
        for i in range(0, 3):
            rand_id = random.choice(all_users)["id"] + "FAKE"
            user = client.single_user(rand_id)
            assert user is None
