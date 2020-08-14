# -*- coding: utf-8 -*-
"""
Testing class for metadata endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadata

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.data_models import metadata_model
from castoredc_api_client.exceptions import CastorException


class TestMetadata:
    model_keys = metadata_model.keys()

    @pytest.fixture(scope="class")
    def all_metadata(self, client):
        all_metadata = client.all_metadata()
        return all_metadata

    def test_all_metadata(self, all_metadata, item_totals):
        assert len(all_metadata) > 0
        assert len(all_metadata) == item_totals["total_metadata"]

    def test_all_metadata_model(self, all_metadata):
        metadata = random.choice(all_metadata)
        api_keys = metadata.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(metadata[key]) in metadata_model[key]

    def test_single_metadata_success(self, client, all_metadata):
        metadata_id = random.choice(all_metadata)["id"]
        metadata = client.single_metadata(metadata_id)
        api_keys = metadata.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(metadata[key]) in metadata_model[key]

    def test_single_metadata_failure(self, client, all_metadata):
        with pytest.raises(CastorException) as e:
            client.single_metadata(random.choice(all_metadata)["id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
