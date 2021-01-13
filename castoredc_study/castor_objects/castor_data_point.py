from typing import Union, Any, TYPE_CHECKING

from exceptions.exceptions import CastorException

if TYPE_CHECKING:
    from castoredc_study.castor_objects.castor_field import CastorField
    from castoredc_study.castor_study import CastorStudy


class CastorDataPoint:
    """Object representing a Castor datapoint. Is an instance of a field with a value for a record.."""

    def __init__(
        self, field_id: str, value: Union[str, int], study: "CastorStudy"
    ) -> None:
        """Creates a CastorField."""
        self.field_id = field_id
        self.value = value
        self.instance_of = self.find_field(study)
        if self.instance_of is None:
            raise CastorException(
                "The field that this is an instance of does not exist in the study!"
            )
        self.form_instance = None

    # Helpers
    def find_field(self, study: "CastorStudy") -> "CastorField":
        return study.get_single_field(self.field_id)

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorDataPoint):
            return NotImplemented
        else:
            return (self.field_id == other.field_id) and (
                self.form_instance == other.form_instance
            )

    def __repr__(self) -> str:
        return self.field_id
