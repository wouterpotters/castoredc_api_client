import itertools
from typing import List, Optional, Any, Union, TYPE_CHECKING

from castoredc_api_client.castor_objects.castor_data_point import CastorDataPoint
from castoredc_api_client.castor_objects.castor_field import CastorField
from castoredc_api_client.castor_objects.castor_form_instance import CastorFormInstance
from castoredc_api_client.castor_objects.castor_record import CastorRecord
from castoredc_api_client.castor_objects.castor_step import CastorStep
from castoredc_api_client.castor_objects.castor_form import CastorForm
from castoredc_api_client.exceptions import CastorException

if TYPE_CHECKING:
    from castoredc_api_client.castoredc_api_client import CastorClient


class CastorStudy:
    """Object representing a study in Castor. Functions as the head of a tree for all interrelations."""

    # TODO: Add study name and other characteristics
    def __init__(self, study_id: str) -> None:
        """Create a CastorStudy object."""
        self.study_id = study_id
        self.forms = []
        self.records = []

        # Dictionary of dicts to store the relationship between a form ID and a list of form instances
        self.form_links = {}

    # STRUCTURE MAPPING
    def map_structure(self, api_client) -> None:
        """Returns a CastorStudy object with the corresponding variable tree depicting interrelations"""
        # Get the structure from the API
        data = api_client.export_study_structure()

        # Loop over all fields
        for field in data:
            # Check if the form for the field exists, if not, create it
            form = self.get_single_form(field["Form Collection ID"])
            if form is None:
                form = CastorForm(
                    form_collection_type=field["Form Type"],
                    form_collection_id=field["Form Collection ID"],
                    form_collection_name=field["Form Collection Name"],
                )
                self.add_form(form)

            # Check if the step for the field exists, if not, create it
            step = form.get_single_step(field["Form ID"])
            if step is None:
                step = CastorStep(
                    step_id=field["Form ID"], step_name=field["Form Name"]
                )
                form.add_step(step)

            # Check if the field exists, if not, create it
            # This should not be possible as there are no doubles, but checking just in case
            new_field = step.get_single_field(field["Field ID"])
            if new_field is None:
                new_field = CastorField(
                    field_id=field["Field ID"],
                    field_name=field["Field Variable Name"],
                    field_label=field["Field Label"],
                    field_type=field["Field Type"],
                    field_required=field["Field Required"],
                    field_option_group=field["Field Option Group"],
                )
                step.add_field(new_field)

    # DATA MAPPING
    def link_data(self, api_client: "CastorClient") -> None:
        """Imports the data from the CastorClient database, maps the interrelations and links it to the study."""
        self.map_structure(api_client)
        self.update_links(api_client)
        self.map_data(api_client)

    def update_links(self, api_client: "CastorClient") -> None:
        """Creates the links between form and form instances."""
        form_links = {"Survey": {}, "Report": {}}

        # Get all survey forms that need to be linked
        survey_forms = self.get_all_survey_forms()
        for form in survey_forms:
            form_links["Survey"][form.form_id] = []

        # Get the name of the survey forms, as the export data can only be linked on name, not on id
        surveys = api_client.all_surveys()
        # Link form id to form name
        for survey in surveys:
            form_links["Survey"][survey["id"]].append(survey["name"])

        # Get all report forms that need to be linked
        report_forms = self.get_all_report_forms()
        for form in report_forms:
            form_links["Report"][form.form_id] = []

        # Get all report instances that need to be linked
        report_instances = api_client.all_report_instances()
        # Link instance to form on id
        for instance in report_instances:
            form_links["Report"][instance["_embedded"]["report"]["id"]].append(
                instance["id"]
            )

        self.form_links = form_links

    def map_data(self, api_client: "CastorClient") -> None:
        """Maps the study data"""
        # Get the data from the API
        data = api_client.export_study_data()

        # Loop over all fields
        for field in data:
            # Check if the record for the field exists, if not, create it
            record = self.get_single_record(field["Record ID"])
            if record is None:
                record = CastorRecord(record_id=field["Record ID"])
                self.add_record(record)

            # Check if it a data line or a record line
            if field["Form Type"] == "":
                pass
            else:
                if field["Form Type"] == "Study":
                    instance_of_field = self.get_single_field(field["Field ID"])
                    instance_of_form = instance_of_field.step.form.form_id
                    form_instance_id = instance_of_form
                    form_instance = record.get_single_form_instance(form_instance_id)
                    if form_instance is None:
                        form_instance = CastorFormInstance(
                            instance_id=form_instance_id,
                            instance_type=field["Form Type"],
                            name_of_form=field["Form Instance Name"],
                            study=self,
                        )
                        record.add_form_instance(form_instance)

                else:
                    form_instance = record.get_single_form_instance(
                        field["Form Instance ID"]
                    )
                    if form_instance is None:
                        form_instance = CastorFormInstance(
                            instance_id=field["Form Instance ID"],
                            instance_type=field["Form Type"],
                            name_of_form=field["Form Instance Name"],
                            study=self,
                        )
                        record.add_form_instance(form_instance)

                # Check if the field exists, if not, create it
                # This should not be possible as there are no doubles, but checking just in case
                data_point = form_instance.get_single_data_point(field["Field ID"])
                if data_point is None:
                    data_point = CastorDataPoint(
                        field_id=field["Field ID"], value=field["Value"], study=self
                    )
                    form_instance.add_data_point(data_point)

    # HELPERS
    def add_form(self, form: CastorForm) -> None:
        """Add a CastorForm to the study."""
        self.forms.append(form)
        form.study = self

    def get_all_forms(self) -> List[CastorForm]:
        """Get all linked CastorForms."""
        return self.forms

    def get_all_survey_forms(self) -> List[CastorForm]:
        """Gets all survey CastorForms."""
        return self.get_all_form_type_forms("Survey")

    def get_all_report_forms(self) -> List[CastorForm]:
        """Gets all report CastorForms."""
        return self.get_all_form_type_forms("Report")

    def get_all_form_type_forms(self, form_type: str) -> List[CastorForm]:
        """Gets all linked CastorFields belonging to form of form_type."""
        forms = self.get_all_forms()
        return [form for form in forms if form.form_type == form_type]

    def get_single_form(self, form_id: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id."""
        return next((form for form in self.forms if form.form_id == form_id), None)

    def get_single_form_name(self, form_name: str) -> Optional[CastorForm]:
        """Get a single CastorForm based on id."""
        return next((form for form in self.forms if form.form_name == form_name), None)

    def add_record(self, record: CastorRecord) -> None:
        """Add a CastorRecord to the study."""
        self.records.append(record)
        record.study = self

    def get_all_records(self) -> List[CastorRecord]:
        """Get all linked CastorRecords."""
        return self.records

    def get_single_record(self, record_id: str) -> Optional[CastorRecord]:
        """Get a single CastorRecord based on id."""
        return next(
            (record for record in self.records if record.record_id == record_id), None
        )

    def get_all_steps(self) -> List[CastorStep]:
        """Get all linked CastorSteps."""
        steps = list(
            itertools.chain.from_iterable([_form.steps for _form in self.forms])
        )
        return steps

    def get_single_step(self, step_id: str) -> Optional[CastorStep]:
        """Get a single CastorStep based on id."""
        steps = self.get_all_steps()
        return next((step for step in steps if step.step_id == step_id), None)

    def get_all_fields(self) -> List[CastorField]:
        """Get all linked CastorFields."""
        fields = list(
            itertools.chain.from_iterable(
                [form.get_all_fields() for form in self.forms]
            )
        )
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

    def get_all_form_type_fields(self, form_type: str) -> List[CastorField]:
        """Gets all linked CastorFields belonging to form of form_type."""
        fields = self.get_all_fields()
        return [field for field in fields if field.step.form.form_type == form_type]

    def get_all_form_instances(self) -> List["CastorFormInstance"]:
        """Returns all form instances"""
        form_instances = list(
            itertools.chain.from_iterable(
                [_record.form_instances for _record in self.records]
            )
        )
        return form_instances

    def get_single_form_instance(
            self, record_id: str, instance_id: str,
    ) -> Optional["CastorFormInstance"]:
        """Returns a single form instance based on id."""
        record = self.get_single_record(record_id)
        all_form_instances = record.get_all_form_instances()
        return next(
            (
                instance
                for instance in all_form_instances
                if instance.instance_id == instance_id
            ),
            None,
        )

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the study"""
        data_points = list(
            itertools.chain.from_iterable(
                [_record.get_all_data_points() for _record in self.records]
            )
        )
        return data_points

    def get_single_data_point(
            self, record_id: str, form_instance_id: str, field_id: str
    ) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        form_instance = self.get_single_form_instance(record_id, form_instance_id)
        data_points = form_instance.get_all_data_points()
        return next(
            (
                _data_point
                for _data_point in data_points
                if _data_point.field_id == field_id
            ),
            None,
        )

    def instance_of_form(
            self, instance_id: str, instance_type: str
    ) -> Optional[CastorForm]:
        """Returns the form of which the given id is an instance.
        instance_id is id for type: Report, name for type: Survey, or id for type: Study"""
        if instance_type == "Study":
            return self.get_single_form(instance_id)
        elif instance_type == "Report" or instance_type == "Survey":
            options = self.form_links[instance_type]
            form_id = next(
                (form_id for form_id in options if instance_id in options[form_id]),
                None,
            )
            return self.get_single_form(form_id)
        else:
            raise CastorException("{} is not a form type.".format(instance_type))

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStudy):
            return NotImplemented
        else:
            return self.study_id == other.study_id

    def __repr__(self) -> str:
        return self.study_id
