from castoredc_api_client.castor_objects.castor_step import CastorStep


class CastorForm:
    """Object representing a form in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, form_collection_name: str, form_collection_id: str, form_collection_type: str) -> None:
        self.form_name = form_collection_name
        self.form_id = form_collection_id
        self.form_type = form_collection_type
        self.study = None
        self.steps = []

    def add_step(self, step: CastorStep) -> None:
        self.steps.append(step)
        step.form = self

    def get_step(self, step_id: str) -> CastorStep:
        return next((step for step in self.steps if step.step_id == step_id), None)

    def __eq__(self, other):
        if not isinstance(other, CastorForm):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.form_id == other.form_id

    def __repr__(self):
        return self.form_id
