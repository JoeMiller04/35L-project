import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

from server.main import app

client = TestClient(app)

ADMIN_KEY = os.getenv("ADMIN_KEY")  

# Simple test to verify testing setup works
def test_test():
    assert True

def test_create_course(client):  
    """Test course creation endpoint"""
    instructor = "Prof AB"
    try:
        response = client.post(
            "/courses",
            json={
                "real": False,
                "term": "23F",
                "subject": "AA",
                "catalog": "BB",
                "title": "CC",
                "instructor": instructor
                },
            headers={"x-api-key": ADMIN_KEY}
        )
        assert response.status_code == 200
        data = response.json()
        assert "_id" in data
        assert data["instructor"] == instructor
        assert data["term"] == "23F"
        assert data["subject"] == "AA"
        assert data["catalog"] == "BB"
        assert data["title"] == "CC"
        
        # Store course ID for cleanup
        course_id = data["_id"]
    finally:
        # Use the delete API for cleanup
        # There is no delete API right now, but we will pretend there is one for now
        if 'course_id' in locals():
            client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})

def test_get_course_by_id(client):
    """Test getting a course by ID"""
    instructor = "Prof XY"
    course_id = None
    try:
        # First create a course
        response = client.post(
            "/courses",
            json={
                "real": False,
                "term": "24W",
                "subject": "TEST",
                "catalog": "101",
                "title": "Test Course",
                "instructor": instructor
            },
            headers={"x-api-key": ADMIN_KEY}
        )
        assert response.status_code == 200
        course_id = response.json()["_id"]
        
        # Get the course by ID
        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        
        # Verify the course data
        assert data["_id"] == course_id
        assert data["instructor"] == instructor
        assert data["term"] == "24W"
        assert data["subject"] == "TEST"
        assert data["catalog"] == "101"
        assert data["title"] == "Test Course"
        assert data["real"] == False
    finally:
        # Clean up: delete the created course
        if course_id:
            # Uncomment when the delete API is implemented
            # client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
            pass

def test_get_nonexistent_course(client):
    """Test getting a course that doesn't exist"""
    # Generate a random ObjectId that shouldn't exist in the database
    random_id = str(ObjectId())
    response = client.get(f"/courses/{random_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_invalid_course_id_format(client):
    """Test accessing a course with invalid ID format"""
    # Use an invalid ObjectId format
    invalid_id = "not-an-objectid"
    response = client.get(f"/courses/{invalid_id}")
    assert response.status_code == 400
    assert "Invalid ID format" in response.json()["detail"]

def test_update_course(client):
    """Test updating a course"""
    instructor = "Initial Prof"
    updated_instructor = "Updated Prof"
    course_id = None
    
    try:
        # First create a course
        response = client.post(
            "/courses",
            json={
                "real": False,
                "term": "24S",
                "subject": "UPDATE",
                "catalog": "101",
                "title": "Test Update Course",
                "instructor": instructor
            },
            headers={"x-api-key": ADMIN_KEY}
        )
        assert response.status_code == 200
        course_id = response.json()["_id"]
        
        # Update the course
        response = client.put(
            f"/courses/{course_id}",
            json={
                "instructor": updated_instructor,
                "title": "Updated Course Title"
            },
            headers={"x-api-key": ADMIN_KEY}
        )
        
        # Verify the update was successful
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == course_id
        assert data["instructor"] == updated_instructor  # Should be updated
        assert data["title"] == "Updated Course Title"  # Should be updated
        assert data["term"] == "24S"  # Should be same
        assert data["subject"] == "UPDATE"  # Should be same
        assert data["catalog"] == "101"  # Should be same
        
        # Verify by re-fetching the course separately
        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["instructor"] == updated_instructor
        assert data["title"] == "Updated Course Title"
        
    finally:
        # Clean up
        if course_id:
            # Uncomment when delete API is implemented
            # client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
            pass
            
            
def test_update_nonexistent_course(client):
    """Test updating a course that doesn't exist"""
    # Generate a random ObjectId that shouldn't exist
    random_id = str(ObjectId())
    
    # Try to update a non-existent course
    response = client.put(
        f"/courses/{random_id}",
        json={"instructor": "No Prof"},
        headers={"x-api-key": ADMIN_KEY}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
    
def test_update_course_invalid_id(client):
    """Test updating a course with invalid ID format"""
    invalid_id = "not-an-objectid"
    
    response = client.put(
        f"/courses/{invalid_id}",
        json={"instructor": "Invalid Prof"},
        headers={"x-api-key": ADMIN_KEY}
    )
    
    assert response.status_code == 400
    assert "Invalid ID format" in response.json()["detail"]
    
    
def test_update_course_no_data(client):
    """Test updating a course with no data provided"""
    # First create a course
    response = client.post(
        "/courses",
        json={
            "real": False,
            "term": "24S",
            "subject": "EMPTY",
            "catalog": "101",
            "title": "Test Empty Update",
            "instructor": "Empty Prof"
        },
        headers={"x-api-key": ADMIN_KEY}
    )
    course_id = response.json()["_id"]
    
    try:
        # Try to update with empty data
        response = client.put(
            f"/courses/{course_id}",
            json={},
            headers={"x-api-key": ADMIN_KEY}
        )
        
        assert response.status_code == 400
        assert "No valid update data" in response.json()["detail"]
        
    finally:
        # Clean up
        if course_id:
            # Uncomment when delete API is implemented
            # client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
            pass
            
            
def test_update_course_unauthorized(client):
    """Test updating a course without admin key"""
    # First create a course with proper admin key
    response = client.post(
        "/courses",
        json={
            "real": False,
            "term": "24S",
            "subject": "AUTH",
            "catalog": "101",
            "title": "Test Auth",
            "instructor": "Auth Prof"
        },
        headers={"x-api-key": ADMIN_KEY}
    )
    course_id = response.json()["_id"]
    
    try:
        # Try to update without admin key
        response = client.put(
            f"/courses/{course_id}",
            json={"instructor": "Unauthorized Prof"},
            # No headers or wrong key
            headers={"x-api-key": "wrong-key"}
        )
        
        assert response.status_code == 401
        assert "Unauthorized" in response.json()["detail"]
        
    finally:
        # Clean up
        if course_id:
            # Uncomment when delete API is implemented
            # client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
            pass


