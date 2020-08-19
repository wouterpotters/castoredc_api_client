from typing import List

from castoredc_api_client.castor_objects import CastorField, CastorStep, CastorForm, CastorStudy


def link_study_with_forms(study: CastorStudy, forms: List[CastorForm]) -> CastorStudy:
    """Takes a list of forms and links them to a study."""
    study.forms = forms
    return study


def link_forms_with_steps(forms: List[CastorForm], steps: List[CastorStep]) -> List[CastorForm]:
    """Takes a list of steps and links them to a list of forms."""
    for step in steps[:3]:
        forms[0].add_step(step)

    for step in steps[3:5]:
        forms[1].add_step(step)

    forms[2].add_step(steps[5])

    for step in steps[6:]:
        forms[3].add_step(step)

    return forms


def link_steps_with_fields(steps: List[CastorStep], fields: List[CastorField]) -> List[CastorStep]:
    """Takes a list of fields and links them to a list of steps."""
    for field in fields[0:3]:
        steps[0].add_field(field)

    steps[1].add_field(fields[3])

    for field in fields[4:6]:
        steps[2].add_field(field)

    for field in fields[6:8]:
        steps[3].add_field(field)

    steps[4].add_field(fields[8])

    for field in fields[9:13]:
        steps[5].add_field(field)

    steps[6].add_field(fields[13])

    for field in fields[14:16]:
        steps[7].add_field(field)

    steps[8].add_field(fields[16])

    return steps


def link_everything(study: CastorStudy,
                    forms: List[CastorForm],
                    steps: List[CastorStep],
                    fields: List[CastorField]) -> CastorStudy:
    """Links a list of fields to a list of steps to a list of forms to a study."""
    steps = link_steps_with_fields(steps, fields)
    forms = link_forms_with_steps(forms, steps)
    study = link_study_with_forms(study, forms)
    return study
