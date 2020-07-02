# -*- coding: utf-8 -*-
"""
Testing class for record endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


def create_record(client, fake):
    institutes = client.all_institutes()
    if fake:
        institute = random.choice(institutes)["institute_id"] + "FAKE"
    else:
        institute = random.choice(institutes)["institute_id"]
    return {"institute_id": institute,
            "email": "totallyfake@fakeemail.com",
            "record_id": str(random.randint(100000, 999999)),
            "ccr_patient_id": None}


class TestRecord:
    record_model = {
        "id": "string",
        "record_id": "string",
        "_embedded": "dict",
        "ccr_patient_id": "string",
        "randomized_id": "string",
        "randomization_group": "int",
        "randomization_group_name": "string",
        "last_opened_step": "string",
        "progress": "int",
        "status": "string",
        "archived": "boolean",
        "archived_reason": "string",
        "created_by": "string",
        "created_on": "dict",
        "updated_by": "string",
        "updated_on": "dict",
        "_links": "dict",
    }

    model_keys = record_model.keys()

    @pytest.fixture(scope="class")
    def all_records(self, client):
        all_records = client.all_records()
        return all_records

    def test_all_records(self, all_records, item_totals):
        assert len(all_records) > 0
        assert len(all_records) == item_totals["total_records"]

    def test_all_records_model(self, all_records):
        for i in range(0, 3):
            random_record = random.choice(all_records)
            api_keys = random_record.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_all_records_archived(self, client):
        all_records = client.all_records(archived=1)
        for record in all_records:
            assert record["archived"] is True

    def test_all_records_not_archived(self, client):
        all_records = client.all_records(archived=0)
        for record in all_records:
            assert record["archived"] is False

    def test_all_records_single_center(self, client):
        # Assumes institute endpoints are working
        institutes = client.all_institutes()
        for i in range(0, 3):
            institute = random.choice(institutes)["institute_id"]
            all_records = client.all_records(institute_id=institute)
            for record in all_records:
                assert record["_embedded"]["institute"]["id"] == institute

    def test_single_record_success(self, client, all_records):
        for i in range(0, 3):
            random_id = random.choice(all_records)["id"]
            random_record = client.single_record(random_id)
            api_keys = random_record.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_record_fail(self, client, all_records):
        for i in range(0, 3):
            random_id = random.choice(all_records)["id"] + "FAKE"
            random_record = client.single_record(random_id)
            assert random_record is None

    def test_create_record_success(self, client):
        len_records = len(client.all_records())

        record = create_record(client, fake=False)
        created = client.create_record(**record)
        new_record_id = created["id"]

        assert created is not None

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == (len_records + 1)
        assert new_record_id in [record["id"] for record in new_records]

    def test_create_record_fail(self, client):
        len_records = len(client.all_records())

        record = create_record(client, fake=True)
        created = client.create_record(**record)

        assert created is None

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == len_records
