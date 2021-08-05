# CastorEDC API Client
This is a Python package for interacting with the API of Castor Electronic Data Capture (EDC).
The package contains functions for all the endpoints defined on https://data.castoredc.com/api#/.

## Getting Started

1. Install the package through pip: `pip install castoredc-api-client` _or_ copy the `castoredc_api_client` folder to your current project folder.
2. Open a Python project and import the client
3. Instantiate the client with your client-ID and client-secret (don't share these!) and url to the server.
4. Link your study with the study-ID
5. Use the wrapper functions to start working with your study.

For all implemented functions, see: https://data.castoredc.com/api#/

```python
import castoredc_api_client

# Create a client with your credentials
c = CastorClient('MYCLIENTID', 'MYCLIENTSECRET', 'data.castoredc.com') 

# Link the client to your study in the Castor EDC database
c.link_study('MYSTUDYID')


# Then you can interact with the API
# Get all records
c.all_records()

# Create a new survey package
c.create_survey_package_instance(survey_package_id="FAKESURVEY-PACKAGE-ID",
                                 record_id="TEST-RECORD",
                                 email_address="obviously@fakeemail.com",
                                 auto_send=True)
```

### Prerequisites

1. Python version > 3.0
2. Requests

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/reiniervlinschoten/castoredc_api_client/tags). 

## Authors

* **R.C.A. van Linschoten** - *Initial Development* - [Reinier van Linschoten](https://github.com/reiniervlinschoten)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Franciscus Gasthuis & Vlietland for making time available for development  
* Castor EDC for support and code review
