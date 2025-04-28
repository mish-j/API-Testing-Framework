# conftest.py
import os
import pytest
import logging
from api_client.client import APIClient
from api_client.logger import setup_logger

# Setup logging
setup_logger(log_level=logging.INFO)

def pytest_addoption(parser):
    """Add command-line options for the test framework."""
    parser.addoption(
        "--base-url",
        action="store",
        default="https://jsonplaceholder.typicode.com",
        help="Base URL for the API"
    )
    parser.addoption(
        "--timeout",
        action="store",
        default=10,
        type=int,
        help="Request timeout in seconds"
    )

@pytest.fixture(scope="session")
def base_url(request):
    """Get the base URL from command line args or environment variable."""
    return request.config.getoption("--base-url") or os.environ.get("API_BASE_URL")

@pytest.fixture(scope="session")
def api_timeout(request):
    """Get the API timeout from command line args or environment variable."""
    return request.config.getoption("--timeout") or int(os.environ.get("API_TIMEOUT", 10))

@pytest.fixture(scope="session")
def api_headers():
    """Default headers to use with API requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

@pytest.fixture(scope="session")
def api_client(base_url, api_headers, api_timeout):
    """Create and configure an API client."""
    return APIClient(
        base_url=base_url,
        headers=api_headers,
        timeout=api_timeout
    )

@pytest.fixture(scope="function")
def test_user():
    """Test user data for API tests."""
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone": "123-456-7890"
    }