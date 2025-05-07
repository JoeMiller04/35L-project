import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

# Import app after patching MongoDB in conftest.py
from server.main import app

client = TestClient(app)

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