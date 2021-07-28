# -*- coding: utf-8 -*-
"""
Global fixtures for testing CastorClient

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import os
from pathlib import Path

from castoredc_api_client.castoredc_api_client import CastorClient
import pytest
import auth.auth_data as auth_data

pytest_plugins = [
    "tests.test_api_endpoints.fixtures_api",
]


@pytest.fixture(scope="class")
def client():
    client = CastorClient(auth_data.client_id, auth_data.client_secret, "data.castoredc.com")
    client.link_study(auth_data.study_id)
    return client
