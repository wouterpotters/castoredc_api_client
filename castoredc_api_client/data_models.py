# -*- coding: utf-8 -*-
"""
Contains the definition of all data models according to the Castor EDC API.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

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