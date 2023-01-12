# Weather API
## Testing
To perform the required tests for this tool, it was decided to run them inside containers. Running tests inside containers offers great advantages in terms of replicability, isolation, consistent environment, and promotes a gain when the system is applied to an CI pipeline. 

Due to the isolation, all tests should be performed with mocks, without any contact with the external environment. This is why a good choice of software architecture is necessary to be able to cover the code without the need for external systems.

The tool chosen for unit testing was [pytest](https://docs.pytest.org/) and for test coverage we used [coverage.py](https://coverage.readthedocs.io/).

Before proceed with tests, build all necessary images:

`docker-compose -f docker-tests.yml build`

Then you can check unit test coverage using:

`docker-compose -f docker-tests.yml run unit-tests`

You should able to see this response:

[![Coverage](docs/coverage-report.png)]

