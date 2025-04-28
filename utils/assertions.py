# utils/assertions.py
import json
import jsonschema

class APIAssertions:
    """Utility class with custom assertion methods for API testing."""
    
    @staticmethod
    def assert_status_code(response, expected_code):
        """
        Assert that the response has the expected status code.
        
        Args:
            response: The response object
            expected_code: Expected HTTP status code
            
        Raises:
            AssertionError: If status code doesn't match
        """
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}"
    
    @staticmethod
    def assert_json_response(response):
        """
        Assert that the response contains valid JSON.
        
        Args:
            response: The response object
            
        Returns:
            dict: The parsed JSON
            
        Raises:
            AssertionError: If response doesn't contain valid JSON
        """
        try:
            return response.json()
        except ValueError:
            raise AssertionError(f"Response is not valid JSON: {response.text}")
    
    @staticmethod
    def assert_schema_valid(response, schema):
        """
        Assert that the response JSON matches the given schema.
        
        Args:
            response: The response object
            schema: JSONSchema to validate against
            
        Raises:
            AssertionError: If schema validation fails
        """
        json_data = APIAssertions.assert_json_response(response)
        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            raise AssertionError(f"Response doesn't match schema: {str(e)}")
    
    @staticmethod
    def assert_header_present(response, header_name):
        """
        Assert that the response contains the specified header.
        
        Args:
            response: The response object
            header_name: Name of the header to check
            
        Raises:
            AssertionError: If header is not present
        """
        assert header_name in response.headers, \
            f"Header '{header_name}' not found in response"
    
    @staticmethod
    def assert_header_value(response, header_name, expected_value):
        """
        Assert that the header has the expected value.
        
        Args:
            response: The response object
            header_name: Name of the header to check
            expected_value: Expected header value
            
        Raises:
            AssertionError: If header value doesn't match
        """
        APIAssertions.assert_header_present(response, header_name)
        assert response.headers[header_name] == expected_value, \
            f"Expected header '{header_name}' to be '{expected_value}', got '{response.headers[header_name]}'"
    
    @staticmethod
    def assert_response_time(response, max_time_ms):
        """
        Assert that the response time is within the expected limit.
        
        Args:
            response: The response object
            max_time_ms: Maximum allowed response time in milliseconds
            
        Raises:
            AssertionError: If response time exceeds the limit
        """
        response_time = response.elapsed.total_seconds() * 1000
        assert response_time <= max_time_ms, \
            f"Response time {response_time}ms exceeds limit of {max_time_ms}ms"
    
    @staticmethod
    def assert_content_type(response, expected_content_type):
        """
        Assert that the response has the expected content type.
        
        Args:
            response: The response object
            expected_content_type: Expected content type
            
        Raises:
            AssertionError: If content type doesn't match
        """
        APIAssertions.assert_header_value(response, "Content-Type", expected_content_type)