# -*- coding: utf-8 -*-
"""
Testing class for field-dependency endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-dependency

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestFieldDependency:
    field_dep_model = {
        "id": "string",
        "operator": "string",
        "value": "string",
        "parent_id": "string",
        "child_id": "string",
        "_links": "dict",
    }
    model_keys = field_dep_model.keys()

    @pytest.fixture(scope="class")
    def all_field_deps(self, client):
        all_field_deps = client.all_field_dependencies()
        return all_field_deps

    def test_all_field_deps(self, all_field_deps, item_totals):
        assert len(all_field_deps) > 0
        assert len(all_field_deps) == item_totals["total_field_deps"]

    def test_all_field_deps_model(self, all_field_deps):
        for i in range(0, 3):
            rand_field = random.choice(all_field_deps)
            api_keys = rand_field.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_success(self, client, all_field_deps):
        for i in range(0, 3):
            rand_id = random.choice(all_field_deps)["id"]
            dep = client.single_field_dependency(rand_id)
            api_keys = dep.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_field_failure(self, client, all_field_deps):
        # NOTE: API seems to truncate text after the ID.
        # i.e. if 247 is an existing ID, then 247TEXT also works.
        for i in range(0, 3):
            rand_id = "FAKE" + random.choice(all_field_deps)["id"] + "FAKE"
            dep = client.single_field_dependency(rand_id)
            assert dep is None
