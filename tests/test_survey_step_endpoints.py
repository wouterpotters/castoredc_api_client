# -*- coding: utf-8 -*-
"""
Testing class for survey step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey-step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


class TestSurveyStep:
    survey_step_model = {
        "id": "string",
        "survey_step_id": "string",
        "survey_step_name": "string",
        "survey_step_description": "string",
        "survey_step_number": "int",
        "_embedded": "dict",
        "_links": "dict",
    }

    model_keys = survey_step_model.keys()

    @pytest.fixture(scope="class")
    def surveys_with_steps(self, client):
        surveys_with_steps = {}
        all_surveys = client.all_surveys()
        for survey in all_surveys:
            steps = client.single_survey_all_steps(survey["id"])
            surveys_with_steps[survey["id"]] = steps

        assert len(list(surveys_with_steps.keys())) > 0

        return surveys_with_steps

    def test_all_survey_steps(self, surveys_with_steps):
        for survey in surveys_with_steps:
            assert len(surveys_with_steps[survey]) > 0
            for step in surveys_with_steps[survey]:
                assert len(step) == len(self.model_keys)
                api_keys = step.keys()
                for key in self.model_keys:
                    assert key in api_keys

    def test_single_survey_single_step_success(self, client, surveys_with_steps):
        for i in range(0, 3):
            surveys = list(surveys_with_steps.keys())
            rand_survey = random.choice(surveys)
            rand_step = random.choice(surveys_with_steps[rand_survey])["survey_step_id"]
            step = client.single_survey_single_step(rand_survey, rand_step)
            api_keys = step.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_survey_single_step_fail(self, client, surveys_with_steps):
        for i in range(0, 3):
            surveys = list(surveys_with_steps.keys())
            rand_survey = random.choice(surveys)
            rand_step = (
                random.choice(surveys_with_steps[rand_survey])["survey_step_id"]
                + "FAKE"
            )
            step = client.single_survey_single_step(rand_survey, rand_step)
            assert step is None
