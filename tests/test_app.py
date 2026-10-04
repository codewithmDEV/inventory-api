import pytest
import database
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    original = database.inventory.copy()
    yield
    database.inventory.clear()
    database.inventory.extend(original)


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()["inventory"]) == 5


def test_get_item_found(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["item"]["id"] == 1


def test_get_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_post_item_success(client):
    response = client.post("/inventory", json={
        "product_name": "Test",
        "price": 9.99,
        "quantity": 10
    })
    assert response.status_code == 201
    assert response.get_json()["item"]["product_name"] == "Test"


def test_post_item_missing_name(client):
    response = client.post("/inventory", json={"price": 9.99, "quantity": 10})
    assert response.status_code == 400


def test_post_item_bad_price(client):
    response = client.post("/inventory", json={
        "product_name": "Test",
        "price": "not a number",
        "quantity": 10
    })
    assert response.status_code == 400


def test_patch_item_success(client):
    response = client.patch("/inventory/1", json={"price": 12.99})
    assert response.status_code == 200
    assert response.get_json()["item"]["price"] == 12.99


def test_patch_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1.0})
    assert response.status_code == 404


def test_delete_item_success(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_search_items(client):
    response = client.get("/inventory/search?query=almond")
    assert response.status_code == 200
    assert len(response.get_json()["results"]) == 2


def test_search_no_query(client):
    response = client.get("/inventory/search")
    assert response.status_code == 400


def test_fetch_barcode_success(client, monkeypatch):
    monkeypatch.setattr(
        "app.external_api.fetch_by_barcode",
        lambda barcode: {"product_name": "Nutella", "brands": "Ferrero"}
    )
    response = client.get("/inventory/fetch/3017620422003")
    assert response.status_code == 200
    assert response.get_json()["product"]["product_name"] == "Nutella"


def test_fetch_barcode_not_found(client, monkeypatch):
    monkeypatch.setattr(
        "app.external_api.fetch_by_barcode",
        lambda barcode: None
    )
    response = client.get("/inventory/fetch/0000000000000")
    assert response.status_code == 404