# -*- coding: utf-8 -*-
"""
Contains the definition of all data models according to the Castor EDC API.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

country_model_1 = {
    "id": str,
    "country_id": str,
    "country_name": str,
    "country_tld": str,
    "country_cca2": str,
    "country_cca3": str,
    "_links": dict,
}

country_model_2 = {
    "id": str,
    "country_id": str,
    "country_name": str,
    "country_tld": str,
    "country_cca2": str,
    "country_cca3": str,
}

study_data_point_model = {
    "field_id": str,
    "field_value": str,
    "record_id": str,
    "updated_on": str,
}

report_data_point_model = {
    "field_id": str,
    "report_instance_id": str,
    "report_instance_name": str,
    "field_value": str,
    "record_id": str,
    "updated_on": str,
}

survey_data_point_model = {
    "field_id": str,
    "survey_instance_id": str,
    "survey_name": str,
    "field_value": str,
    "record_id": str,
    "updated_on": str,
}

field_dep_model = {
    "id": str,
    "operator": str,
    "value": str,
    "parent_id": str,
    "child_id": str,
    "_links": dict,
}

field_model = {
    "id": [str, ],
    "parent_id": [str, ],
    "field_id": [str, ],
    "field_number": [int, ],
    "field_label": [str, ],
    "field_is_alias": [bool, ],
    "field_variable_name": [str, type(None)],
    "field_type": [str, ],
    "field_required": [int, ],
    "field_hidden": [int, ],
    "field_info": [str, ],
    "field_units": [str, ],
    "field_min": [int, float, type(None), ],
    "field_min_label": [str, type(None), ],
    "field_max": [int, float, type(None), ],
    "field_max_label": [str, type(None), ],
    "field_summary_template": [str, type(None), ],
    "field_slider_step": [int, type(None), ],
    "report_id": [str, ],
    "field_length": [int, type(None), ],
    "additional_config": [str, ],
    "exclude_on_data_export": [bool, ],
    "option_group": [dict, type(None), ],
    "metadata_points": [list, ],
    "validations": [list, ],
    "dependency_parents": [list, ],
    "dependency_children": [list, ],
    "_links": [dict, ],
}

field_opt_model = {
    "id": str,
    "name": str,
    "description": str,
    "layout": bool,
    "options": list,
    "_links": dict,
}

field_val_model = {
    "id": int,
    "type": str,
    "value": str,
    "operator": str,
    "text": str,
    "field_id": str,
    "_links": dict,
}

institute_model = {
    "id": [str, ],
    "institute_id": [str, ],
    "name": [str, ],
    "abbreviation": [str, ],
    "code": [str, type(None)],
    "order": [int, ],
    "country_id": [int, ],
    "deleted": [bool, ],
    "_links": [dict, ],
}

metadata_model = {
    "id": [str, ],
    "metadata_type": [dict, ],
    "parent_id": [str, type(None)],
    "value": [str, ],
    "description": [str, type(None)],
    "element_type": [str, ],
    "element_id": [str],
    "_links": [dict, ],
}