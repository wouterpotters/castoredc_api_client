# -*- coding: utf-8 -*-
"""
Testing class for query endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/query

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestQuery:
    query_model = {
        "id": "string",
        "record_id": "string",
        "field_id": "string",
        "status": "string",
        "first_query_remark": "string",
        "created_by": "string",
        "created_on": "dict",
        "updated_by": "string",
        "updated_on": "dict",
        "_embedded": "dict",
        "_links": "dict",
      }
    model_keys = query_model.keys()

    @pytest.fixture(scope="class")
    def all_queries(self, client):
        all_queries = client.all_queries()
        return all_queries

    def test_all_queries(self, all_queries, item_totals):
        assert len(all_queries) > 0
        assert len(all_queries) == item_totals["total_queries"]

    def test_all_queries_model(self, all_queries):
        for i in range(0, 3):
            rand_query = random.choice(all_queries)
            api_keys = rand_query.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_query_success(self, client, all_queries):
        for i in range(0, 3):
            rand_id = random.choice(all_queries)["id"]
            query = client.single_query(rand_id)
            api_keys = query.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_query_failure(self, client, all_queries):
        for i in range(0, 3):
            rand_id = random.choice(all_queries)["id"] + "FAKE"
            query = client.single_query(rand_id)
            assert query is None
