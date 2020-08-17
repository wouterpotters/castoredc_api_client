import itertools


class CastorField:
    """Object representing a Castor Field. Functions as a node of a tree for all interrelations."""

    def __init__(self, field_id: str, field_name: str, field_label: str, field_type: str, field_required: bool,
                 field_option_group: str) -> None:
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
        # TODO: more informative
        return "{field_name} - {field_label} - {step_name} - {form_name}".format(
            field_name=self.field_name,
            field_label=self.field_label,
            step_name=self.step.step_name,
            form_name=self.step.form.form_name
        )


class CastorStep:
    """Object representing a step in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, step_id: str, step_name: str) -> None:
        self.step_id = step_id
        self.step_name = step_name
        self.form = None
        self.fields = []

    def add_field(self, field: CastorField) -> None:
        self.fields.append(field)
        field.step = self

    def get_field(self, field_id: str) -> CastorField:
        return next((field for field in self.fields if field.field_id == field_id), None)

    def __eq__(self, other):
        if not isinstance(other, CastorStep):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.step_id == other.step_id

    def __repr__(self):
        return "{step_name} - {form_name}".format(
            step_name=self.step_name,
            form_name=self.form.form_name
        )


class CastorForm:
    """Object representing a form in Castor. Functions as a branch of a tree for all interrelations."""

    def __init__(self, form_collection_type: str, form_collection_id: str, form_collection_name: str) -> None:
        self.form_type = form_collection_type
        self.form_id = form_collection_id
        self.form_name = form_collection_name
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
        return "{form_name}".format(
            form_name=self.form_name
        )


class CastorStudy:
    """Object representing a study in Castor. Functions as the head of a tree for all interrelations."""
    # TODO: Add study name and other characteristics
    def __init__(self, study_id: str) -> None:
        self.study_id = study_id
        self.forms = []

    def add_form(self, form: CastorForm) -> None:
        self.forms.append(form)
        form.study = self

    def get_form(self, form_id: str) -> CastorForm:
        return next((form for form in self.forms if form.form_id == form_id), None)

    def get_all_fields(self):
        # TODO: Documentation everywhere
        steps = list(itertools.chain.from_iterable([_form.steps for _form in self.forms]))
        fields = list(itertools.chain.from_iterable([_step.fields for _step in steps]))
        return fields

    def get_single_field(self, field_id):
        fields = self.get_all_fields()
        return next((field for field in fields if field.field_id == field_id), None)

    def __eq__(self, other):
        if not isinstance(other, CastorStudy):
            return ValueError("Can't compare {0} and {1}".format(type(other), type(self)))
        else:
            return self.study_id == other.study_id

    def __repr__(self):
        return "{form_name}".format(
            form_name=self.study_id
        )
