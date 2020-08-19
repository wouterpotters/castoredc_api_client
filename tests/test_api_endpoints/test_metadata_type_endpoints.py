# -*- coding: utf-8 -*-
"""
Testing class for metadatatype endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadatatype

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import metadata_type_model
from castoredc_api_client.exceptions import CastorException


class TestMetadataType:
    model_keys = metadata_type_model.keys()

    @pytest.fixture(scope="class")
    def all_metadata_types(self, client):
        all_metadata_types = client.all_metadata_types()
        return all_metadata_types

    def test_all_metadata_types(self, all_metadata_types, item_totals):
        assert len(all_metadata_types) > 0
        assert len(all_metadata_types) == item_totals["total_metadata_types"]

    def test_all_metadata_types_model(self, all_metadata_types):
        metadata_type = random.choice(all_metadata_types)
        api_keys = metadata_type.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(metadata_type[key]) in metadata_type_model[key]

    def test_single_metadata_type_success(self, client, all_metadata_types):
        metadata_type = client.single_metadata_type(
            random.choice(all_metadata_types)["id"]
        )
        api_keys = metadata_type.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(metadata_type[key]) in metadata_type_model[key]

    def test_single_metadata_type_failure(self, client, all_metadata_types):
        with pytest.raises(CastorException) as e:
            client.single_metadata_type(random.choice(all_metadata_types)["id"] ** 100)
        assert str(e.value) == "404 Entity not found."
