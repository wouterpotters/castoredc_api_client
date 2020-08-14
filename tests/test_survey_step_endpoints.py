# -*- coding: utf-8 -*-
"""
Testing class for survey step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey-step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from castoredc_api_client.exceptions import CastorException
from tests.data_models import survey_step_model


class TestSurveyStep:
    model_keys = survey_step_model.keys()

    @pytest.fixture(scope="class")
    def surveys_with_steps(self, client):
        surveys_with_steps = {}
        all_surveys = client.all_surveys()
        for survey in all_surveys:
            steps = client.single_survey_all_steps(survey["id"])
            surveys_with_steps[survey["id"]] = steps
        return surveys_with_steps

    def test_all_survey_steps(self, surveys_with_steps):
        for survey in surveys_with_steps:
            assert len(surveys_with_steps[survey]) > 0
            for step in surveys_with_steps[survey]:
                assert len(step) == len(self.model_keys)
                api_keys = step.keys()
                for key in self.model_keys:
                    assert key in api_keys
                    assert type(step[key]) in survey_step_model[key]

    def test_single_survey_single_step_success(self, client, surveys_with_steps):
        for i in range(0, 3):
            rand_survey = random.choice(list(surveys_with_steps.keys()))
            rand_step = random.choice(surveys_with_steps[rand_survey])["survey_step_id"]
            step = client.single_survey_single_step(rand_survey, rand_step)
            api_keys = step.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys
                assert type(step[key]) in survey_step_model[key]

    def test_single_survey_single_step_fail(self, client, surveys_with_steps):
        rand_survey = random.choice(list(surveys_with_steps.keys()))
        rand_step = (
            random.choice(surveys_with_steps[rand_survey])["survey_step_id"] + "FAKE"
        )

        with pytest.raises(CastorException) as e:
            client.single_survey_single_step(rand_survey, rand_step)
        assert str(e.value) == "404 Entity not found."
