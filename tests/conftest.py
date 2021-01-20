# -*- coding: utf-8 -*-
"""
Global fixtures for testing CastorClient

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import logging
import logging.handlers
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
    client = CastorClient(auth_data.client_id, auth_data.client_secret)

    """Instantiates the logger for testing purposes."""
    # Set logger name and base level
    logger = logging.getLogger("castoredc_api_client")
    logger.setLevel(logging.DEBUG)
    # Create file logger
    # Create the directory if it does not exist
    Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))).mkdir(
        parents=True, exist_ok=True
    )
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "logs", "CastorClient.log")
    )
    f_handler = logging.handlers.RotatingFileHandler(
        file_path, maxBytes=5000000, backupCount=5
    )
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    client.link_study(auth_data.study_id)
    yield client

    handlers = client.logger.handlers[:]
    for handler in handlers:
        handler.close()
        client.logger.removeHandler(handler)
