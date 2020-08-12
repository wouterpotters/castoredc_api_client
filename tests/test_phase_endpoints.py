# -*- coding: utf-8 -*-
"""
Testing class for phase endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/phase

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.data_models import phase_model
from castoredc_api_client.exceptions import CastorException


class TestPhase:
    model_keys = phase_model.keys()

    @pytest.fixture(scope="class")
    def all_phases(self, client):
        all_phases = client.all_phases()
        return all_phases

    def test_all_phases(self, all_phases, item_totals):
        assert len(all_phases) > 0
        assert len(all_phases) == item_totals["total_phases"]

    def test_all_phases_model(self, all_phases):
        phase = random.choice(all_phases)
        api_keys = phase.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(phase[key]) in phase_model[key]

    def test_single_phase_success(self, client, all_phases):
        phase_id = random.choice(all_phases)["phase_id"]
        phase = client.single_phase(phase_id)
        api_keys = phase.keys()
        assert len(self.model_keys) == len(api_keys)
        for key in self.model_keys:
            assert key in api_keys
            assert type(phase[key]) in phase_model[key]

    def test_single_phase_failure(self, client, all_phases):
        with pytest.raises(CastorException) as e:
            client.single_phase(random.choice(all_phases)["phase_id"] + "FAKE")
        assert str(e.value) == "404 Entity not found."
