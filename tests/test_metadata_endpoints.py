# -*- coding: utf-8 -*-
"""
Testing class for metadata endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadata

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestMetadata:
    metadata_model = {
        "id": "string",
        "metadata_type": "dict",
        "parent_id": "string",
        "value": "string",
        "description": "string",
        "element_type": "int",
        "element_id": "int",
        "_links": "dict",
      }
    model_keys = metadata_model.keys()

    @pytest.fixture(scope="class")
    def all_metadata(self, client):
        all_metadata = client.all_metadata()
        return all_metadata

    def test_all_metadata(self, all_metadata, item_totals):
        assert len(all_metadata) > 0
        assert len(all_metadata) == item_totals["total_metadata"]

    def test_all_metadata_model(self, all_metadata):
        for i in range(0, 3):
            metadata = random.choice(all_metadata)
            api_keys = metadata.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_metadata_success(self, client, all_metadata):
        for i in range(0, 3):
            metadata_id = random.choice(all_metadata)["id"]
            metadata = client.single_metadata(metadata_id)
            api_keys = metadata.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_metadata_failure(self, client, all_metadata):
        for i in range(0, 3):
            metadata_id = random.choice(all_metadata)["id"] + "FAKE"
            metadata = client.single_metadata(metadata_id)
            assert metadata is None
