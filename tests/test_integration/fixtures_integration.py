import pytest
import auth.auth_data as auth_data

from castoredc_study.castor_study import CastorStudy


@pytest.fixture(scope="class")
def integration_study():
    study = CastorStudy(auth_data.study_id)
    return study
