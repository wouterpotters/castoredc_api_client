import copy
from typing import List

import pytest

from castoredc_api_client.castor_objects import CastorField, CastorStep, CastorForm, CastorStudy
from tests.test_castor_objects.helpers_castor_objects import link_study_with_forms, link_forms_with_steps, \
    link_steps_with_fields, link_everything


@pytest.fixture(scope="session")
def fields() -> List[CastorField]:
    """Creates CastorFields for use in tests."""
    field1 = CastorField(field_id="FAKE-SURVEY-FIELD-ID1", field_name="Survey Field 1a1",
                         field_label="This is the first survey field",
                         field_type="checkbox", field_required=False, field_option_group="FAKE-OPTION-GROUP-ID1")
    field2 = CastorField(field_id="FAKE-SURVEY-FIELD-ID2", field_name="Survey Field 1a2",
                         field_label="This is the second survey field",
                         field_type="string", field_required=False, field_option_group=None)
    field3 = CastorField(field_id="FAKE-SURVEY-FIELD-ID3", field_name="Survey Field 1a3",
                         field_label="This is the third survey field",
                         field_type="calculation", field_required=False, field_option_group=None)
    field4 = CastorField(field_id="FAKE-SURVEY-FIELD-ID4", field_name="Survey Field 1b1",
                         field_label="This is the first survey field",
                         field_type="string", field_required=False, field_option_group=None)
    field5 = CastorField(field_id="FAKE-SURVEY-FIELD-ID5", field_name="Survey Field 1c1",
                         field_label="This is the first survey field",
                         field_type="number", field_required=False, field_option_group=None)
    field6 = CastorField(field_id="FAKE-SURVEY-FIELD-ID6", field_name="Survey Field 1c2",
                         field_label="This is the second survey field",
                         field_type="number", field_required=False, field_option_group=None)
    field7 = CastorField(field_id="FAKE-REPORT-FIELD-ID1", field_name="Report Field 1a1",
                         field_label="This is the first report field",
                         field_type="radio", field_required=True, field_option_group="FAKE-OPTION-GROUP-ID2")
    field8 = CastorField(field_id="FAKE-REPORT-FIELD-ID2", field_name="Report Field 1a2",
                         field_label="This is the second report field",
                         field_type="checkbox", field_required=True, field_option_group="FAKE-OPTION-GROUP-ID3")
    field9 = CastorField(field_id="FAKE-REPORT-FIELD-ID3", field_name="Report Field 1b1",
                         field_label="This is the first report field",
                         field_type="checkbox", field_required=True, field_option_group="FAKE-OPTION-GROUP-ID4")
    field10 = CastorField(field_id="FAKE-REPORT-FIELD-ID4", field_name="Report Field 2a1",
                          field_label="This is the first report field",
                          field_type="number", field_required=True, field_option_group=None)
    field11 = CastorField(field_id="FAKE-REPORT-FIELD-ID5", field_name="Report Field 2a2",
                          field_label="This is the second report field",
                          field_type="calculation", field_required=True, field_option_group=None)
    field12 = CastorField(field_id="FAKE-REPORT-FIELD-ID6", field_name="Report Field 2a3",
                          field_label="This is the third report field",
                          field_type="date", field_required=True, field_option_group=None)
    field13 = CastorField(field_id="FAKE-REPORT-FIELD-ID7", field_name="Report Field 2a4",
                          field_label="This is the fourth report field",
                          field_type="checkbox", field_required=True, field_option_group="FAKE-OPTION-GROUP-ID5")
    field14 = CastorField(field_id="FAKE-STUDY-FIELD-ID1", field_name="Study Field 1a1",
                          field_label="This is the first study field",
                          field_type="calculation", field_required=True, field_option_group=None)
    field15 = CastorField(field_id="FAKE-STUDY-FIELD-ID2", field_name="Study Field 1b1",
                          field_label="This is the first study field",
                          field_type="datetime", field_required=True, field_option_group=None)
    field16 = CastorField(field_id="FAKE-STUDY-FIELD-ID3", field_name="Study Field 1b2",
                          field_label="This is the second study field",
                          field_type="number", field_required=True, field_option_group=None)
    field17 = CastorField(field_id="FAKE-STUDY-FIELD-ID4", field_name="Study Field 1c1",
                          field_label="This is the first study field",
                          field_type="checkbox", field_required=False, field_option_group="FAKE-OPTION-GROUP-ID1")
    return [field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13,
            field14, field15, field16, field17]


