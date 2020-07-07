# -*- coding: utf-8 -*-
"""
Testing class for country endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/country

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random
import pytest

from castoredc_api_client.exceptions import CastorException


class TestCountry:
    country_model = {
        "id": "string",
        "country_id": "string",
        "country_name": "string",
        "country_tld": "string",
        "country_cca2": "string",
        "country_cca3": "string",
    }
    model_keys = country_model.keys()

    @pytest.fixture(scope="class")
    def all_countries(self, client):
        """Returns a list of dicts containing all countries in the Castor database."""
        all_countries = client.all_countries()
        return all_countries

    def test_all_countries(self, all_countries):
        """Tests if the all_countries function returns all_countries"""
        assert len(all_countries) == 250
        countries = [container["country_name"] for container in all_countries]
        assert "Netherlands" in countries
        assert "Maldives" in countries

    def test_all_countries_model(self, all_countries):
        """Tests if the value returned by the all_countries function is equal to the specified country model."""
        for i in range(0, 5):
            random_country = random.choice(all_countries)
            random_keys = random_country.keys()
            assert len(random_keys) == len(self.model_keys)
            for key in random_keys:
                assert key in self.model_keys

    def test_single_country_success(self, client):
        """Tests if the single_country function returns a proper country model."""
        for i in range(0, 5):
            country_id = random.randrange(2, 252)
            result = client.single_country(country_id)
            result_keys = result.keys()
            assert len(result_keys) == len(self.model_keys)
            for key in result_keys:
                assert key in self.model_keys

    def test_single_country_failure_too_large(self, client):
        """Tests if retrieving a non-existent (edge case: upper range) country ID raises an error."""
        with pytest.raises(CastorException) as e:
            country_id = random.randrange(253)
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_negative(self, client):
        """Tests if retrieving a non-existent (edge case: negative) country ID raises an error."""
        with pytest.raises(CastorException) as e:
            country_id = random.randrange(-300, -1)
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_zero(self, client):
        """Tests if retrieving a non-existent (edge case: zero) country ID raises an error."""
        with pytest.raises(CastorException) as e:
            country_id = 0
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_one(self, client):
        """Tests if retrieving a non-existent (edge case: lower range) country ID raises an error."""
        with pytest.raises(CastorException) as e:
            country_id = 1
            result = client.single_country(country_id)
            assert e == "404 Entity not found."
