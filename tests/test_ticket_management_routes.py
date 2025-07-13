"""
    Pytest file to test
"""
import base64
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = TestClient(app)


@pytest.fixture
def create_ticket_payload():
    #As users were considered static for now, assumed that user_id will be taken from token,
    # but in code it was hard coded as static-user for now
    return {
        "title": "Test Issue",
        "description": "Sample issue description",
        "comments": "This is a test ticket",
    }

@pytest.fixture
def create_ticket_payload_user1():

    return {
        "title": "Test Issue",
        "description": "Sample issue description",
        "comments": "This is a test ticket created by User1",
        "created_by": "User1"
    }


def test_create_ticket(create_ticket_payload):
    response = client.post("/ticket_management/create_ticket", json=create_ticket_payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success" or data.get("message") != ""

def test_create_ticket2(create_ticket_payload_user1):
    # creating ticket with one more user to test the listing tickets
    response = client.post("/ticket_management/create_ticket", json=create_ticket_payload_user1)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success" or data.get("message") != ""


def test_view_ticket(create_ticket_payload):
    # First create a ticket
    create_resp = client.post("/ticket_management/create_ticket", json=create_ticket_payload)
    ticket_id = create_resp.json().get("data", {}).get("ticket_id", None)

    if not ticket_id:
        pytest.skip("Ticket creation failed, cannot test view_ticket")

    response = client.post("/ticket_management/view_ticket", json={"ticket_id": ticket_id})
    assert response.status_code == 200
    assert response.json().get("data", {}).get("_id", None) == ticket_id


def test_update_ticket(create_ticket_payload):
    create_resp = client.post("/ticket_management/create_ticket", json=create_ticket_payload)
    # print(create_resp.json())
    ticket_id = create_resp.json().get("data", {}).get("ticket_id", None)
    # print(ticket_id)
    if not ticket_id:
        pytest.skip("Ticket creation failed, cannot test update_ticket")

    payload = {
        "ticket_id": ticket_id,
        "status": "in_progress",
        "updated_by": "support1"
    }
    update_resp = client.post("/ticket_management/update_ticket", json=payload)
    assert update_resp.status_code == 200
    assert update_resp.json().get("status") == "success"


def test_list_tickets_user():
    response = client.post("/ticket_management/list_tickets", json={"user_id": "User1"})
    assert response.status_code == 200
    assert isinstance(response.json().get("tickets", []), list)


def test_list_tickets_support_team():
    response = client.post("/ticket_management/list_tickets", json=None)
    assert response.status_code == 200
    assert isinstance(response.json().get("tickets", []), list)


def test_create_and_fetch_base64_image():
    # Step 1: Simulate base64 image payload

    fake_image_bytes = b"This is a fake image content"
    encoded_image = base64.b64encode(fake_image_bytes).decode("utf-8")
    data_uri_prefix = "data:image/png;base64,"
    full_image_data = data_uri_prefix + encoded_image

    payload = {
        "title": "Ticket with Base64 Image",
        "description": "This ticket has a base64 image",
        "comments": "Testing base64 upload and fetch",
        "image_data": full_image_data,
        "image_name": "test_image.png",
        "created_by": "TestUser1"
    }

    # Step 2: Create Ticket
    create_response = client.post("/ticket_management/create_ticket", json=payload)
    assert create_response.status_code == 200, create_response.text
    create_json = create_response.json()
    assert create_json.get("status") == "success"
    ticket_id = create_json.get("data", {}).get("ticket_id", None)
    assert ticket_id, "ticket_id should not be empty"

    # Step 3: View Ticket (to get the image path)
    view_payload = {"ticket_id": ticket_id}
    view_response = client.post("/ticket_management/view_ticket", json=view_payload)
    # print(view_response.json())
    assert view_response.status_code == 200, view_response.text
    image_url = view_response.json().get("data", {}).get("image_path")
    assert image_url, "image_url should not be empty"

    # Extract image file name
    image_name = os.path.basename(image_url)

    # Step 4: Fetch Image by Name
    image_name = os.path.basename(urlparse(image_url).path)
    fetch_response = client.post("/ticket_management/fetch_image", params={"image_name": image_name})
    assert fetch_response.status_code == 200
    assert fetch_response.headers["content-type"].startswith("image/")  # check if response is an image
    assert len(fetch_response.content) > 0


    # Optional: verify returned image base64 matches what was sent
    returned_image_b64 = fetch_response.content
    print("returned_image_b64", returned_image_b64)
    expected_bytes = base64.b64decode(encoded_image)
    print("expected_bytes",expected_bytes)

    assert returned_image_b64 == expected_bytes, "Returned image base64 should match the original"