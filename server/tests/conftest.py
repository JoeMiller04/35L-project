import os
import sys
import pytest
import asyncio
from fastapi.testclient import TestClient

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the app
from server.main import app

# Override the event_loop fixture to handle closing properly
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    # Don't close the loop - this prevents the "Event loop is closed" errors
    # when pytest-asyncio tries to use it after the test
    # loop.close()

@pytest.fixture(scope="session")
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session", autouse=True)
def final_cleanup():
    yield  # Run all the tests first.
    # After tests are done, run the clean_db.py script.
    # This prevents test courses from being left in the database
    os.system("python server/data/clean_db.py")

