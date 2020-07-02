# -*- coding: utf-8 -*-
"""
Testing class for step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestStep:
    step_model = {
        "id": "string",
        "step_id": "string",
        "step_description": "string",
        "step_name": "string",
        "step_order": "int",
        "_embedded": "dict",
        "_links": "dict",
    }

    model_keys = step_model.keys()

    @pytest.fixture(scope="class")
    def all_steps(self, client):
        all_steps = client.all_steps()
        return all_steps

    def test_all_steps_amount(self, all_steps, item_totals):
        assert len(all_steps) == item_totals["total_steps"]

    def test_all_steps_model(self, all_steps):
        for step in all_steps:
            step_keys = step.keys()
            assert len(step_keys) == len(self.model_keys)
            for key in step_keys:
                assert key in self.model_keys

    def test_single_step_success(self, all_steps, client):
        for i in range(0, 3):
            random_id = random.choice(all_steps)["id"]
            step = client.single_step(random_id)
            assert step is not None

            step_keys = step.keys()
            assert len(step_keys) == len(self.model_keys)
            for key in step_keys:
                assert key in self.model_keys

    def test_single_step_fail(self, all_steps, client):
        for i in range(0, 3):
            random_id = random.choice(all_steps)["id"] + "FAKE"
            step = client.single_step(random_id)
            assert step is None
