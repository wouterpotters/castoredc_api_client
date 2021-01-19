from datetime import datetime
from typing import Union, Any, TYPE_CHECKING

from exceptions.exceptions import CastorException

if TYPE_CHECKING:
    from castoredc_study.castor_objects.castor_field import CastorField
    from castoredc_study.castor_study import CastorStudy


class CastorDataPoint:
    """Object representing a Castor datapoint. Is an instance of a field with a value for a record.."""

    def __init__(
        self, field_id: str, raw_value: Union[str, int], study: "CastorStudy", filled_in: str
    ) -> None:
        """Creates a CastorField."""
        self.field_id = field_id
        self.raw_value = raw_value
        self.instance_of = self.find_field(study)
        if self.instance_of is None:
            raise CastorException(
                "The field that this is an instance of does not exist in the study!"
            )
        self.form_instance = None
        self.filled_in = datetime.strptime(filled_in, "%Y-%m-%d %H:%M:%S")
        self.value = None

    # Helpers
    def find_field(self, study: "CastorStudy") -> "CastorField":
        return study.get_single_field(self.field_id)

    def interpret(self) -> None:
        """Transform the raw value into analysable data."""
        if "Missing" in self.raw_value:
            self.value = self.raw_value
        elif self.instance_of.field_type in ["checkbox", "dropdown", "radio"]:
            self.__interpret_optiongroup()
        elif self.instance_of.field_type in ["numeric", "year", "slider", "randomization"]:
            self.__interpret_numeric()
        elif self.instance_of.field_type in ["string", "textarea", "upload"]:
            self.value = self.raw_value
        elif self.instance_of.field_type in ["calculation"]:
            try:
                self.__interpret_numeric()
            except ValueError:
                self.value = self.raw_value
        elif self.instance_of.field_type in ["date"]:
            self.value = datetime.strptime(self.raw_value, "%d-%m-%Y")
        elif self.instance_of.field_type in ["datetime"]:
            self.value = datetime.strptime(self.raw_value, "%d-%m-%Y;%H:%M")
        elif self.instance_of.field_type in ["time"]:
            self.value = datetime.strptime(self.raw_value, "%H:%M").time()
        elif self.instance_of.field_type in ["numberdate"]:
            self.__interpret_numberdate()
        else:
            pass

    def __interpret_optiongroup(self) -> None:
        """Interprets optiongroup data"""
        # Get the optiongroup for this data point
        optiongroup = self.instance_of.field_option_group
        # Get all optiongroup options from the study
        study_groups = self.form_instance.record.study.optiongroups
        # Retrieve the options
        study_optiongroup = next((group for group in study_groups if (group["id"] == optiongroup)), None)
        if study_optiongroup is None:
            raise CastorException("Optiongroup not found. Is id correct and are optiongroups loaded?")
        # Get options
        options = study_optiongroup["options"]
        # Transform options into dict value: name
        link = {item["value"]: item["name"] for item in options}
        # Get values, split by ; for checklists
        value_list = self.raw_value.split(";")
        # Values to names
        new_values = [link[value] for value in value_list]
        # Return string for a single value, else return the list
        if len(new_values) == 1:
            self.value = new_values[0]
        else:
            self.value = new_values

    def __interpret_numeric(self) -> None:
        """Interprets numeric data"""
        if "." in self.raw_value:
            self.value = float(self.raw_value)
        else:
            self.value = int(self.raw_value)

    def __interpret_numberdate(self) -> None:
        """Interprets numberdate data"""
        # Get number and date from the string
        number, date = self.raw_value.split(";")
        # Interpret number
        if "." in number:
            number = float(number)
        else:
            number = int(number)
        # Interpret date
        date = datetime.strptime(date, "%d-%m-%Y")
        # Combine
        self.value = [number, date]

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorDataPoint):
            return NotImplemented
        else:
            return (self.field_id == other.field_id) and (
                self.form_instance == other.form_instance
            )

    def __repr__(self) -> str:
        return self.form_instance.record.record_id + " - " \
               + self.form_instance.instance_of.form_name + " - " \
               + self.instance_of.field_name
