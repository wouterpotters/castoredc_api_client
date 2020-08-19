from typing import Optional


class CastorField:
    """Object representing a Castor Field. Functions as a node of a tree for all interrelations."""

    def __init__(self, field_name: str, field_id: str, field_type: str, field_label: str, field_required: bool,
                 field_option_group: Optional[str]) -> None:
        self.field_id = field_id
        self.field_name = field_name
        self.field_label = field_label
        self.field_type = field_type
        self.field_required = field_required
        self.field_option_group = field_option_group
        self.step = None

    def __eq__(self, other):
        if not isinstance(other, CastorField):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.field_id == other.field_id

    def __repr__(self):
        return self.field_id
