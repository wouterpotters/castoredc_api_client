import pytest

from castoredc_api_client.castor_objects import CastorStudy, CastorForm, CastorStep, CastorField


@pytest.fixture(scope="function")
def fields():
    field1 = CastorField("FAKE-SURVEY-FIELD-ID1", "Survey Field 1a1", "This is the first survey field",
                         "checkbox", False, "FAKE-OPTION-GROUP-ID1")
    field2 = CastorField("FAKE-SURVEY-FIELD-ID2", "Survey Field 1a2", "This is the second survey field",
                         "string", False, None)
    field3 = CastorField("FAKE-SURVEY-FIELD-ID3", "Survey Field 1a3", "This is the third survey field",
                         "calculation", False, None)
    field4 = CastorField("FAKE-SURVEY-FIELD-ID4", "Survey Field 1b1", "This is the first survey field",
                         "string", False, None)
    field5 = CastorField("FAKE-SURVEY-FIELD-ID5", "Survey Field 1c1", "This is the first survey field",
                         "number", False, None)
    field6 = CastorField("FAKE-SURVEY-FIELD-ID6", "Survey Field 1c2", "This is the second survey field",
                         "number", False, None)
    field7 = CastorField("FAKE-REPORT-FIELD-ID1", "Report Field 1a1", "This is the first report field",
                         "radio", True, "FAKE-OPTION-GROUP-ID2")
    field8 = CastorField("FAKE-REPORT-FIELD-ID2", "Report Field 1a2", "This is the second report field",
                         "checkbox", True, "FAKE-OPTION-GROUP-ID3")
    field9 = CastorField("FAKE-REPORT-FIELD-ID3", "Report Field 1b1", "This is the first report field",
                         "checkbox", True, "FAKE-OPTION-GROUP-ID4")
    field10 = CastorField("FAKE-REPORT-FIELD-ID4", "Report Field 2a1", "This is the first report field",
                          "number", True, None)
    field11 = CastorField("FAKE-REPORT-FIELD-ID5", "Report Field 2a2", "This is the second report field",
                          "calculation", True, None)
    field12 = CastorField("FAKE-REPORT-FIELD-ID6", "Report Field 2a3", "This is the third report field",
                          "date", True, None)
    field13 = CastorField("FAKE-REPORT-FIELD-ID7", "Report Field 2a4", "This is the fourth report field",
                          "checkbox", True, "FAKE-OPTION-GROUP-ID5")
    field14 = CastorField("FAKE-STUDY-FIELD-ID14", "Study Field 1a1", "This is the first study field",
                          "calculation", True, None)
    field15 = CastorField("FAKE-STUDY-FIELD-ID15", "Study Field 1b1", "This is the first study field",
                          "datetime", True, None)
    field16 = CastorField("FAKE-STUDY-FIELD-ID16", "Study Field 1b2", "This is the second study field",
                          "number", True, None)
    field17 = CastorField("FAKE-STUDY-FIELD-ID17", "Study Field 1c1", "This is the first study field",
                          "checkbox", False, "FAKE-OPTION-GROUP-ID1")
    return [field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13,
            field14, field15, field16, field17]


@pytest.fixture(scope="function")
def steps():
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


@pytest.fixture(scope="function")
def forms():
    form1 = CastorForm("Survey", "FAKE-SURVEY-ID1", "Fake Survey")
    form2 = CastorForm("Report", "FAKE-REPORT-ID1", "Fake Report")
    form3 = CastorForm("Report", "FAKE-REPORT-ID2", "Fake Report")
    form4 = CastorForm("Study", "FAKE-STUDY-ID", "Fake Study")
    return [form1, form2, form3, form4]


@pytest.fixture(scope="function")
def study():
    study = CastorStudy("FAKE-ID")
    return study


@pytest.fixture(scope="function")
def study_with_forms(study, forms):
    study.forms = forms
    return study


@pytest.fixture(scope="function")
def forms_with_steps(forms, steps):
    forms[0].steps = steps[:3]
    forms[1].steps = steps[3:5]
    forms[2].steps = steps[5]
    forms[3].steps = steps[6:]
    return forms


@pytest.fixture(scope="function")
def steps_with_fields(steps, fields):
    steps[0].fields = fields[0:3]
    steps[1].fields = fields[3]
    steps[2].fields = fields[4:6]
    steps[3].fields = fields[6:8]
    steps[4].fields = fields[8]
    steps[5].fields = fields[9:13]
    steps[6].fields = fields[13]
    steps[7].fields = fields[14:16]
    steps[8].fields = fields[16]
    return steps


@pytest.fixture(scope="function")
def complete_study(study, forms, steps, fields):
    steps[0].fields = fields[0:3]
    steps[1].fields = fields[3]
    steps[2].fields = fields[4:6]
    steps[3].fields = fields[6:8]
    steps[4].fields = fields[8]
    steps[5].fields = fields[9:13]
    steps[6].fields = fields[13]
    steps[7].fields = fields[14:16]
    steps[8].fields = fields[16]

    forms[0].steps = steps[:3]
    forms[1].steps = steps[3:5]
    forms[2].steps = steps[5]
    forms[3].steps = steps[6:]

    study.forms = forms
    return study
