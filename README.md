# Castor-Client

This is a Python package for interacting with the API of Castor Electronic Data Capture (EDC).
The package contains functions for all the endpoints defined on https://data.castoredc.com/api#/.
Logging functionalities are included for keeping an audit trail.

## Getting Started

1. Install the package through pip: `pip install castor-client`
2. Open a Python project and import the client
3. Instantiate the client with your client-ID and client-secret (don't share these!)
4. Link your study with the study-ID
5. Use the wrapper functions to start working with your database

```python
from castoredc_api_client.castoredc_api_client import CastorClient
c = CastorClient('MYCLIENTID', 'MYCLIENTSECRET')
c.link_study('MYSTUDYID')

c.all_records()
```

### TODOs

#### Package
* Expand docstrings for all functions
* Expand documentation for all lines so users understand different steps
* Expand data-mapping (efficient sorting algorithms for client.fields)
* Allow file-uploading functionality
* Refactor create_survey_package_instance
* Refactor retrieve_data_by_id to only work for the intentioned use case and create a different function for the usecase of record_progress

#### Tests
* Make failing tests expect CastorException
* Create docstring for each test
* Add comments to parts of tests to clarify what is happening
* Increase test coverage (edge cases)
* Test model values (currently only testing model keys)

### Prerequisites

1. Python version > 3.6.0
2. Requests

### Installing Dev Environment

TODO

## Running the tests

TODO

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **R.C.A. van Linschoten** - *Initial Development* - [Reinier van Linschoten](https://github.com/reiniervlinschoten)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Franciscus Gasthuis & Vlietland for making time available for development  
* Castor EDC for support and code review
