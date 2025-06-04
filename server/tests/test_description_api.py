import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
import os

from server.main import app

client = TestClient(app)
ADMIN_KEY = os.getenv("ADMIN_KEY")




def test_get_description_successful(client):
    """Test successful retrieval of a description"""
    # Test getting PHYSICS 1A description
    response = client.get("/descriptions/PHYSICS/1A")
    
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "PHYSICS"
    assert data["catalog"] == "1A"
    assert data["units"] == "5.0"
    assert data["description"][0:5] == "Lectu" 





def test_get_nonexistent_description(client):
    """Test retrieving a description that doesn't exist"""
    # Test getting a nonexistent description
    response = client.get("/description/NONEXISTENT/COURSE")
    
    assert response.status_code == 404
    assert "No description found" in response.json()["detail"]

