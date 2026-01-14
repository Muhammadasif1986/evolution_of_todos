import requests
import json

# Test the backend API
BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing backend API...")

    # Test if the server is running
    try:
        response = requests.get(f"{BASE_URL}")
        print(f"Server status: {response.status_code}")
        print(f"Response: {response.text[:100]}...")  # First 100 chars
    except requests.exceptions.ConnectionError:
        print("Could not connect to backend server. Make sure it's running on http://localhost:8000")
        return

    # Test API docs are available
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"API Docs status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to API docs")

    print("\nBackend server is running and accessible!")
    print(f"Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    test_api()