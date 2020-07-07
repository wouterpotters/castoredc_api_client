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
        all_countries = client.all_countries()
        return all_countries

    def test_all_countries(self, all_countries):
        assert len(all_countries) == 250
        countries = [container["country_name"] for container in all_countries]
        assert "Netherlands" in countries
        assert "Maldives" in countries

    def test_all_countries_model(self, all_countries):
        for i in range(0, 5):
            random_country = random.choice(all_countries)
            random_keys = random_country.keys()
            assert len(random_keys) == len(self.model_keys)
            for key in random_keys:
                assert key in self.model_keys

    def test_single_country_success(self, client):
        for i in range(0, 5):
            country_id = random.randrange(2, 252)
            result = client.single_country(country_id)
            assert result is not None

    def test_single_country_failure_too_large(self, client):
        with pytest.raises(CastorException) as e:
            country_id = random.randrange(252, 400)
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_negative(self, client):
        with pytest.raises(CastorException) as e:
            country_id = random.randrange(-300, 2)
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_zero(self, client):
        with pytest.raises(CastorException) as e:
            country_id = 0
            result = client.single_country(country_id)
            assert e == "404 Entity not found."

    def test_single_country_failure_one(self, client):
        with pytest.raises(CastorException) as e:
            country_id = 1
            result = client.single_country(country_id)
            assert e == "404 Entity not found."
