# -*- coding: utf-8 -*-
"""
Testing class for report-instance endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-instance

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import report_instance_model
from castoredc_api_client.exceptions import CastorException


def create_report_instance(client, record_id, fake):
    reports = client.all_reports()
    report_ids = [report["id"] for report in reports]
    random_report = random.choice(report_ids)

    custom_name = str(random.randint(10000000, 99999999))
    if fake:
        random_report += "FAKE"

    return {
        "record_id": record_id,
        "report_id": random_report,
        "report_name_custom": custom_name,
    }


class TestReportInstance:
    model_keys = report_instance_model.keys()

    @pytest.fixture(scope="class")
    def all_report_instances(self, client):
        all_report_instances = client.all_report_instances()
        return all_report_instances

    def test_all_report_instances(self, all_report_instances, item_totals):
        assert len(all_report_instances) > 0
        assert len(all_report_instances) == item_totals["total_report_instances"]

    def test_all_report_instances_model(self, all_report_instances):
        rand_report_instance = random.choice(all_report_instances)
        api_keys = rand_report_instance.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(rand_report_instance[key]) in report_instance_model[key]

    def test_single_report_instance_success(self, client, all_report_instances):
        rand_id = random.choice(all_report_instances)["id"]
        report_instance = client.single_report_instance(rand_id)
        api_keys = report_instance.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(report_instance[key]) in report_instance_model[key]

    def test_single_report_instance_fail(self, client, all_report_instances):
        with pytest.raises(CastorException) as e:
            client.single_report_instance(
                random.choice(all_report_instances)["id"] + "FAKE"
            )
        assert "The request you made was malformed" in str(e.value)

    def test_all_report_instances_record_success(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        rand_rec = random.choice(records)
        reports = client.all_report_instances_record(rand_rec)
        for report in reports:
            report_keys = report.keys()
            assert len(self.model_keys) == len(report_keys)
            for key in self.model_keys:
                assert key in report_keys
                assert type(report[key]) in report_instance_model[key]

    def test_all_report_instances_record_fail(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        with pytest.raises(CastorException) as e:
            client.all_report_instances_record(random.choice(records) + "FAKE")
        assert "The request you made was malformed" in str(e.value)

    def test_single_report_instance_record_success(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        random_record = random.choice(records)
        random_report = random.choice(records_with_reports[random_record])
        report = client.single_report_instance_record(random_record, random_report)
        report_keys = report.keys()
        assert len(self.model_keys) == len(report_keys)
        for key in self.model_keys:
            assert key in report_keys
            assert type(report[key]) in report_instance_model[key]

    def test_single_report_instance_record_fail(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        random_record = random.choice(records)
        reports = records_with_reports[random_record]
        random_report = random.choice(reports) + "FAKE"
        with pytest.raises(CastorException) as e:
            client.single_report_instance_record(random_record, random_report)
        assert "The request you made was malformed" in str(e.value)

    def test_create_report_instance_record_success(self, client, records_with_reports):
        random_record = random.choice(list(records_with_reports.keys()))
        report_instance = create_report_instance(client, random_record, fake=False)
        record_reports = client.all_report_instances_record(random_record)
        amount_reports = len(record_reports)

        created = client.create_report_instance_record(**report_instance)

        assert created["name"] == report_instance["report_name_custom"]
        assert created["record_id"] == report_instance["record_id"]

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports + 1 == new_amount

    def test_create_report_instance_record_fail(self, client, records_with_reports):
        random_record = random.choice(list(records_with_reports.keys()))
        report_instance = create_report_instance(client, random_record, fake=True)
        record_reports = client.all_report_instances_record(random_record)
        amount_reports = len(record_reports)

        with pytest.raises(CastorException) as e:
            client.create_report_instance_record(**report_instance)
        assert "The request you made was malformed" in str(e.value)

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports == new_amount

    def test_create_multiple_report_instances_record_success(
        self, client, records_with_reports
    ):
        random_record = random.choice(list(records_with_reports.keys()))

        reports = []
        for i in range(0, 5):
            report_instance = create_report_instance(client, random_record, fake=False)
            reports.append(report_instance)

        record_reports = client.all_report_instances_record(random_record)
        amount_reports = len(record_reports)

        created = client.create_multiple_report_instances_record(random_record, reports)

        assert created["total_success"] == 5
        assert created["total_failed"] == 0

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports + 5 == new_amount

    def test_create_multiple_report_instances_record_fail(
        self, client, records_with_reports
    ):
        random_record = random.choice(list(records_with_reports.keys()))

        reports = []
        for i in range(0, 5):
            report_instance = create_report_instance(client, random_record, fake=True)
            reports.append(report_instance)

        record_reports = client.all_report_instances_record(random_record)
        amount_reports = len(record_reports)

        created = client.create_multiple_report_instances_record(random_record, reports)

        assert created["total_success"] == 0
        assert created["total_failed"] == 5

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports == new_amount
