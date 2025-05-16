import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

# Import app after patching MongoDB in conftest.py
from server.main import app

client = TestClient(app)

"""Test suite for the user API endpoints.
Currently tests the following endpoints:
- POST /users
- DELETE /users/{id}
- GET /users/{id}
- POST /login
"""


ADMIN_KEY = os.getenv("ADMIN_KEY")  

# Simple test to verify testing setup works
def test_test():
    assert True

def test_create_user(client):  # Add client as parameter to get it from fixture
    """Test user creation endpoint"""
    username = "testuser1151"
    try:
        response = client.post(
            "/users",
            json={"username": username, "password": "testpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "_id" in data
        assert data["username"] == username
        
        # Store user ID for cleanup
        user_id = data["_id"]
    finally:
        # Use the delete API for cleanup
        if 'user_id' in locals():
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_delete_user(client):  
    """Test user deletion endpoint"""
    username = "deleteuser"
    user_id = None
    try:
        # First create a user
        response = client.post(
            "/users",
            json={"username": username, "password": "testpassword"}
        )
        user_id = response.json()["_id"]

        # Use wrong API key
        response = client.delete(f"/users/{user_id}", headers={"x-api-key": "wrongkey"})
        assert response.status_code == 401
        assert "Unauthorized" in response.json()["detail"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})
        assert response.status_code == 204
        
        # Try to get the deleted user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404
    finally:
        # If the user was not deleted, clean up here
        if user_id and response.status_code != 200:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_create_duplicate_user(client):  
    """Test creating a user with an existing username"""
    username = "duplicate"
    user_id = None
    try:
        # First create a user
        response1 = client.post(
            "/users",
            json={"username": username, "password": "password1"}
        )
        user_id = response1.json()["_id"]
        
        # Try to create another user with the same username
        response = client.post(
            "/users",
            json={"username": username, "password": "password2"}
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    finally:
        # Use the delete API for cleanup
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_get_user_by_id(client):  # Add client as parameter
    """Test getting a user by ID"""
    username = "getuser"
    user_id = None
    try:
        # First create a user
        create_response = client.post(
            "/users",
            json={"username": username, "password": "password"}
        )
        user_id = create_response.json()["_id"]
        
        # Get the user by ID
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == user_id
        assert data["username"] == username
    finally:
        # Use the delete API for cleanup
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_invalid_user_id_format(client):
    """Test accessing a user with invalid ID format"""
    # Use an invalid ObjectId format
    invalid_id = "not-an-objectid"
    response = client.get(f"/users/{invalid_id}")
    assert response.status_code == 400


def test_get_nonexistent_user(client):
    """Test getting a user that doesn't exist"""
    # Generate a random ObjectId that shouldn't exist in the database
    random_id = str(ObjectId())
    response = client.get(f"/users/{random_id}")
    assert response.status_code == 404


def test_login_success(client):  # Add client as parameter
    """Test successful login"""
    username = "loginuser"
    user_id = None
    try:
        # First create a user
        response = client.post(
            "/users",
            json={"username": username, "password": "correctpass"}
        )
        user_id = response.json()["_id"]
        
        # Login with correct credentials
        response = client.post(
            "/login",
            params={"username": username, "password": "correctpass"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "_id" in data
        assert data["username"] == username
    finally:
        # Use the delete API for cleanup
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_login_wrong_password(client):  # Add client as parameter
    """Test login with incorrect password"""
    username = "wrongpass"
    user_id = None
    try:
        # First create a user
        response = client.post(
            "/users",
            json={"username": username, "password": "correctpass"}
        )
        user_id = response.json()["_id"]
        
        # Login with wrong password
        response = client.post(
            "/login",
            params={"username": username, "password": "wrongpass"}
        )
        
        assert response.status_code == 401
    finally:
        # Use the delete API for cleanup
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_add_course_to_user(client):
    """Test adding a course to a user's saved list"""
    username = "courseuser1"
    course_name = "CS 35L"
    user_id = None
    
    try:
        # First create a user
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        assert response.status_code == 200
        user_id = response.json()["_id"]
        
        # Add a course to user's saved list
        response = client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "add"}
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == user_id
        assert data["username"] == username
        assert course_name in data["saved_courses"]
        
        # Get the user's courses list directly
        response = client.get(f"/users/{user_id}/courses")
        assert response.status_code == 200
        courses = response.json()
        assert course_name in courses
        
    finally:
        # Use the delete API for cleanup
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_add_duplicate_course(client):
    """Test adding the same course twice to a user's list"""
    username = "courseuser2"
    course_name = "MATH 31A"
    user_id = None
    
    try:
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        user_id = response.json()["_id"]
        
        client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "add"}
        )
        
        # Add the same course a second time
        response = client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "add"}
        )
        
        # Should only show up once
        assert response.status_code == 200
        data = response.json()
        saved_courses = data["saved_courses"]
        assert saved_courses.count(course_name) == 1
        
    finally:
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_remove_course(client):
    """Test removing a course from a user's saved list"""
    username = "courseuser3"
    course_name = "PHYS 1A"
    user_id = None
    
    try:
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        user_id = response.json()["_id"]
        
        # Add a course to user's saved list
        client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "add"}
        )
        
        response = client.get(f"/users/{user_id}/courses")
        courses = response.json()
        assert course_name in courses
        
        response = client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "remove"}
        )
        
        # Check that the course was removed
        assert response.status_code == 200
        data = response.json()
        assert course_name not in data["saved_courses"]
        
    finally:
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_remove_nonexistent_course(client):
    """Test removing a course that's not in the user's list"""
    username = "courseuser4"
    course_name = "HIST 1A"
    user_id = None
    
    try:
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        user_id = response.json()["_id"]
        
        # Try to remove a course that's not in the list
        response = client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "remove"}
        )
        
        # This should succeed anyway
        assert response.status_code == 200
        
    finally:
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_invalid_course_action(client):
    """Test using an invalid action with the course update endpoint"""
    username = "courseuser5"
    course_name = "CHEM 14A"
    user_id = None
    
    try:
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        user_id = response.json()["_id"]
        
        # Try a bad action
        response = client.post(
            f"/users/{user_id}/courses",
            json={"course_name": course_name, "action": "not real action"}
        )
        
        # This should fail
        assert response.status_code == 400
        assert "Invalid action" in response.json()["detail"]
        
    finally:
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_get_courses_empty_list(client):
    """Test getting courses for a user with no saved courses"""
    username = "courseuser6"
    user_id = None
    
    try:
        # First create a user with no saved courses
        response = client.post(
            "/users",
            json={"username": username, "password": "testpass"}
        )
        user_id = response.json()["_id"]
        
        response = client.get(f"/users/{user_id}/courses")
        
        # Should return an empty list
        assert response.status_code == 200
        courses = response.json()
        assert isinstance(courses, list)
        assert len(courses) == 0
        
    finally:
        if user_id:
            client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_get_courses_nonexistent_user(client):
    """Test getting courses for a user that doesn't exist"""
    # Generate a random ObjectId that shouldn't exist
    random_id = str(ObjectId())
    
    # Try to get courses for non-existent user
    response = client.get(f"/users/{random_id}/courses")
    
    # Should fail with user not found
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_add_course_invalid_user_id(client):
    """Test adding a course with an invalid user ID format"""
    invalid_id = "not-an-objectid"
    
    # Try to add a course with invalid user ID
    response = client.post(
        f"/users/{invalid_id}/courses",
        json={"course_name": "CS 31", "action": "add"}
    )
    
    # Should fail with invalid ID format
    assert response.status_code == 400
    assert "Invalid user ID format" in response.json()["detail"]

