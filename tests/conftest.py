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

data_options = {
    "numeric": "1",
    "date": "11-11-2017",
    "string": "testing",
    "dropdown": "1",
    "radio": "1",
    "textarea": "testing",
    "slider": "5",
    "checkbox": "1",
    "calculation": "5",
    "year": "2005",
}


@pytest.fixture(scope="session")
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
    client.gather_field_map()
    yield client

    handlers = client.logger.handlers[:]
    for handler in handlers:
        handler.close()
        client.logger.removeHandler(handler)


@pytest.fixture(scope="class")
def item_totals(client):
    # TODO: refactor this so that it only runs once, or when it needs
    # to be updated.
    item_totals = {
        "total_fields": client.request_size("/field"),
        "total_field_deps": client.request_size("/field-dependency"),
        "total_field_opts": client.request_size("/field-optiongroup"),
        "total_field_vals": client.request_size("/field-validation"),
        "total_institutes": client.request_size("/institute"),
        "total_metadata": client.request_size("/metadata"),
        "total_metadatatypes": client.request_size("/metadatatype"),
        "total_phases": client.request_size("/phase"),
        "total_queries": client.request_size("/query"),
        "total_study_data_points": client.request_size("/data-point-collection/study"),
        "total_report_data_points": client.request_size(
            "/data-point-collection/report-instance"
        ),
        "total_survey_data_points": client.request_size(
            "/data-point-collection/survey-instance"
        ),
        "total_records": client.request_size("/record"),
        "total_reports": client.request_size("/report"),
        "total_report_instances": client.request_size("/report-instance"),
        "total_steps": client.request_size("/step"),
        "total_studies": client.request_size("/study", base=True),
        "total_surveys": client.request_size("/survey"),
        "total_survey_packages": client.request_size("/surveypackage"),
    }
    return item_totals


@pytest.fixture(scope="class")
def all_record_ids(client):
    records = client.all_records(archived=0)
    all_record_ids = [record["id"] for record in records]
    return all_record_ids


@pytest.fixture(scope="class")
def records_with_reports(client, all_record_ids):
    records_with_reports = {}
    for record_id in all_record_ids:
        report_instances = client.all_report_instances_record(record_id)
        if report_instances is not None and len(report_instances) > 0:
            report_inst_ids = [inst["id"] for inst in report_instances]
            records_with_reports[record_id] = report_inst_ids
    return records_with_reports


@pytest.fixture(scope="class")
def records_with_survey_package_instances(client, all_record_ids):
    records_with_survey_package_instances = {}
    for record_id in all_record_ids:
        survey_package_instances = client.all_survey_package_instances(record=record_id)
        if survey_package_instances is not None and len(survey_package_instances) > 0:
            survey_inst_ids = [inst["id"] for inst in survey_package_instances]
            records_with_survey_package_instances[record_id] = survey_inst_ids
    return records_with_survey_package_instances


@pytest.fixture(scope="class")
def records_with_survey_instances(client, all_record_ids):
    records_with_survey_instances = {}
    for record_id in all_record_ids:
        survey_instance_ids = []
        survey_instances = client.all_survey_data_points_record(record_id)
        if survey_instances is not None and len(survey_instances) > 0:
            for instance in survey_instances:
                survey_instance_ids.append(
                    (instance["survey_instance_id"], instance["survey_name"])
                )
            survey_instance_ids = list(set(survey_instance_ids))
            records_with_survey_instances[record_id] = survey_instance_ids
    return records_with_survey_instances


@pytest.fixture(scope="class")
def all_report_data_points(client):
    all_report_data_points = client.all_report_data_points()
    return all_report_data_points


@pytest.fixture(scope="class")
def all_study_data_points(client):
    all_study_data_points = client.all_study_data_points()
    return all_study_data_points


@pytest.fixture(scope="class")
def all_survey_data_points(client):
    all_survey_data_points = client.all_survey_data_points()
    return all_survey_data_points


@pytest.fixture(scope="session")
def report_field_ids(client):
    """Returns a list of field ids for every report in the study.
    Can only gather data on fields that have already been filled in once
    for any subject."""
    report_data_points = client.all_report_data_points()
    report_field_ids = set(field["field_id"] for field in report_data_points)
    return report_field_ids


@pytest.fixture(scope="session")
def survey_field_ids(client):
    """Returns a list of field ids for every survey in the study.
    Can only gather data on fields that have already been filled in once
    for any subject."""
    survey_data_points = client.all_survey_data_points()
    survey_field_ids = set(field["field_id"] for field in survey_data_points)
    return survey_field_ids


@pytest.fixture(scope="session")
def study_field_ids(client):
    """Returns a list of field ids for every phase/study-field in the study.
    Can only gather data on fields that have already been filled in once
    for any subject."""
    study_data_points = client.all_study_data_points()
    study_field_ids = set(field["field_id"] for field in study_data_points)
    return study_field_ids
