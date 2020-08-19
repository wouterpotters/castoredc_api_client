import itertools
from typing import List, Optional, Any, Union

from castoredc_api_client.castor_objects.castor_form import CastorForm
from castoredc_api_client.castor_objects.castor_step import CastorStep
from castoredc_api_client.castor_objects.castor_field import CastorField


class CastorStudy:
    """Object representing a study in Castor. Functions as the head of a tree for all interrelations."""

    # TODO: Add study name and other characteristics
    def __init__(self, study_id: str) -> None:
        """Create a CastorStudy object."""
        self.study_id = study_id
        self.forms = []

    def add_form(self, form: CastorForm) -> None:
        """Add a CastorForm to the study."""
        self.forms.append(form)
        form.study = self

    def get_all_forms(self) -> List[CastorForm]:
        """Get all linked CastorForms."""
        return self.forms

    def get_single_form(self, form_id: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id."""
        return next((form for form in self.forms if form.form_id == form_id), None)

    def get_all_steps(self) -> List[CastorStep]:
        """Get all linked CastorSteps."""
        steps = list(itertools.chain.from_iterable([_form.steps for _form in self.forms]))
        return steps

    def get_single_step(self, step_id: str) -> Optional[CastorStep]:
        """Get a single CastorStep based on id."""
        steps = self.get_all_steps()
        return next((step for step in steps if step.step_id == step_id), None)

    def get_all_fields(self) -> List[CastorField]:
        """Get all linked CastorFields."""
        steps = list(itertools.chain.from_iterable([_form.steps for _form in self.forms]))
        fields = list(itertools.chain.from_iterable([_step.fields for _step in steps]))
        return fields

    def get_single_field(self, field_id: str) -> Optional[CastorField]:
        """Get a single CastorField based on id."""
        fields = self.get_all_fields()
        return next((field for field in fields if field.field_id == field_id), None)

    def get_all_study_fields(self) -> List[CastorField]:
        """Gets all linked study CastorFields."""
        return self.get_all_form_type_fields("Study")

    def get_all_survey_fields(self) -> List[CastorField]:
        """Gets all linked survey CastorFields."""
        return self.get_all_form_type_fields("Survey")

    def get_all_report_fields(self) -> List[CastorField]:
        """Gets all linked report CastorFields."""
        return self.get_all_form_type_fields("Report")

    # Helpers
    def get_all_form_type_fields(self, form_type: str) -> List[CastorField]:
        """Gets all linked CastorFields belonging to form of form_type."""
        fields = self.get_all_fields()
        return [field for field in fields if field.step.form.form_type == form_type]

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, ValueError]:
        if not isinstance(other, CastorStudy):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.study_id == other.study_id

    def __repr__(self) -> str:
        return self.study_id
