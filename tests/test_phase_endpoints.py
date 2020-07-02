# -*- coding: utf-8 -*-
"""
Testing class for phase endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/phase

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestPhase:
    phase_model = {
        "id": "string",
        "phase_id": "string",
        "phase_description": "",  # TODO, no documentation on value returned
        "phase_name": "string",
        "phase_duration": "int",
        "phase_order": "int",
        "_links": "dict",
      }

    model_keys = phase_model.keys()

    @pytest.fixture(scope="class")
    def all_phases(self, client):
        all_phases = client.all_phases()
        return all_phases

    def test_all_phases(self, all_phases, item_totals):
        assert len(all_phases) > 0
        assert len(all_phases) == item_totals["total_phases"]

    def test_all_phases_model(self, all_phases):
        for i in range(0, 3):
            phase = random.choice(all_phases)
            api_keys = phase.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_phase_success(self, client, all_phases):
        for i in range(0, 3):
            phase_id = random.choice(all_phases)["phase_id"]
            phase = client.single_phase(phase_id)
            api_keys = phase.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_phase_failure(self, client, all_phases):
        for i in range(0, 3):
            phase_id = random.choice(all_phases)["phase_id"] + "FAKE"
            phase = client.single_phase(phase_id)
            assert phase is None
