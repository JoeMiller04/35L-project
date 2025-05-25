import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

from server.main import app

client = TestClient(app)
ADMIN_KEY = os.getenv("ADMIN_KEY")

# These ratings should be in the MongoDB collection already
test_ratings = [
    {"subject": "CHEM", "catalog": "153D", "rating": 4.0},
    {"subject": "CHEM", "catalog": "19", "rating": 4.0},
    {"subject": "COM LIT", "catalog": "C163", "rating": 4.2}
]

def test_get_rating_successful(client):
    """Test successful retrieval of a rating"""
    # Test getting CHEM 153D rating
    response = client.get("/ratings/CHEM/153D")
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "CHEM"
    assert data["catalog"] == "153D"
    assert data["rating"] == 4.0


def test_get_rating_with_space_in_subject(client):
    """Test retrieval of a rating with a space in the subject"""
    # Test getting COM LIT C163 rating
    response = client.get("/ratings/COM%20LIT/C163")
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "COM LIT"
    assert data["catalog"] == "C163"
    assert data["rating"] == 4.2


def test_get_nonexistent_rating(client):
    """Test retrieving a rating that doesn't exist"""
    # Test getting a nonexistent rating
    response = client.get("/ratings/NONEXISTENT/COURSE")
    
    assert response.status_code == 404
    assert "No rating found" in response.json()["detail"]


def test_get_rating_case_insensitive(client):
    """Test that rating lookup is case insensitive"""
    # The database has "CHEM" but we'll query with "chem"
    response = client.get("/ratings/chem/153D")
    
    # Should be 200 since the API converts to uppercase
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "CHEM"
    assert data["catalog"] == "153D"
    assert data["rating"] == 4.0


def test_get_rating_with_special_chars(client):
    """Test retrieval of a rating with special characters in catalog"""
    response = client.get("/ratings/COM%20SCI/35L")
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "COM SCI"
    assert data["catalog"] == "35L"
    assert data["rating"] == 2.8


def test_get_rating_with_number_only_catalog(client):
    """Test retrieval of a rating with a catalog that's just a number"""
    response = client.get("/ratings/CHEM/19")
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "CHEM"
    assert data["catalog"] == "19"
    assert data["rating"] == 4.0


def test_get_all_ratings_for_subject(client):
    """Test getting all ratings for a subject through multiple requests"""
    # This endpoint doesn't support getting all ratings at once,
    # so we'll make separate requests for known CHEM courses
    catalogs = ["153D", "19"]
    
    for catalog in catalogs:
        response = client.get(f"/ratings/CHEM/{catalog}")
        assert response.status_code == 200
        data = response.json()
        assert data["subject"] == "CHEM"
        assert data["catalog"] == catalog
        assert data["rating"] == 4.0