# -*- coding: utf-8 -*-
"""
Testing class for metadatatype endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadatatype

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestMetadataType:
    metadatatype_model = {
        "id": "string",
        "name": "string",
        "description": "string",
        "_links": "dict",
      }
    model_keys = metadatatype_model.keys()

    @pytest.fixture(scope="class")
    def all_metadatatypes(self, client):
        all_metadatatypes = client.all_metadatatypes()
        return all_metadatatypes

    def test_all_metadatatypes(self, all_metadatatypes, item_totals):
        assert len(all_metadatatypes) > 0
        assert len(all_metadatatypes) == item_totals["total_metadatatypes"]

    def test_all_metadatatypes_model(self, all_metadatatypes):
        for i in range(0, 3):
            metadatatype = random.choice(all_metadatatypes)
            api_keys = metadatatype.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_metadatatype_success(self, client, all_metadatatypes):
        for i in range(0, 3):
            metadatatype_id = random.choice(all_metadatatypes)["id"]
            metadatatype = client.single_metadatatype(metadatatype_id)
            api_keys = metadatatype.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_metadatatype_failure(self, client, all_metadatatypes):
        for i in range(0, 3):
            metadatatype_id = random.choice(all_metadatatypes)["id"] ** 100
            metadatatype = client.single_metadatatype(metadatatype_id)
            assert metadatatype is None
