import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

from server.main import app

client = TestClient(app)
ADMIN_KEY = os.getenv("ADMIN_KEY")

# Test course data for creating test courses
test_course_data = {
    "real": False,
    "subject": "CS",
    "catalog": "101",
    "title": "Introduction to Testing",
    "term": "25S",
    "instructor": "Test Instructor",
}

test_user_data = {
    "username": "course_list_test_user",
    "password": "test_password",
}

course_id = None

def test_test():
    """Simple test to verify testing setup works"""
    assert True


def create_course(client):
    """Create a test course and return the course ID"""

    response = client.post(
        "/courses",
        json=test_course_data,
        headers={"x-api-key": ADMIN_KEY}
    )
    course_id = response.json()["_id"]
    
    assert response.status_code == 200
    assert response.json()["subject"] == test_course_data["subject"]
    assert course_id is not None
    
    return course_id

def create_user(client):
    """Create a test user and return the user ID"""
    
    response = client.post(
        "/users",
        json=test_user_data
    )

    data = response.json()
    assert "_id" in data
    user_id = data["_id"]
    
    assert response.status_code == 200
    assert response.json()["username"] == test_user_data["username"]
    assert user_id is not None
    
    return user_id


def test_add_course_to_list(client):
    """Test adding a course to a user's course list"""
    # Create a test course
    course_id = create_course(client)
    
    # Create a test user
    user_id = create_user(client)
    
    # Add the course to the user's list
    response = client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": course_id, "action": "add"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["course_list"] == [course_id]
    
    # Clean up the test course and user
    client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_add_duplicate_course_to_list(client):
    """Test adding the same course twice to a user's course list"""
    course_id = create_course(client)
    user_id = create_user(client)

    # Add a course
    client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": course_id, "action": "add"}
    )
    
    # Add the same course a second time
    response = client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": course_id, "action": "add"}
    )
    
    # Get the updated user
    assert response.status_code == 200
    data = response.json()
    course_list = data["course_list"]
    
    # Count occurrences of the course ID
    count = course_list.count(course_id)
    
    # Should only appear once
    assert count == 1, f"Course {course_id} appears {course_id} times, expected once"

    # Clean up the test course and user
    client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_remove_course_from_list(client):
    """Test removing a course from a user's course list"""
    course_id = create_course(client)
    user_id = create_user(client)

    # Add a course to user's course list
    client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": course_id, "action": "add"}
    )
    
    # Verify it was added
    response = client.get(f"/users/{user_id}/course-list")
    courses = response.json()
    found = any(course["_id"] == course_id for course in courses)
    assert found, f"Course {user_id} not found after adding"
    
    # Remove the course
    response = client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": course_id, "action": "remove"}
    )
    
    # Check that the course was removed
    assert response.status_code == 200
    data = response.json()
    assert user_id not in data["course_list"]
    
    # Verify through the GET endpoint too
    response = client.get(f"/users/{user_id}/course-list")
    courses = response.json()
    found = any(course["_id"] == course_id for course in courses)
    assert not found, f"Course {course_id} still found after removal"

    # Clean up the test course and user
    client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_remove_nonexistent_course_from_list(client):
    """Test removing a course that's not in the user's list"""
    user_id = create_user(client)
    course_id = create_course(client)

    # Generate a random course ID that shouldn't exist in the user's list
    nonexistent_course_id = str(ObjectId())
    
    # Try to remove a course that's not in the list
    response = client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": nonexistent_course_id, "action": "remove"}
    )
    
    assert response.status_code == 404

    client.delete(f"/courses/{course_id}", headers={"x-api-key": ADMIN_KEY})
    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})


def test_invalid_course_list_action(client):
    """Test using an invalid action with the course list update endpoint"""
    user_id = create_user(client)
    test_course = create_course(client)

    # Try a bad action
    response = client.post(
        f"/users/{user_id}/course-list",
        json={"course_id": test_course, "action": "not_valid"}
    )
    
    # This should fail
    assert response.status_code == 400
    assert "Invalid action" in response.json()["detail"]

    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})



def test_get_course_list_empty(client):
    user_id = create_user(client)

    """Test getting course list for a user with an empty list"""
    response = client.get(f"/users/{user_id}/course-list")
    
    # Should return an empty list
    assert response.status_code == 200
    courses = response.json()
    assert isinstance(courses, list)
    assert len(courses) == 0

    client.delete(f"/users/{user_id}", headers={"x-api-key": ADMIN_KEY})

# TODO A couple more test cases