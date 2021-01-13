from typing import List, Any, Union
from castoredc_study.castor_objects.castor_field import CastorField


class CastorStep:
    """Object representing a step in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, step_name: str, step_id: str) -> None:
        """Creates a CastorStep object."""
        self.step_name = step_name
        self.step_id = step_id
        self.form = None
        self.fields = []

    def add_field(self, field: CastorField) -> None:
        """Adds a CastorField to the step."""
        self.fields.append(field)
        field.step = self

    def get_all_fields(self) -> List[CastorField]:
        """Returns all linked CastorFields."""
        return self.fields

    def get_single_field(self, field_id: str) -> CastorField:
        """Returns a linked CastorField based on id."""
        return next(
            (field for field in self.fields if field.field_id == field_id), None
        )

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorStep):
            return NotImplemented
        else:
            return self.step_id == other.step_id

    def __repr__(self) -> str:
        return self.step_id
