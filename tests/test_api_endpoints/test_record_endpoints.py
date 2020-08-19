# -*- coding: utf-8 -*-
"""
Testing class for record endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import record_model
from castoredc_api_client.exceptions import CastorException


def create_record(client, fake):
    institutes = client.all_institutes()
    if fake:
        institute = random.choice(institutes)["institute_id"] + "FAKE"
    else:
        institute = random.choice(institutes)["institute_id"]
    return {
        "institute_id": institute,
        "email": "totallyfake@fakeemail.com",
        "record_id": str(random.randint(100000, 999999)),
        "ccr_patient_id": None,
    }


class TestRecord:
    model_keys = record_model.keys()

    @pytest.fixture(scope="class")
    def all_records(self, client):
        all_records = client.all_records()
        return all_records

    def test_all_records(self, all_records, item_totals):
        assert len(all_records) > 0
        assert len(all_records) == item_totals["total_records"]

    def test_all_records_model(self, all_records):
        random_record = random.choice(all_records)
        api_keys = random_record.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(random_record[key]) in record_model[key]

    def test_all_records_archived(self, client):
        all_records = client.all_records(archived=1)
        for record in all_records:
            assert record["archived"] is True

    def test_all_records_not_archived(self, client):
        all_records = client.all_records(archived=0)
        for record in all_records:
            assert record["archived"] is False

    def test_all_records_single_center(self, client):
        institutes = client.all_institutes()
        institute = random.choice(institutes)["institute_id"]
        all_records = client.all_records(institute_id=institute)
        for record in all_records:
            assert record["_embedded"]["institute"]["id"] == institute

    def test_single_record_success(self, client, all_records):
        random_id = random.choice(all_records)["id"]
        random_record = client.single_record(random_id)
        api_keys = random_record.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(random_record[key]) in record_model[key]

    def test_single_record_fail(self, client, all_records):
        with pytest.raises(CastorException) as e:
            client.single_record(random.choice(all_records)["id"] + "FAKE")
        assert str(e.value) == "404 Record not found."

    def test_create_record_success(self, client):
        len_records = len(client.all_records())

        record = create_record(client, fake=False)
        created = client.create_record(**record)
        new_record_id = created["id"]

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == (len_records + 1)
        assert new_record_id in [record["id"] for record in new_records]

    def test_create_record_fail(self, client):
        len_records = len(client.all_records())

        record = create_record(client, fake=True)
        with pytest.raises(CastorException) as e:
            client.create_record(**record)
        assert str(e.value) == "422 Failed Validation"

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == len_records
