# api_client/client.py
import json
import logging
import requests
from requests.exceptions import RequestException
from jsonschema import validate, ValidationError

class APIClient:
    """
    A modular API client for making HTTP requests with detailed logging.
    """
    def __init__(self, base_url, headers=None, timeout=10):
        """
        Initialize the API client.
        
        Args:
            base_url (str): The base URL for all API requests
            headers (dict, optional): Default headers to include with each request
            timeout (int, optional): Default request timeout in seconds
        """
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "application/json"}
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def _log_request(self, method, url, headers, params=None, data=None):
        """Log request details."""
        self.logger.info(f"Request: {method} {url}")
        self.logger.debug(f"Headers: {headers}")
        if params:
            self.logger.debug(f"Query Parameters: {params}")
        if data:
            self.logger.debug(f"Request Body: {data}")
            
    def _log_response(self, response):
        """Log response details."""
        self.logger.info(f"Response Status: {response.status_code}")
        self.logger.debug(f"Response Headers: {response.headers}")
        try:
            self.logger.debug(f"Response Body: {response.json()}")
        except ValueError:
            self.logger.debug(f"Response Body: {response.text}")
    
    def _make_request(self, method, endpoint, headers=None, params=None, data=None, json_data=None, files=None):
        """
        Make an HTTP request and handle exceptions.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint (str): API endpoint to call
            headers (dict, optional): Additional headers for this request
            params (dict, optional): Query parameters to include
            data (dict/str, optional): Request body as form data or raw string
            json_data (dict, optional): Request body as JSON
            files (dict, optional): Files to upload
            
        Returns:
            requests.Response: The response object
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers}
        if headers:
            request_headers.update(headers)
            
        self._log_request(method, url, request_headers, params, data or json_data)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                params=params,
                data=data,
                json=json_data,
                files=files,
                timeout=self.timeout
            )
            self._log_response(response)
            return response
        except RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint, headers=None, params=None):
        """Send a GET request."""
        return self._make_request("GET", endpoint, headers, params)
    
    def post(self, endpoint, headers=None, params=None, data=None, json_data=None, files=None):
        """Send a POST request."""
        return self._make_request("POST", endpoint, headers, params, data, json_data, files)
    
    def put(self, endpoint, headers=None, params=None, data=None, json_data=None):
        """Send a PUT request."""
        return self._make_request("PUT", endpoint, headers, params, data, json_data)
    
    def delete(self, endpoint, headers=None, params=None):
        """Send a DELETE request."""
        return self._make_request("DELETE", endpoint, headers, params)
    
    def patch(self, endpoint, headers=None, params=None, data=None, json_data=None):
        """Send a PATCH request."""
        return self._make_request("PATCH", endpoint, headers, params, data, json_data)
    
    def validate_schema(self, response, schema):
        """
        Validate response JSON against a schema.
        
        Args:
            response (requests.Response): Response object
            schema (dict): JSONSchema to validate against
            
        Returns:
            bool: True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            response_json = response.json()
            validate(instance=response_json, schema=schema)
            self.logger.info("Schema validation passed")
            return True
        except ValueError as e:
            self.logger.error(f"Invalid JSON in response: {str(e)}")
            raise
        except ValidationError as e:
            self.logger.error(f"Schema validation failed: {str(e)}")
            raise