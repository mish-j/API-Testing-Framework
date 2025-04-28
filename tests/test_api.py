# tests/test_api.py
import pytest
import allure
from utils.assertions import APIAssertions
from schemas import USER_SCHEMA, USERS_LIST_SCHEMA, ERROR_SCHEMA

@allure.epic("REST API Testing Framework")
@allure.feature("Users API")
class TestUsersAPI:
    
    @allure.story("Get all users")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_users(self, api_client):
        """Test getting a list of all users."""
        # Arrange
        endpoint = "/users"
        
        # Act
        with allure.step("Send GET request to /users endpoint"):
            response = api_client.get(endpoint)
        
        # Assert
        with allure.step("Verify response status code is 200"):
            APIAssertions.assert_status_code(response, 200)
            
        with allure.step("Verify response contains valid JSON"):
            json_data = APIAssertions.assert_json_response(response)
            
        with allure.step("Verify response matches schema"):
            APIAssertions.assert_schema_valid(response, USERS_LIST_SCHEMA)
            
        with allure.step("Verify response time is acceptable"):
            APIAssertions.assert_response_time(response, 1000)  # 1000ms = 1s
    
    @allure.story("Get user by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user_by_id(self, api_client, user_id):
        """Test getting a single user by ID."""
        # Arrange
        endpoint = f"/users/{user_id}"
        
        # Act
        with allure.step(f"Send GET request to /users/{user_id} endpoint"):
            response = api_client.get(endpoint)
        
        # Assert
        with allure.step("Verify response status code is 200"):
            APIAssertions.assert_status_code(response, 200)
            
        with allure.step("Verify response matches user schema"):
            APIAssertions.assert_schema_valid(response, USER_SCHEMA)
            
        with allure.step("Verify user ID in response matches requested ID"):
            user_data = APIAssertions.assert_json_response(response)
            assert user_data["id"] == user_id, f"Expected user ID {user_id}, got {user_data['id']}"
    
    @allure.story("Create new user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api_client, test_user):
        """Test creating a new user."""
        # Arrange
        endpoint = "/users"
        
        # Act
        with allure.step("Send POST request to create a new user"):
            response = api_client.post(endpoint, json_data=test_user)
        
        # Assert
        with allure.step("Verify response status code is 201"):
            APIAssertions.assert_status_code(response, 201)
            
        with allure.step("Verify response matches user schema"):
            APIAssertions.assert_schema_valid(response, USER_SCHEMA)
            
        with allure.step("Verify created user data contains submitted values"):
            user_data = APIAssertions.assert_json_response(response)
            assert user_data["name"] == test_user["name"]
            assert user_data["email"] == test_user["email"]
    
    @allure.story("Get non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_non_existent_user(self, api_client):
        """Test getting a user that doesn't exist."""
        # Arrange
        endpoint = "/users/999"  # Assuming 999 is an invalid user ID
        
        # Act
        with allure.step("Send GET request for non-existent user"):
            response = api_client.get(endpoint)
        
        # Assert
        with allure.step("Verify response status code is 404"):
            APIAssertions.assert_status_code(response, 404)
    
    @allure.story("Update user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api_client):
        """Test updating an existing user."""
        # Arrange
        user_id = 1
        endpoint = f"/users/{user_id}"
        update_data = {
            "name": "Updated User Name",
            "email": "updated@example.com"
        }
        
        # Act
        with allure.step(f"Send PUT request to update user {user_id}"):
            response = api_client.put(endpoint, json_data=update_data)
        
        # Assert
        with allure.step("Verify response status code is 200"):
            APIAssertions.assert_status_code(response, 200)
            
        with allure.step("Verify response contains updated data"):
            user_data = APIAssertions.assert_json_response(response)
            assert user_data["name"] == update_data["name"]
            assert user_data["email"] == update_data["email"]
    
    @allure.story("Delete user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, api_client):
        """Test deleting a user."""
        # Arrange
        user_id = 1
        endpoint = f"/users/{user_id}"
        
        # Act
        with allure.step(f"Send DELETE request to remove user {user_id}"):
            response = api_client.delete(endpoint)
        
        # Assert
        with allure.step("Verify response status code is 200"):
            APIAssertions.assert_status_code(response, 200)