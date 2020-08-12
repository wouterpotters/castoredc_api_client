# -*- coding: utf-8 -*-
"""
Testing class for query endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/query

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.data_models import query_model
from castoredc_api_client.exceptions import CastorException


class TestQuery:
    model_keys = query_model.keys()

    @pytest.fixture(scope="class")
    def all_queries(self, client):
        all_queries = client.all_queries()
        return all_queries

    def test_all_queries(self, all_queries, item_totals):
        assert len(all_queries) > 0
        assert len(all_queries) == item_totals["total_queries"]

    def test_all_queries_model(self, all_queries):
        rand_query = random.choice(all_queries)
        api_keys = rand_query.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(rand_query[key]) in query_model[key]

    def test_single_query_success(self, client, all_queries):
        rand_id = random.choice(all_queries)["id"]
        query = client.single_query(rand_id)
        api_keys = query.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(query[key]) in query_model[key]

    def test_single_query_failure(self, client, all_queries):
        with pytest.raises(CastorException) as e:
            client.single_query(random.choice(all_queries)["id"] + "FAKE")
        assert str(e.value) == "404 Query not found."
