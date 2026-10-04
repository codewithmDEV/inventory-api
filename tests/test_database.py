import pytest
import database

@pytest.fixture(autouse=True)
def reset_inventory():
    original = database.inventory.copy()
    yield
    database.inventory.clear()
    database.inventory.extend(original)

def test_get_all():
    result = database.get_all()
    assert len(result) == 5

def test_get_by_id_found():
    item = database.get_by_id(1)
    assert item["id"] == 1

def test_get_by_id_not_found():
    item = database.get_by_id(999)
    assert item is None

def test_add_item():
    new_item = {
        "product_name": "Test Product",
        "price": 9.99,
        "quantity": 10,
        "brand": "Test Brand",
        "description": "Test Description"
    }
    added_item = database.add_item(new_item)
    assert added_item["id"] is not None
    assert added_item["product_name"] == "Test Product"
    assert len(database.get_all()) == 6

def test_update_item():
    updated_item = database.update_item(1, {"product_name": "Updated", "price": 19.99})
    assert updated_item["product_name"] == "Updated"
    assert updated_item["price"] == 19.99

def test_update_item_not_found():
    result = database.update_item(999, {"price": 99.99})
    assert result is None

def test_delete_item():
    assert database.delete_item(1) is True
    assert database.get_by_id(1) is None
    assert len(database.get_all()) == 4

def test_delete_item_not_found():
    assert database.delete_item(999) is False