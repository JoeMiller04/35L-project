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

