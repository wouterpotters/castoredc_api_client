# -*- coding: utf-8 -*-
"""
Testing classes for the different Castor Objects.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest

from castoredc_api_client.castor_objects import CastorStudy, CastorForm


class TestCastorStudy:
    """Testing class for CastorStudy object unit tests."""
    # Creating a study
    def test_study_create(self):
        """Tests creation of a study."""
        study = CastorStudy("FAKE-ID")
        assert type(study) is CastorStudy
        assert study.study_id == "FAKE-ID"

    # Adding and getting forms
    def test_study_add_form(self):
        """Tests adding a form to a study."""
        study = CastorStudy("FAKE-ID")
        assert len(study.forms) == 0
        form = CastorForm("Survey", "FAKE-FORM-ID", "Fake Survey")
        study.add_form(form)
        assert len(study.forms) == 1
        assert study.forms[0] == form

    def test_study_get_form(self, study_with_forms):
        """Tests getting a form from the study."""
        form = study_with_forms.get_form("FAKE-REPORT-ID2")
        assert type(form) is CastorForm
        assert form.form_id == "FAKE-REPORT-ID2"
        assert form.form_type == "Report"
        assert form.form_name == "Fake Report"

    def test_study_get_form_fail(self, study_with_forms):
        """Tests failing to get a form from the study."""
        form = study_with_forms.get_form("FAKE-REPORT-ID3")
        assert form is None


class TestCastorForm:
    """Testing class for CastorForm object unit tests."""
    pass