@pytest.fixture(scope="session")
def steps() -> List[CastorStep]:
    """Creates CastorSteps for use in tests."""
    step1 = CastorStep("Survey Step 1a", "FAKE-SURVEY-STEP-ID1")
    step2 = CastorStep("Survey Step 1b", "FAKE-SURVEY-STEP-ID2")
    step3 = CastorStep("Survey Step 1c", "FAKE-SURVEY-STEP-ID3")
    step4 = CastorStep("Report Step 1a", "FAKE-REPORT-STEP-ID1")
    step5 = CastorStep("Report Step 1b", "FAKE-REPORT-STEP-ID2")
    step6 = CastorStep("Report Step 2a", "FAKE-REPORT-STEP-ID3")
    step7 = CastorStep("Study Step 1a", "FAKE-STUDY-STEP-ID1")
    step8 = CastorStep("Study Step 1b", "FAKE-STUDY-STEP-ID2")
    step9 = CastorStep("Study Step 1c", "FAKE-STUDY-STEP-ID3")
    return [step1, step2, step3, step4, step5, step6, step7, step8, step9]


@pytest.fixture(scope="session")
def forms() -> List[CastorForm]:
    """Creates CastorForms for use in tests."""
    form1 = CastorForm("Fake Survey", "FAKE-SURVEY-ID1", "Survey")
    form2 = CastorForm("Fake Report", "FAKE-REPORT-ID1", "Report")
    form3 = CastorForm("Fake Report", "FAKE-REPORT-ID2", "Report")
    form4 = CastorForm("Fake Study", "FAKE-STUDY-ID", "Study")
    return [form1, form2, form3, form4]


@pytest.fixture(scope="session")
def study() -> CastorStudy:
    """Creates a CastorStudy for use in tests."""
    study = CastorStudy("FAKE-ID")
    return study


@pytest.fixture(scope="session")
def study_with_forms(study: CastorStudy, forms: List[CastorForm]) -> CastorStudy:
    """Creates a CastorStudy with linked forms for use in tests."""
    # Deepcopy to prevent every fixture linking the objects
    return link_study_with_forms(copy.deepcopy(study), copy.deepcopy(forms))


@pytest.fixture(scope="session")
def forms_with_steps(forms: List[CastorForm], steps: List[CastorStep]) -> List[CastorForm]:
    """Creates CastorForms with linked steps for use in tests."""
    # Deepcopy to prevent every fixture linking the objects
    return link_forms_with_steps(copy.deepcopy(forms), copy.deepcopy(steps))


@pytest.fixture(scope="session")
def steps_with_fields(steps: List[CastorStep], fields: List[CastorField]) -> List[CastorStep]:
    """Creates CastorSteps with linked fields for use in tests."""
    # Deepcopy to prevent every fixture linking the objects
    return link_steps_with_fields(copy.deepcopy(steps), copy.deepcopy(fields))


@pytest.fixture(scope="session")
def complete_study(study: CastorStudy, forms: List[CastorForm],
                   steps: List[CastorStep], fields: List[CastorField]) -> CastorStudy:
    """Creates a CastorStudy with linked forms, steps, and fields for use in tests."""#
    # Deepcopy to prevent every fixture linking the objects
    return link_everything(copy.deepcopy(study), copy.deepcopy(forms), copy.deepcopy(steps), copy.deepcopy(fields))
