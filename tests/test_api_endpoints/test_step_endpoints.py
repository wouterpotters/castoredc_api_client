# -*- coding: utf-8 -*-
"""
Testing class for step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from tests.test_api_endpoints.data_models import study_step_model
from castoredc_api_client.exceptions import CastorException


class TestStep:
    model_keys = study_step_model.keys()

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
                assert type(step[key]) in study_step_model[key]

    def test_single_step_success(self, all_steps, client):
        random_id = random.choice(all_steps)["id"]
        step = client.single_step(random_id)

        step_keys = step.keys()
        assert len(step_keys) == len(self.model_keys)
        for key in step_keys:
            assert key in self.model_keys
            assert type(step[key]) in study_step_model[key]

    def test_single_step_fail(self, all_steps, client):
        with pytest.raises(CastorException) as e:
            client.single_step(random.choice(all_steps)["id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
