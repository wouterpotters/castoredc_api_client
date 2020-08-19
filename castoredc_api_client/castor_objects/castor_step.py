from typing import List

from castoredc_api_client.castor_objects.castor_field import CastorField


class CastorStep:
    """Object representing a step in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, step_name: str, step_id: str) -> None:
        self.step_name = step_name
        self.step_id = step_id
        self.form = None
        self.fields = []

    def add_field(self, field: CastorField) -> None:
        self.fields.append(field)
        field.step = self

    def get_all_fields(self) -> List[CastorField]:
        return self.fields

    def get_single_field(self, field_id: str) -> CastorField:
        return next((field for field in self.fields if field.field_id == field_id), None)

    def __eq__(self, other):
        if not isinstance(other, CastorStep):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.step_id == other.step_id

    def __repr__(self):
        return self.step_id
