# REST API Testing Framework

A comprehensive testing framework for REST APIs using Python, Pytest, and Requests.

## Features

- Supports testing all CRUD operations
- Configurable test environment
- Detailed test reporting
- Test data generation
- Schema validation
- Parallel test execution
- Smoke and regression test suites

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/api-test-framework.git
   cd api-test-framework
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. For Allure reporting, install Allure command-line tool:
   - On macOS: `brew install allure`
   - On Windows: Download from [GitHub](https://github.com/allure-framework/allure2/releases)

## Configuration

Update configuration settings in `config/config.py` to match your test environment:

- `BASE_URL`: API base URL
- `TIMEOUT`: Request timeout in seconds
- `RETRY_COUNT`: Number of retry attempts for failed requests

## Running Tests

### Basic Usage

Run all tests:
```
python run_tests.py
```

Run with verbose output:
```
python run_tests.py -v
```

### Test Suites

Run smoke tests only:
```
python run_tests.py --smoke
```

Run regression tests only:
```
python run_tests.py --regression
```

### Reporting

Generate HTML report:
```
python run_tests.py --html
```

Generate Allure report:
```
python run_tests.py --allure
```

View Allure report:
```
allure serve reports/[timestamp]/allure-results
```

## Project Structure

```
api_test_framework/
├── config/           # Configuration files
├── tests/            # Test modules
├── utils/            # Utility modules
├── reports/          # Test reports (generated)
├── conftest.py       # Common fixtures
├── run_tests.py      # Test runner
└── requirements.txt  # Dependencies
```

## Adding New Tests

1. Create a new test file in the `tests/` directory
2. Import required modules and fixtures
3. Create test functions using appropriate markers
4. Run the tests

Example:
```python
import pytest
import allure
from utils.api_client import APIClient

@pytest.mark.api
@pytest.mark.smoke
def test_example(api_client):
    response = api_client.get("/endpoint")
    assert response.status_code == 200
```

## Best Practices

- Keep tests independent and idempotent
- Use descriptive test names
- Add appropriate test markers
- Validate response schemas
- Test both positive and negative scenarios
- Use fixtures for setup and teardown
